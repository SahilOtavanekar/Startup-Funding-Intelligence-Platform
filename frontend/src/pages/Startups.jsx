import { useState, useEffect } from 'react';
import { getStartups } from '../services/api.js';
import './Startups.css';

/**
 * Startups Page — browse the startup dataset.
 */
function Startups() {
    const [startups, setStartups] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');
    const [filterIndustry, setFilterIndustry] = useState('');

    useEffect(() => {
        const fetchStartups = async () => {
            try {
                const data = await getStartups();
                setStartups(data.startups || []);
            } catch (err) {
                setError('Failed to load startups. Is the backend running?');
            } finally {
                setLoading(false);
            }
        };
        fetchStartups();
    }, []);

    // Unique industries for filter
    const industries = [...new Set(startups.map((s) => s.industry))].sort();

    // Filtered data
    const filtered = startups.filter((s) => {
        const matchesSearch = s.startup_name?.toLowerCase().includes(searchTerm.toLowerCase())
            || s.location?.toLowerCase().includes(searchTerm.toLowerCase());
        const matchesIndustry = filterIndustry === '' || s.industry === filterIndustry;
        return matchesSearch && matchesIndustry;
    });

    if (loading) {
        return (
            <div className="startups-page animate-in" style={{ textAlign: 'center', paddingTop: '4rem' }}>
                <div className="loading-spinner"></div>
                <p className="text-muted" style={{ marginTop: '1rem' }}>Loading startups…</p>
            </div>
        );
    }

    return (
        <div className="startups-page animate-in">
            <h1 className="mb-md">
                Startup <span className="text-accent">Database</span>
            </h1>
            <p className="text-muted mb-xl" style={{ maxWidth: 550 }}>
                Explore {startups.length} startups in our dataset. Filter by industry or search by name.
            </p>

            {error && (
                <div className="glass-card" style={{ marginBottom: 'var(--space-lg)', padding: 'var(--space-lg)' }}>
                    <p className="text-danger">⚠️ {error}</p>
                </div>
            )}

            {/* Filters */}
            <div className="startup-filters">
                <div className="form-group">
                    <input
                        type="text"
                        className="form-input"
                        placeholder="🔍 Search by name or location…"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
                <div className="form-group">
                    <select
                        className="form-select"
                        value={filterIndustry}
                        onChange={(e) => setFilterIndustry(e.target.value)}
                    >
                        <option value="">All Industries</option>
                        {industries.map((ind) => (
                            <option key={ind} value={ind}>{ind}</option>
                        ))}
                    </select>
                </div>
                <div className="filter-count text-muted">
                    {filtered.length} of {startups.length}
                </div>
            </div>

            {/* Table */}
            <div className="glass-card table-container">
                <table className="startup-table">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Industry</th>
                            <th>Location</th>
                            <th>Founded</th>
                            <th>Team</th>
                            <th>Investors</th>
                            <th>Raised</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filtered.slice(0, 50).map((startup, i) => (
                            <tr key={i}>
                                <td className="startup-name">{startup.startup_name}</td>
                                <td>
                                    <span className="industry-badge">{startup.industry}</span>
                                </td>
                                <td className="text-muted">{startup.location}</td>
                                <td>{startup.founded_year}</td>
                                <td>{startup.team_size}</td>
                                <td>{startup.investor_count}</td>
                                <td className="funding-amount">
                                    ${(startup.total_raised / 1_000_000).toFixed(1)}M
                                </td>
                                <td>
                                    <span className={`status-badge ${startup.funding_success ? 'success' : 'pending'}`}>
                                        {startup.funding_success ? '✅ Funded' : '⏳ Pending'}
                                    </span>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                {filtered.length > 50 && (
                    <p className="text-muted" style={{ textAlign: 'center', padding: 'var(--space-md)', fontSize: '0.85rem' }}>
                        Showing first 50 of {filtered.length} results
                    </p>
                )}
            </div>
        </div>
    );
}

export default Startups;
