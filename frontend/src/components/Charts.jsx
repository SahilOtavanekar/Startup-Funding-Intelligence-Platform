import {
    BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
    XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend
} from 'recharts';
import './Charts.css';

// Placeholder data — will be replaced with Supabase / API data in Phase 7
const INDUSTRY_DATA = [
    { name: 'Technology', funding: 42 },
    { name: 'Healthcare', funding: 28 },
    { name: 'Finance', funding: 22 },
    { name: 'Education', funding: 15 },
    { name: 'E-commerce', funding: 18 },
    { name: 'Energy', funding: 12 },
    { name: 'SaaS', funding: 35 },
];

const TREND_DATA = [
    { year: '2019', amount: 120 },
    { year: '2020', amount: 95 },
    { year: '2021', amount: 180 },
    { year: '2022', amount: 210 },
    { year: '2023', amount: 195 },
    { year: '2024', amount: 250 },
];

const PIE_DATA = [
    { name: 'Seed', value: 35 },
    { name: 'Series A', value: 28 },
    { name: 'Series B', value: 20 },
    { name: 'Series C+', value: 17 },
];

const COLORS = ['#6366f1', '#22d3ee', '#34d399', '#fbbf24', '#f87171', '#a78bfa', '#fb923c'];

/**
 * Charts — Recharts-powered visualizations for the Insights page.
 */
function Charts() {
    return (
        <div className="charts-grid">
            {/* Funding by Industry (Bar) */}
            <div className="glass-card chart-card">
                <h4 className="mb-md">💰 Funding by Industry</h4>
                <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={INDUSTRY_DATA}>
                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                        <XAxis dataKey="name" tick={{ fill: '#94a3b8', fontSize: 12 }} />
                        <YAxis tick={{ fill: '#94a3b8', fontSize: 12 }} />
                        <Tooltip
                            contentStyle={{ background: '#1e293b', border: '1px solid rgba(99,102,241,0.2)', borderRadius: 8 }}
                            labelStyle={{ color: '#e2e8f0' }}
                        />
                        <Bar dataKey="funding" radius={[6, 6, 0, 0]}>
                            {INDUSTRY_DATA.map((_, i) => (
                                <Cell key={i} fill={COLORS[i % COLORS.length]} />
                            ))}
                        </Bar>
                    </BarChart>
                </ResponsiveContainer>
            </div>

            {/* Funding Trend (Line) */}
            <div className="glass-card chart-card">
                <h4 className="mb-md">📈 Funding Trend Over Time</h4>
                <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={TREND_DATA}>
                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                        <XAxis dataKey="year" tick={{ fill: '#94a3b8', fontSize: 12 }} />
                        <YAxis tick={{ fill: '#94a3b8', fontSize: 12 }} />
                        <Tooltip
                            contentStyle={{ background: '#1e293b', border: '1px solid rgba(99,102,241,0.2)', borderRadius: 8 }}
                            labelStyle={{ color: '#e2e8f0' }}
                        />
                        <Line type="monotone" dataKey="amount" stroke="#22d3ee" strokeWidth={3} dot={{ r: 5, fill: '#22d3ee' }} />
                    </LineChart>
                </ResponsiveContainer>
            </div>

            {/* Round Distribution (Pie) */}
            <div className="glass-card chart-card">
                <h4 className="mb-md">🎯 Funding Round Distribution</h4>
                <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                        <Pie
                            data={PIE_DATA}
                            cx="50%"
                            cy="50%"
                            outerRadius={100}
                            dataKey="value"
                            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                        >
                            {PIE_DATA.map((_, i) => (
                                <Cell key={i} fill={COLORS[i % COLORS.length]} />
                            ))}
                        </Pie>
                        <Tooltip
                            contentStyle={{ background: '#1e293b', border: '1px solid rgba(99,102,241,0.2)', borderRadius: 8 }}
                        />
                        <Legend wrapperStyle={{ color: '#94a3b8', fontSize: 12 }} />
                    </PieChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}

export default Charts;
