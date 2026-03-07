import { useState, useEffect } from 'react';
import PredictionForm from '../components/PredictionForm.jsx';
import { getIndustryTrends } from '../services/api.js';
import './Home.css';

/**
 * Home Page — platform overview + prediction tool.
 */
function Home() {
    const [stats, setStats] = useState({
        total_startups: '—',
        total_funded: '—',
        avg_funding: '—',
        success_rate: '—',
    });

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const data = await getIndustryTrends();
                const rate = data.total_startups > 0
                    ? ((data.total_funded / data.total_startups) * 100).toFixed(0)
                    : 0;
                setStats({
                    total_startups: data.total_startups?.toLocaleString() || '—',
                    total_funded: data.total_funded?.toLocaleString() || '—',
                    avg_funding: `$${data.avg_funding}M`,
                    success_rate: `${rate}%`,
                });
            } catch {
                // Use defaults if API unavailable
            }
        };
        fetchStats();
    }, []);

    return (
        <div className="home-page animate-in">
            {/* Hero Section */}
            <section className="hero">
                <div className="hero-badge">🚀 AI-Powered Analytics Platform</div>
                <h1 className="hero-title">
                    Startup Funding <span className="text-accent">Intelligence</span>
                </h1>
                <p className="hero-subtitle text-muted">
                    Predict funding success probability, explore industry trends,
                    and uncover insights across the startup ecosystem — powered by machine learning.
                </p>
            </section>

            {/* Stats Row */}
            <section className="stats-row grid-4 mb-xl">
                <div className="glass-card stat-card">
                    <div className="stat-icon">📊</div>
                    <p className="stat-value text-accent">{stats.success_rate}</p>
                    <p className="stat-label text-muted">Avg Success Rate</p>
                </div>
                <div className="glass-card stat-card">
                    <div className="stat-icon">🏢</div>
                    <p className="stat-value" style={{ color: 'var(--color-success)' }}>{stats.total_startups}</p>
                    <p className="stat-label text-muted">Startups Analyzed</p>
                </div>
                <div className="glass-card stat-card">
                    <div className="stat-icon">💰</div>
                    <p className="stat-value" style={{ color: 'var(--color-warning)' }}>{stats.avg_funding}</p>
                    <p className="stat-label text-muted">Avg Funding</p>
                </div>
                <div className="glass-card stat-card">
                    <div className="stat-icon">🌍</div>
                    <p className="stat-value" style={{ color: '#a78bfa' }}>15+</p>
                    <p className="stat-label text-muted">Industries Covered</p>
                </div>
            </section>

            {/* Prediction Tool */}
            <section>
                <div className="section-header">
                    <h2>Predict Funding Success</h2>
                    <p className="text-muted">
                        Input your startup parameters and our XGBoost model will estimate
                        the probability of securing funding.
                    </p>
                </div>
                <PredictionForm />
            </section>

            {/* Features Section */}
            <section className="features-section">
                <h2 className="mb-lg">Platform <span className="text-accent">Capabilities</span></h2>
                <div className="features-grid">
                    <div className="glass-card feature-card">
                        <div className="feature-icon">🔮</div>
                        <h4>ML Predictions</h4>
                        <p className="text-muted">XGBoost-powered predictions with SHAP explainability for transparent, data-driven insights.</p>
                    </div>
                    <div className="glass-card feature-card">
                        <div className="feature-icon">📈</div>
                        <h4>Trend Analysis</h4>
                        <p className="text-muted">Explore funding trends across industries, geographies, and time periods with interactive charts.</p>
                    </div>
                    <div className="glass-card feature-card">
                        <div className="feature-icon">🧪</div>
                        <h4>Experiment Tracking</h4>
                        <p className="text-muted">MLflow integration for reproducible experiments, hyperparameter logging, and model versioning.</p>
                    </div>
                    <div className="glass-card feature-card">
                        <div className="feature-icon">⚡</div>
                        <h4>Real-time API</h4>
                        <p className="text-muted">FastAPI backend serving predictions with sub-second response times and auto-generated docs.</p>
                    </div>
                </div>
            </section>
        </div>
    );
}

export default Home;
