# 🚀 AI-Driven Job Market Intelligence (Full-Stack)

A premium, interactive AI system for job market intelligence. This version transitions from Streamlit to a modern **Full-Stack** architecture for better performance, aesthetics, and hosting flexibility.

## ✨ Features
- **Glassmorphism Dashboard**: Interactive market overview with animated charts.
- **AI Salary Engine**: Real-time salary projection based on multiple market variables.
- **Skill Gap Analysis**: Visualized career path optimization.
- **Docker Ready**: Multi-stage Dockerfile for production deployment.

## 🛠️ Tech Stack
- **Frontend**: React (Vite), Recharts, Lucide, Axios.
- **Backend**: FastAPI, Pydantic, Uvicorn.
- **AI/ML**: Scikit-learn (RandomForest), Joblib.
- **DevOps**: Docker.

## 🏗️ Setup & Installation

1. **Clone & Install Backend**:
   ```bash
   pip install -r requirements.txt
   python src/utils/generate_data.py
   python src/models/train.py
   ```

2. **Run Backend API**:
   ```bash
   uvicorn src.api.main:app --reload
   ```

3. **Setup & Run Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Docker (Optional)**:
   ```bash
   docker build -t ai-job-market .
   docker run -p 8000:8000 ai-job-market
   ```

---
Developed by **G R VIGNESH**
