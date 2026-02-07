from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
from typing import List, Optional

app = FastAPI(title="AI Job Market Intelligence API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data for market insights
try:
    df_market = pd.read_csv("data/job_market_data.csv")
except Exception as e:
    print(f"Error loading CSV data: {e}")
    df_market = pd.DataFrame()

# Load models and artifacts
try:
    model = joblib.load("src/models/salary_model.pkl")
    le_title = joblib.load("src/models/le_title.pkl")
    le_loc = joblib.load("src/models/le_loc.pkl")
    le_exp = joblib.load("src/models/le_exp.pkl")
    mlb = joblib.load("src/models/mlb_skills.pkl")
    feature_columns = joblib.load("src/models/feature_columns.pkl")
    skill_freq = joblib.load("src/models/skill_recommendation_data.pkl")
except Exception as e:
    print(f"Error loading models: {e}")

class PredictionRequest(BaseModel):
    job_title: str
    location: str
    experience_level: str
    skills: List[str]

class PredictionResponse(BaseModel):
    predicted_salary: float

class RecommendationRequest(BaseModel):
    target_job: str
    current_skills: List[str]

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Job Market Intelligence API"}

@app.get("/market_data")
def get_market_data():
    if df_market.empty:
        return {"error": "Data not available"}
    
    # Calculate some basic stats for the dashboard
    all_skills = df_market['Skills'].str.split(', ').explode()
    skill_counts = all_skills.value_counts().head(12).to_dict()
    
    job_salary = df_market.groupby('Job Title')['Salary'].mean().to_dict()
    
    exp_salary = df_market.groupby('Experience Level')['Salary'].mean().to_dict()
    
    return {
        "skill_demand": [{"skill": k, "count": v} for k, v in skill_counts.items()],
        "job_salary": [{"title": k, "salary": v} for k, v in job_salary.items()],
        "exp_salary": [{"level": k, "salary": v} for k, v in exp_salary.items()],
        "total_postings": len(df_market)
    }

@app.post("/predict_salary", response_model=PredictionResponse)
def predict_salary(req: PredictionRequest):
    try:
        # Encode inputs
        # Use a default/catch-all if label is unknown (simplified)
        def safe_encode(le, val):
            try:
                return le.transform([val])[0]
            except:
                return 0 # Default to first category if unknown

        title_enc = safe_encode(le_title, req.job_title)
        loc_enc = safe_encode(le_loc, req.location)
        exp_enc = safe_encode(le_exp, req.experience_level)
        
        # Skill encoding
        skill_vector = mlb.transform([req.skills])
        skills_df = pd.DataFrame(skill_vector, columns=[f"Skill_{s}" for s in mlb.classes_])
        
        # Prepare input df
        input_data = pd.DataFrame([[title_enc, loc_enc, exp_enc]], columns=['Title_Enc', 'Loc_Enc', 'Exp_Enc'])
        full_input = pd.concat([input_data, skills_df], axis=1)
        
        # Ensure all columns exist (even if not in current request skills)
        for col in feature_columns:
            if col not in full_input.columns:
                full_input[col] = 0
        
        # Reorder columns to match training
        full_input = full_input[feature_columns]
        
        prediction = model.predict(full_input)[0]
        return PredictionResponse(predicted_salary=round(prediction, 2))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recommend_skills")
def recommend_skills(req: RecommendationRequest):
    try:
        # Get top skills for the target job title
        job_skills = skill_freq[skill_freq['Job Title'] == req.target_job]
        if job_skills.empty:
            return {"recommended_skills": [], "message": "Job title not found in training data"}
        
        # Filter out skills the user already has
        recommendations = job_skills[~job_skills['Skills_List'].isin(req.current_skills)]
        recommendations = recommendations.sort_values(by='count', ascending=False)
        
        return {
            "target_job": req.target_job,
            "recommended_skills": recommendations['Skills_List'].head(5).tolist(),
            "top_market_skills": job_skills.sort_values(by='count', ascending=False)['Skills_List'].head(10).tolist()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
