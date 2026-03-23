import { useState, useEffect } from 'react';
import { getStartups } from '../services/api.js';
import './Startups.css';

/**
 * Startups Page — browse the startup dataset.
 */
function Startups() {
    const [startups, setStartups] = useState([]);
    const [allIndustries, setAllIndustries] = useState([]);
    const [loading, setLoading] = useState(true);
    const [totalMatches, setTotalMatches] = useState(0);
    const [totalDataset, setTotalDataset] = useState(0);
    const [error, setError] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');
    const [filterIndustry, setFilterIndustry] = useState('');

    // Fetch Industries once
    useEffect(() => {
        import('../services/api.js').then(api => {
            api.getAvailableIndustries().then(data => setAllIndustries(data));
        });
    }, []);

    // Live search effect
    useEffect(() => {
        const handler = setTimeout(() => {
            fetchData();
        }, 300); // 300ms debounce
        return () => clearTimeout(handler);
    }, [searchTerm, filterIndustry]);

    const fetchData = async () => {
        setLoading(true);
        try {
            const data = await getStartups(searchTerm, filterIndustry);
            setStartups(data.startups || []);
            setTotalMatches(data.total_matches || 0);
            setTotalDataset(data.total_dataset || 0);
        } catch (err) {
            setError('Search failed. Check if backend is alive.');
        } finally {
            setLoading(false);
        }
    };

    // Since we filter on server, 'filtered' is just the 'startups' array now
    const filtered = startups;

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
                Explore all {totalDataset.toLocaleString()} startups in our dataset. Filter by industry or search by name.
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
                        {allIndustries.map((ind) => (
                            <option key={ind} value={ind}>{ind}</option>
                        ))}
                    </select>
                </div>
                <div className="filter-count text-muted">
                    {totalMatches.toLocaleString()} of {totalDataset.toLocaleString()}
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
                                    {startup.total_raised >= 1000000 
                                      ? `$${(startup.total_raised / 1000000).toFixed(1)}M` 
                                      : `$${(startup.total_raised / 1000).toFixed(0)}K`}
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
