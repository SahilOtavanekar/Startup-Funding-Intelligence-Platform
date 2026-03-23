import { useState, useEffect } from 'react';
import { getAvailableIndustries, getAvailableLocations, getTrendingStartups } from '../services/api.js';

/**
 * Trending Page — Top growing startups leaderboard.
 */
function Trending() {
    const [industries, setIndustries] = useState(['All']);
    const [locations, setLocations] = useState(['All']);
    const [selectedIndustry, setSelectedIndustry] = useState('All');
    const [selectedLocation, setSelectedLocation] = useState('All');
    const [startups, setStartups] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchFilters = async () => {
            try {
                const [indData, locData] = await Promise.all([
                    getAvailableIndustries(),
                    getAvailableLocations()
                ]);
                setIndustries(['All', ...indData]);
                setLocations(['All', ...locData]);
            } catch (err) {
                console.error("Failed to load filters", err);
            }
        };
        fetchFilters();
    }, []);

    useEffect(() => {
        const fetchTrending = async () => {
            setLoading(true);
            setError(null);
            try {
                const data = await getTrendingStartups(selectedIndustry, selectedLocation);
                setStartups(data);
            } catch (err) {
                console.error("Failed to fetch trending", err);
                setError("Failed to fetch trending data");
            } finally {
                setLoading(false);
            }
        };

        fetchTrending();
    }, [selectedIndustry, selectedLocation]);

    return (
        <div className="predict-page animate-in" style={{ maxWidth: 1000 }}>
            <h1 className="mb-md">
                Top Growing <span className="text-accent">Startups</span>
            </h1>
            <p className="text-muted mb-xl" style={{ maxWidth: 650 }}>
                Discover high-potential startups exhibiting maximum funding momentum. Ranked by total funding raised relative to their operational age.
            </p>

            <div className="glass-card mb-lg" style={{ padding: 'var(--space-md)', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                <div>
                    <label className="text-muted" style={{ display: 'block', marginBottom: '0.5rem', fontSize: '0.85rem' }}>
                        INDUSTRY
                    </label>
                    <select 
                        style={{
                            width: '100%', padding: '0.8rem', borderRadius: '4px',
                            backgroundColor: 'rgba(255, 255, 255, 0.05)',
                            border: '1px solid rgba(255, 255, 255, 0.1)',
                            color: 'var(--text-primary)', fontSize: '1rem', outline: 'none'
                        }}
                        value={selectedIndustry}
                        onChange={(e) => setSelectedIndustry(e.target.value)}
                    >
                        {industries.map((ind) => (
                            <option key={ind} value={ind} style={{ color: 'black' }}>{ind}</option>
                        ))}
                    </select>
                </div>
                <div>
                    <label className="text-muted" style={{ display: 'block', marginBottom: '0.5rem', fontSize: '0.85rem' }}>
                        LOCATION
                    </label>
                    <select 
                        style={{
                            width: '100%', padding: '0.8rem', borderRadius: '4px',
                            backgroundColor: 'rgba(255, 255, 255, 0.05)',
                            border: '1px solid rgba(255, 255, 255, 0.1)',
                            color: 'var(--text-primary)', fontSize: '1rem', outline: 'none'
                        }}
                        value={selectedLocation}
                        onChange={(e) => setSelectedLocation(e.target.value)}
                    >
                        {locations.map((loc) => (
                            <option key={loc} value={loc} style={{ color: 'black' }}>{loc}</option>
                        ))}
                    </select>
                </div>
            </div>

            {loading && <p className="text-muted">Analyzing operational momentum...</p>}
            {error && <p style={{ color: 'red' }}>{error}</p>}

            {!loading && startups.length > 0 && (
                <div className="glass-card table-container">
                    <table className="startup-table" style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse' }}>
                        <thead>
                            <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
                                <th style={{ padding: '1rem' }}>Rank</th>
                                <th style={{ padding: '1rem' }}>Startup</th>
                                <th style={{ padding: '1rem' }}>Sector & Hub</th>
                                <th style={{ padding: '1rem' }}>Age</th>
                                <th style={{ padding: '1rem' }}>Raised</th>
                                <th style={{ padding: '1rem' }}>Momentum</th>
                            </tr>
                        </thead>
                        <tbody>
                            {startups.map((startup, index) => (
                                <tr key={index} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                                    <td style={{ padding: '1rem' }}>
                                        <span style={{ 
                                            display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
                                            width: '28px', height: '28px', borderRadius: '50%', 
                                            backgroundColor: index < 3 ? 'var(--accent-color)' : 'rgba(255,255,255,0.1)', 
                                            color: index < 3 ? 'black' : 'white', 
                                            fontWeight: 700, fontSize: '0.9rem'
                                        }}>
                                            {index + 1}
                                        </span>
                                    </td>
                                    <td style={{ padding: '1rem', fontWeight: 600 }}>{startup.startup_name}</td>
                                    <td style={{ padding: '1rem' }}>
                                        <div style={{ fontSize: '0.9rem', color: 'var(--accent-color)' }}>{startup.industry}</div>
                                        <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>📍 {startup.location}</div>
                                    </td>
                                    <td style={{ padding: '1rem', color: 'var(--text-muted)' }}>{startup.startup_age} yrs</td>
                                    <td style={{ padding: '1rem', fontWeight: 'bold', color: 'var(--color-success)' }}>{startup.total_raised}</td>
                                    <td style={{ padding: '1rem' }}>
                                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                            <div style={{ width: '100px', height: '8px', background: 'rgba(255,255,255,0.1)', borderRadius: '4px', overflow: 'hidden' }}>
                                                <div style={{ width: `${startup.momentum_score}%`, height: '100%', background: 'var(--accent-color)' }}></div>
                                            </div>
                                            <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>{startup.momentum_score}</span>
                                        </div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
            
            {!loading && startups.length === 0 && (
                <p className="text-muted">No trending startups found in this category.</p>
            )}
        </div>
    );
}

export default Trending;
