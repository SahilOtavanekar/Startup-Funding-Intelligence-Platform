import PredictionForm from '../components/PredictionForm.jsx';
import './Home.css';

/**
 * Home Page — platform overview + prediction tool.
 */
function Home() {
    return (
        <div className="home-page animate-in">
            {/* Hero Section */}
            <section className="hero">
                <h1 className="hero-title">
                    Startup Funding <span className="text-accent">Intelligence</span>
                </h1>
                <p className="hero-subtitle text-muted">
                    AI-powered analytics to predict funding success and explore startup ecosystem trends.
                </p>
            </section>

            {/* Stats Row */}
            <section className="stats-row grid-3 mb-xl">
                <div className="glass-card stat-card">
                    <p className="stat-value text-accent">87%</p>
                    <p className="stat-label text-muted">Model Accuracy</p>
                </div>
                <div className="glass-card stat-card">
                    <p className="stat-value" style={{ color: 'var(--color-success)' }}>2,500+</p>
                    <p className="stat-label text-muted">Startups Analyzed</p>
                </div>
                <div className="glass-card stat-card">
                    <p className="stat-value" style={{ color: 'var(--color-warning)' }}>15+</p>
                    <p className="stat-label text-muted">Industries Covered</p>
                </div>
            </section>

            {/* Prediction Tool */}
            <section>
                <h2 className="mb-lg">Predict Funding Success</h2>
                <PredictionForm />
            </section>
        </div>
    );
}

export default Home;
