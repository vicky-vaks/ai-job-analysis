import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import os

def train_models():
    # Load data
    df = pd.read_csv("data/job_market_data.csv")
    
    # --- 1. Salary Prediction Model ---
    # Preprocessing
    df['Skills_List'] = df['Skills'].apply(lambda x: [s.strip() for s in x.split(',')])
    
    # Encode categorical features
    le_title = LabelEncoder()
    le_loc = LabelEncoder()
    le_exp = LabelEncoder()
    
    df['Title_Enc'] = le_title.fit_transform(df['Job Title'])
    df['Loc_Enc'] = le_loc.fit_transform(df['Location'])
    df['Exp_Enc'] = le_exp.fit_transform(df['Experience Level'])
    
    # MultiLabelBinarizer for Skills
    mlb = MultiLabelBinarizer()
    skills_encoded = mlb.fit_transform(df['Skills_List'])
    skills_columns = [f"Skill_{s}" for s in mlb.classes_]
    skills_df = pd.DataFrame(skills_encoded, columns=skills_columns)
    
    X = pd.concat([df[['Title_Enc', 'Loc_Enc', 'Exp_Enc']], skills_df], axis=1)
    y = df['Salary']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    print(f"Salary Model MAE: {mean_absolute_error(y_test, y_pred):.2f}")
    print(f"Salary Model R2: {r2_score(y_test, y_pred):.2f}")
    
    # Save Model artifacts
    os.makedirs("src/models", exist_ok=True)
    joblib.dump(model, "src/models/salary_model.pkl")
    joblib.dump(le_title, "src/models/le_title.pkl")
    joblib.dump(le_loc, "src/models/le_loc.pkl")
    joblib.dump(le_exp, "src/models/le_exp.pkl")
    joblib.dump(mlb, "src/models/mlb_skills.pkl")
    joblib.dump(X.columns.tolist(), "src/models/feature_columns.pkl")
    
    # --- 2. Skill Recommendation Preparation ---
    # We will use simple frequency-based correlation for recommendations
    # Calculate skill-job title mapping
    skill_job_matrix = df.explode('Skills_List')
    skill_freq = skill_job_matrix.groupby(['Job Title', 'Skills_List']).size().reset_index(name='count')
    joblib.dump(skill_freq, "src/models/skill_recommendation_data.pkl")
    
    print("Models and artifacts saved successfully.")

if __name__ == "__main__":
    train_models()
