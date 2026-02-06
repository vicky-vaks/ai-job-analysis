# AI-Driven Job Market Intelligence & Salary Optimization System

This project is an end-to-end AI system that analyzes job market data to identify in-demand skills, predict salaries, and recommend skill paths for job seekers.

## 🚀 Features
- **Market Overview**: Interactive visualizations of skill demand and salary distributions.
- **Salary Predictor**: ML model to estimate market value based on title, location, and skills.
- **Skill Path Optimizer**: Identifies skill gaps and recommends learning paths for target roles.

## 🛠️ Tech Stack
- **Frontend**: Streamlit
- **Backend**: FastAPI
- **ML**: Scikit-learn (RandomForest), Joblib
- **Data**: Pandas, Numpy, Plotly

## 🏗️ Setup & Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd ai-job-market-project
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate Data & Train Models**:
   ```bash
   python src/utils/generate_data.py
   python src/models/train.py
   ```

4. **Run the API Backend**:
   ```bash
   python src/api/main.py
   ```

5. **Run the Dashboard**:
   ```bash
   streamlit run dashboard/app.py
   ```

Developed by **G R VIGNESH**
