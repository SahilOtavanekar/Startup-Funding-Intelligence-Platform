import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getIndustryTrends } from '../services/api.js';
import './Home.css';

/**
 * Home Page — platform overview + roadmap link.
 */
function Home() {
    const [stats, setStats] = useState({
        total_startups: '—',
        total_funded: '—',
        avg_funding: '—',
        success_rate: '—',
        total_industries: '—',
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
                    total_industries: `${data.total_industries}+`,
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
                <div className="hero-badge">🚀 Data-Driven Analytics Platform</div>
                <h1 className="hero-title">
                    Startup Funding <span className="text-accent">Intelligence</span>
                </h1>
                <p className="hero-subtitle text-muted">
                    Explore industry benchmarks, build strategic funding roadmaps,
                    and uncover insights across the global startup ecosystem.
                </p>
                <Link to="/trending" className="btn btn-primary mt-md" style={{ display: 'inline-block', padding: '0.8rem 2rem', backgroundColor: 'var(--accent-color)', color: 'black', textDecoration: 'none', borderRadius: '4px', fontWeight: 'bold' }}>
                    🔥 Top Growing Startups
                </Link>
            </section>

            {/* Stats Row */}
            <section className="stats-row grid-4 mb-xl mt-xl">
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
                    <p className="stat-value" style={{ color: '#a78bfa' }}>{stats.total_industries}</p>
                    <p className="stat-label text-muted">Industries Covered</p>
                </div>
            </section>

            {/* Features Section */}
            <section className="features-section mt-xl">
                <h2 className="mb-lg">Platform <span className="text-accent">Capabilities</span></h2>
                <div className="features-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1rem' }}>
                    <div className="glass-card feature-card">
                        <div className="feature-icon">🔥</div>
                        <h4>Top Trending Startups</h4>
                        <p className="text-muted">Discover companies with massive operational momentum based on their funding-to-age velocity.</p>
                    </div>
                    <div className="glass-card feature-card">
                        <div className="feature-icon">📈</div>
                        <h4>Trend Analysis</h4>
                        <p className="text-muted">Explore funding trends across industries, geographies, and time periods with interactive charts.</p>
                    </div>
                    <div className="glass-card feature-card">
                        <div className="feature-icon">💼</div>
                        <h4>Strategic Benchmarks</h4>
                        <p className="text-muted">Analyze {stats.total_startups}+ real-world funding events to determine typical team sizes and funding milestones.</p>
                    </div>
                    <div className="glass-card feature-card">
                        <div className="feature-icon">⚡</div>
                        <h4>Real-time API</h4>
                        <p className="text-muted">FastAPI backend serving aggregated insights with sub-second response times and auto-generated docs.</p>
                    </div>
                </div>
            </section>
        </div>
    );
}

export default Home;
