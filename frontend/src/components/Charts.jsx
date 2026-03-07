import { useState, useEffect } from 'react';
import {
    BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, AreaChart, Area,
    XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend
} from 'recharts';
import { getIndustryTrends } from '../services/api.js';
import './Charts.css';

const COLORS = ['#6366f1', '#22d3ee', '#34d399', '#fbbf24', '#f87171', '#a78bfa', '#fb923c', '#ec4899', '#14b8a6', '#f97316'];

// Custom tooltip for dark theme
const CustomTooltip = ({ active, payload, label }) => {
    if (!active || !payload || !payload.length) return null;
    return (
        <div className="chart-tooltip">
            <p className="tooltip-label">{label}</p>
            {payload.map((entry, i) => (
                <p key={i} style={{ color: entry.color || '#e2e8f0' }}>
                    {entry.name}: {typeof entry.value === 'number' ? entry.value.toLocaleString() : entry.value}
                </p>
            ))}
        </div>
    );
};

/**
 * Charts — Recharts-powered visualizations for the Insights page.
 * Fetches live data from the analytics API.
 */
function Charts() {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const result = await getIndustryTrends();
                setData(result);
            } catch (err) {
                console.error('Failed to fetch analytics:', err);
                setError('Failed to load analytics data. Is the backend running?');
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    if (loading) {
        return (
            <div className="charts-loading">
                <div className="loading-spinner"></div>
                <p className="text-muted">Loading analytics data…</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="charts-error glass-card">
                <p className="text-danger">⚠️ {error}</p>
                <p className="text-muted" style={{ fontSize: '0.85rem', marginTop: '0.5rem' }}>
                    Start the backend: <code>uvicorn app.main:app --reload</code>
                </p>
            </div>
        );
    }

    const {
        industry_funding = [],
        success_rate = [],
        year_funding = [],
        round_distribution = [],
        location_distribution = [],
        team_by_success = [],
        total_startups = 0,
        total_funded = 0,
        avg_funding = 0,
    } = data || {};

    return (
        <div className="charts-container">
            {/* Summary Stats Row */}
            <div className="chart-stats-row">
                <div className="glass-card stat-mini">
                    <span className="stat-mini-value text-accent">{total_startups}</span>
                    <span className="stat-mini-label text-muted">Total Startups</span>
                </div>
                <div className="glass-card stat-mini">
                    <span className="stat-mini-value" style={{ color: '#34d399' }}>{total_funded}</span>
                    <span className="stat-mini-label text-muted">Successfully Funded</span>
                </div>
                <div className="glass-card stat-mini">
                    <span className="stat-mini-value" style={{ color: '#fbbf24' }}>${avg_funding}M</span>
                    <span className="stat-mini-label text-muted">Avg Funding</span>
                </div>
                <div className="glass-card stat-mini">
                    <span className="stat-mini-value" style={{ color: '#a78bfa' }}>
                        {total_startups > 0 ? ((total_funded / total_startups) * 100).toFixed(0) : 0}%
                    </span>
                    <span className="stat-mini-label text-muted">Success Rate</span>
                </div>
            </div>

            {/* Charts Grid */}
            <div className="charts-grid">
                {/* Funding by Industry (Bar) */}
                <div className="glass-card chart-card">
                    <h4 className="chart-title">💰 Funding by Industry</h4>
                    <p className="chart-subtitle text-muted">Total funding raised (in millions $)</p>
                    <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={industry_funding}>
                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                            <XAxis dataKey="name" tick={{ fill: '#94a3b8', fontSize: 11 }} angle={-20} textAnchor="end" height={60} />
                            <YAxis tick={{ fill: '#94a3b8', fontSize: 12 }} />
                            <Tooltip content={<CustomTooltip />} />
                            <Bar dataKey="funding" name="Funding ($M)" radius={[6, 6, 0, 0]}>
                                {industry_funding.map((_, i) => (
                                    <Cell key={i} fill={COLORS[i % COLORS.length]} />
                                ))}
                            </Bar>
                        </BarChart>
                    </ResponsiveContainer>
                </div>

                {/* Success Rate by Industry (Bar) */}
                <div className="glass-card chart-card">
                    <h4 className="chart-title">🎯 Success Rate by Industry</h4>
                    <p className="chart-subtitle text-muted">Percentage of startups that received funding</p>
                    <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={success_rate} layout="vertical">
                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                            <XAxis type="number" tick={{ fill: '#94a3b8', fontSize: 12 }} unit="%" />
                            <YAxis dataKey="name" type="category" tick={{ fill: '#94a3b8', fontSize: 11 }} width={110} />
                            <Tooltip content={<CustomTooltip />} />
                            <Bar dataKey="success_rate" name="Success Rate (%)" radius={[0, 6, 6, 0]} fill="#34d399" />
                        </BarChart>
                    </ResponsiveContainer>
                </div>

                {/* Funding Trend Over Time (Area) */}
                <div className="glass-card chart-card chart-wide">
                    <h4 className="chart-title">📈 Funding Trend Over Time</h4>
                    <p className="chart-subtitle text-muted">Total funding raised by year (in millions $)</p>
                    <ResponsiveContainer width="100%" height={300}>
                        <AreaChart data={year_funding}>
                            <defs>
                                <linearGradient id="colorFunding" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#22d3ee" stopOpacity={0.3} />
                                    <stop offset="95%" stopColor="#22d3ee" stopOpacity={0} />
                                </linearGradient>
                            </defs>
                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                            <XAxis dataKey="year" tick={{ fill: '#94a3b8', fontSize: 12 }} />
                            <YAxis tick={{ fill: '#94a3b8', fontSize: 12 }} />
                            <Tooltip content={<CustomTooltip />} />
                            <Area type="monotone" dataKey="amount" name="Funding ($M)" stroke="#22d3ee" strokeWidth={3} fill="url(#colorFunding)" dot={{ r: 4, fill: '#22d3ee' }} />
                        </AreaChart>
                    </ResponsiveContainer>
                </div>

                {/* Round Distribution (Pie) */}
                <div className="glass-card chart-card">
                    <h4 className="chart-title">🥧 Funding Round Distribution</h4>
                    <p className="chart-subtitle text-muted">Number of startups by funding stage</p>
                    <ResponsiveContainer width="100%" height={300}>
                        <PieChart>
                            <Pie
                                data={round_distribution}
                                cx="50%"
                                cy="50%"
                                outerRadius={100}
                                innerRadius={40}
                                dataKey="value"
                                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                            >
                                {round_distribution.map((_, i) => (
                                    <Cell key={i} fill={COLORS[i % COLORS.length]} />
                                ))}
                            </Pie>
                            <Tooltip content={<CustomTooltip />} />
                            <Legend wrapperStyle={{ color: '#94a3b8', fontSize: 12 }} />
                        </PieChart>
                    </ResponsiveContainer>
                </div>

                {/* Top Locations (Bar) */}
                <div className="glass-card chart-card">
                    <h4 className="chart-title">🌍 Top Startup Locations</h4>
                    <p className="chart-subtitle text-muted">Number of startups by city</p>
                    <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={location_distribution} layout="vertical">
                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                            <XAxis type="number" tick={{ fill: '#94a3b8', fontSize: 12 }} />
                            <YAxis dataKey="name" type="category" tick={{ fill: '#94a3b8', fontSize: 10 }} width={130} />
                            <Tooltip content={<CustomTooltip />} />
                            <Bar dataKey="count" name="Startups" radius={[0, 6, 6, 0]} fill="#a78bfa" />
                        </BarChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>
    );
}

export default Charts;
