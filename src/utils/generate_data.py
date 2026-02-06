import pandas as pd
import numpy as np
import random
import os

# Set seed for reproducibility
np.random.seed(42)

# Define data components
job_titles = ["Data Scientist", "Machine Learning Engineer", "Software Engineer", "Data Analyst", "Data Engineer", "AI Researcher", "MLOps Engineer", "Backend Developer", "Frontend Developer", "Full Stack Developer"]
locations = ["Remote", "New York, NY", "San Francisco, CA", "Austin, TX", "London, UK", "Berlin, Germany", "Bangalore, India", "Toronto, Canada", "Sydney, Australia", "Singapore"]
companies = ["TechCorp", "DataFlow", "AI Innovations", "CloudSystems", "Insightly", "ScaleAI", "FutureLogix", "WebNexus", "AlphaSolutions", "NextGen Tech"]
skills_pool = ["Python", "Machine Learning", "Deep Learning", "SQL", "Tableau", "Power BI", "R", "Java", "Docker", "Kubernetes", "AWS", "Azure", "React", "Node.js", "Spark", "PyTorch", "TensorFlow", "Pandas", "NLP", "Computer Vision"]
experience_levels = ["Entry-level", "Mid-level", "Senior-level", "Executive"]

def generate_skills(title):
    num_skills = random.randint(3, 7)
    base_skills = []
    if "Data" in title or "ML" in title or "AI" in title:
        base_skills = ["Python", "SQL"]
    elif "Developer" in title or "Software" in title:
        base_skills = ["Java", "Docker"]
    
    selected_skills = list(set(base_skills + random.sample(skills_pool, num_skills)))
    return ", ".join(selected_skills[:7])

def calculate_salary(title, exp, location):
    base_salary = 60000
    if "Senior" in exp: base_salary += 40000
    if "Mid" in exp: base_salary += 20000
    if "Executive" in exp: base_salary += 80000
    
    if any(x in title for x in ["AI", "ML", "Machine Learning"]): base_salary += 25000
    if "Data" in title: base_salary += 15000
    
    if "San Francisco" in location or "New York" in location: base_salary *= 1.4
    if "Remote" in location: base_salary *= 1.1
    
    return int(base_salary + np.random.normal(0, 5000))

# Generate dataset
num_rows = 2000
data = []

for _ in range(num_rows):
    title = random.choice(job_titles)
    exp = random.choice(experience_levels)
    loc = random.choice(locations)
    comp = random.choice(companies)
    skills = generate_skills(title)
    salary = calculate_salary(title, exp, loc)
    
    data.append({
        "Job Title": title,
        "Company": comp,
        "Location": loc,
        "Experience Level": exp,
        "Skills": skills,
        "Salary": salary,
        "Post Date": pd.Timestamp.now() - pd.Timedelta(days=random.randint(0, 90))
    })

df = pd.DataFrame(data)

# Save to CSV
os.makedirs("data", exist_ok=True)
df.to_csv("data/job_market_data.csv", index=False)
print("Synthetic dataset generated and saved to data/job_market_data.csv")
