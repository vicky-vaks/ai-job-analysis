import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import json

# Configuration
st.set_page_config(page_title="AI Job Market Intelligence", layout="wide")
API_URL = "http://localhost:8000"

st.title("🚀 AI-Driven Job Market Intelligence System")
st.markdown("""
Analyze high-demand skills, predict your potential salary, and get personalized skill recommendations to optimize your career path.
""")

# Load local data for global insights
@st.cache
def load_data():
    return pd.read_csv("data/job_market_data.csv")

df = load_data()

# Sidebar - Navigation
menu = st.sidebar.selectbox("Navigation", ["Market Overview", "Salary Predictor", "Skill Path Optimizer"])

if menu == "Market Overview":
    st.header("📊 Global Market Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top Demanded Skills")
        all_skills = df['Skills'].str.split(', ').explode()
        skill_counts = all_skills.value_counts().head(10).reset_index()
        skill_counts.columns = ['Skill', 'Frequency']
        fig1 = px.bar(skill_counts, x='Frequency', y='Skill', orientation='h', color='Frequency', color_continuous_scale='Viridis')
        st.plotly_chart(fig1, use_container_width=True)
        
    with col2:
        st.subheader("Salary Distribution by Role")
        fig2 = px.box(df, x='Salary', y='Job Title', color='Job Title', title="Salary Ranges")
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Market Heatmap: Salary vs Experience")
    fig3 = px.scatter(df, x='Experience Level', y='Salary', color='Job Title', size='Salary', hover_data=['Location'])
    st.plotly_chart(fig3, use_container_width=True)

elif menu == "Salary Predictor":
    st.header("💰 Salary Prediction Engine")
    st.write("Enter your profile details to estimate your market value.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        job_title = st.selectbox("Target Job Title", sorted(df['Job Title'].unique()))
        location = st.selectbox("Location", sorted(df['Location'].unique()))
        experience = st.selectbox("Experience Level", sorted(df['Experience Level'].unique()))
    
    with col2:
        all_possible_skills = sorted(list(set(df['Skills'].str.split(', ').explode())))
        selected_skills = st.multiselect("Your Skills", all_possible_skills)
    
    if st.button("Predict Salary"):
        payload = {
            "job_title": job_title,
            "location": location,
            "experience_level": experience,
            "skills": selected_skills
        }
        try:
            response = requests.post(f"{API_URL}/predict_salary", json=payload)
            if response.status_code == 200:
                result = response.json()
                st.success(f"Estimated Market Salary: ${result['predicted_salary']:,.2f}")
                st.info("Note: This prediction is based on current market trends and model training data.")
            else:
                st.error("Error connecting to API. Ensure the backend is running.")
        except Exception as e:
            st.error(f"Connection failed: {e}")

elif menu == "Skill Path Optimizer":
    st.header("🎯 Skill Recommendation Engine")
    st.write("Identify gaps in your skill set for your dream role.")
    
    target_job = st.selectbox("Desired Role", sorted(df['Job Title'].unique()))
    current_skills = st.multiselect("Your Current Skills", sorted(list(set(df['Skills'].str.split(', ').explode()))))
    
    if st.button("Generate Recommendations"):
        payload = {
            "target_job": target_job,
            "current_skills": current_skills
        }
        try:
            response = requests.post(f"{API_URL}/recommend_skills", json=payload)
            if response.status_code == 200:
                data = response.json()
                
                st.subheader(f"Top 5 Skills to Learn for {target_job}:")
                for skill in data['recommended_skills']:
                    st.write(f"- ✅ {skill}")
                
                st.subheader("Most Common Skills in this Role:")
                st.write(", ".join(data['top_market_skills']))
                
                # Visual comparison
                st.subheader("Skill Gap Analysis")
                market_skills = data['top_market_skills']
                overlap = set(market_skills).intersection(set(current_skills))
                gap = set(market_skills).difference(set(current_skills))
                
                st.progress(len(overlap) / len(market_skills) if market_skills else 0)
                st.write(f"You have {len(overlap)} out of {len(market_skills)} core skills for this role.")
                
            else:
                st.error("Error connecting to API.")
        except Exception as e:
            st.error(f"Connection failed: {e}")

st.sidebar.markdown("---")
st.sidebar.info("Developed G R VIGNESH")
