import { useState, useEffect } from 'react'
import axios from 'axios'
import { LayoutDashboard, TrendingUp, Target, BrainCircuit, Github, Cpu } from 'lucide-react'
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, 
  Cell, PieChart, Pie, ScatterChart, Scatter, ZAxis 
} from 'recharts'
import './index.css'

const API_BASE = 'http://localhost:8000'

function App() {
  const [activeTab, setActiveTab] = useState('Overview')
  
  return (
    <div className="app-container">
      <nav className="sidebar glass">
        <div style={{ padding: '0 1rem', marginBottom: '2rem' }}>
          <h2 className="gradient-text" style={{ fontSize: '1.5rem', display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Cpu size={32} /> MarketPulse
          </h2>
        </div>
        
        <div className={`nav-item ${activeTab === 'Overview' ? 'active' : ''}`} onClick={() => setActiveTab('Overview')}>
          <LayoutDashboard size={20} /> Market Overview
        </div>
        <div className={`nav-item ${activeTab === 'Salary' ? 'active' : ''}`} onClick={() => setActiveTab('Salary')}>
          <TrendingUp size={20} /> Salary Predictor
        </div>
        <div className={`nav-item ${activeTab === 'Skills' ? 'active' : ''}`} onClick={() => setActiveTab('Skills')}>
          <Target size={20} /> Skill Optimizer
        </div>
        
        <div style={{ marginTop: 'auto', padding: '1rem' }}>
          <div className="nav-item" style={{ fontSize: '0.8rem', opacity: 0.6 }}>
            <Github size={16} /> @GRVIGNESH
          </div>
        </div>
      </nav>

      <main className="main-content">
        <header style={{ marginBottom: '3rem' }}>
          <h1 style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>
            {activeTab === 'Overview' && "Global Market Intelligence"}
            {activeTab === 'Salary' && "AI Salary Projection"}
            {activeTab === 'Skills' && "Career Path Optimizer"}
          </h1>
          <p style={{ color: 'var(--text-dim)', fontSize: '1.1rem' }}>
            {activeTab === 'Overview' && "Real-time insights from across the tech landscape."}
            {activeTab === 'Salary' && "Estimate your market value using our ML engine."}
            {activeTab === 'Skills' && "Identify skill gaps and bridge your way to your dream role."}
          </p>
        </header>

        {activeTab === 'Overview' && <MarketOverview />}
        {activeTab === 'Salary' && <SalaryPredictor />}
        {activeTab === 'Skills' && <SkillOptimizer />}
      </main>
    </div>
  )
}

function MarketOverview() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    axios.get(`${API_BASE}/market_data`)
      .then(res => {
        setData(res.data)
        setLoading(false)
      })
      .catch(err => console.error(err))
  }, [])

  if (loading) return <div className="glass-card">Loading market insights...</div>

  return (
    <div className="grid">
      <div className="glass-card" style={{ gridColumn: 'span 2' }}>
        <h3>Top Demanded Skills</h3>
        <div style={{ height: 300, marginTop: '1rem' }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data.skill_demand} layout="vertical">
              <XAxis type="number" hide />
              <YAxis dataKey="skill" type="category" width={100} stroke="#94a3b8" />
              <Tooltip 
                contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }}
                itemStyle={{ color: '#8b5cf6' }}
              />
              <Bar dataKey="count" radius={[0, 4, 4, 0]}>
                {data.skill_demand.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={`hsl(${260 + (index * 10)}, 70%, 60%)`} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="glass-card">
        <h3>Average Salary by Role</h3>
        <div style={{ height: 300, marginTop: '1rem' }}>
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data.job_salary}
                dataKey="salary"
                nameKey="title"
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={80}
                paddingAngle={5}
              >
                {data.job_salary.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={`hsl(${180 + (index * 15)}, 70%, 50%)`} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="glass-card" style={{ gridColumn: 'span 3' }}>
        <h3>Experience vs Compensation</h3>
        <div style={{ height: 300, marginTop: '1rem' }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data.exp_salary}>
              <XAxis dataKey="level" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip contentStyle={{ background: '#1e293b', border: '1px solid #334155' }} />
              <Bar dataKey="salary" fill="var(--primary)" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}

function SalaryPredictor() {
  const [form, setForm] = useState({ job_title: 'Data Scientist', location: 'Remote', experience_level: 'Mid-level', skills: [] })
  const [prediction, setPrediction] = useState(null)
  const [options, setOptions] = useState({ titles: [], locations: [], experiences: [], skills: [] })

  useEffect(() => {
    // Generate some default options for now to avoid complexity of another endpoint
    setOptions({
      titles: ["Data Scientist", "Machine Learning Engineer", "Software Engineer", "Data Analyst", "Data Engineer", "AI Researcher", "MLOps Engineer", "Backend Developer", "Frontend Developer", "Full Stack Developer"],
      locations: ["Remote", "New York, NY", "San Francisco, CA", "Austin, TX", "London, UK", "Berlin, Germany", "Bangalore, India", "Toronto, Canada", "Sydney, Australia", "Singapore"],
      experiences: ["Entry-level", "Mid-level", "Senior-level", "Executive"],
      skills: ["Python", "SQL", "Deep Learning", "Docker", "Kubernetes", "AWS", "React", "PyTorch"]
    })
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const res = await axios.post(`${API_BASE}/predict_salary`, form)
      setPrediction(res.data.predicted_salary)
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <div className="glass-card" style={{ maxWidth: 800 }}>
      <form onSubmit={handleSubmit}>
        <div className="grid">
          <div className="form-group">
            <label>Job Title</label>
            <select value={form.job_title} onChange={e => setForm({...form, job_title: e.target.value})}>
              {options.titles.map(t => <option key={t} value={t}>{t}</option>)}
            </select>
          </div>
          <div className="form-group">
            <label>Location</label>
            <select value={form.location} onChange={e => setForm({...form, location: e.target.value})}>
              {options.locations.map(l => <option key={l} value={l}>{l}</option>)}
            </select>
          </div>
          <div className="form-group">
            <label>Experience Level</label>
            <select value={form.experience_level} onChange={e => setForm({...form, experience_level: e.target.value})}>
              {options.experiences.map(ex => <option key={ex} value={ex}>{ex}</option>)}
            </select>
          </div>
        </div>
        
        <button type="submit" className="btn-primary" style={{ marginTop: '1rem' }}>Predict Market Value</button>
      </form>

      {prediction && (
        <div className="glass-card" style={{ marginTop: '2rem', textAlign: 'center', borderColor: 'var(--primary)' }}>
          <h2 style={{ fontSize: '1rem', color: 'var(--text-dim)' }}>Estimated Annual Salary</h2>
          <h1 className="gradient-text" style={{ fontSize: '3rem' }}>
            ${prediction.toLocaleString()}
          </h1>
        </div>
      )}
    </div>
  )
}

function SkillOptimizer() {
  const [targetJob, setTargetJob] = useState('Data Scientist')
  const [currentSkills, setCurrentSkills] = useState([])
  const [results, setResults] = useState(null)
  
  const titles = ["Data Scientist", "Machine Learning Engineer", "Software Engineer", "Data Analyst", "Data Engineer", "AI Researcher", "MLOps Engineer", "Backend Developer", "Frontend Developer", "Full Stack Developer"]
  const allSkills = ["Python", "SQL", "Machine Learning", "Deep Learning", "React", "Node.js", "Docker", "Kubernetes", "AWS", "Azure", "Spark", "PyTorch", "TensorFlow", "Pandas", "Tableau", "Power BI"]

  const generate = async () => {
    try {
      const res = await axios.post(`${API_BASE}/recommend_skills`, {
        target_job: targetJob,
        current_skills: currentSkills
      })
      setResults(res.data)
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      <div className="glass-card">
        <div className="grid">
          <div className="form-group">
            <label>Target Role</label>
            <select value={targetJob} onChange={e => setTargetJob(e.target.value)}>
              {titles.map(t => <option key={t} value={t}>{t}</option>)}
            </select>
          </div>
          <div className="form-group" style={{ gridColumn: 'span 2' }}>
            <label>Select Your Current Skills</label>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', marginTop: '0.5rem' }}>
              {allSkills.map(skill => (
                <div 
                  key={skill}
                  onClick={() => {
                    if (currentSkills.includes(skill)) setCurrentSkills(currentSkills.filter(s => s !== skill))
                    else setCurrentSkills([...currentSkills, skill])
                  }}
                  style={{
                    padding: '0.4rem 0.8rem',
                    borderRadius: '20px',
                    fontSize: '0.85rem',
                    cursor: 'pointer',
                    background: currentSkills.includes(skill) ? 'var(--primary)' : 'rgba(255,255,255,0.05)',
                    border: '1px solid var(--glass-border)',
                    transition: 'all 0.2s'
                  }}
                >
                  {skill}
                </div>
              ))}
            </div>
          </div>
        </div>
        <button onClick={generate} className="btn-primary" style={{ marginTop: '1.5rem' }}>Analyze Skill Gap</button>
      </div>

      {results && (
        <div className="grid">
          <div className="glass-card">
            <h3>Top Recommendations</h3>
            <div style={{ marginTop: '1rem', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {results.recommended_skills.map((s, i) => (
                <div key={s} style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <div style={{ width: 8, height: 8, borderRadius: '50%', background: 'var(--accent)' }} />
                  {s}
                </div>
              ))}
            </div>
          </div>
          <div className="glass-card" style={{ gridColumn: 'span 2' }}>
            <h3>Market Standard for {targetJob}</h3>
            <p style={{ color: 'var(--text-dim)', marginTop: '0.5rem' }}>Core skills found in 80%+ of top-tier postings</p>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', marginTop: '1rem' }}>
              {results.top_market_skills.map(s => (
                <span key={s} className="glass" style={{ padding: '4px 12px', borderRadius: '12px', fontSize: '0.9rem' }}>{s}</span>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default App
