import { useState } from 'react';
import { predictFunding } from '../services/api.js';
import './PredictionForm.css';

const INDUSTRIES = [
    'Technology', 'Healthcare', 'Finance', 'Education', 'E-commerce',
    'Energy', 'Real Estate', 'Food & Beverage', 'Transportation', 'Media',
    'Agriculture', 'Manufacturing', 'Retail', 'Gaming', 'SaaS',
];

/**
 * PredictionForm — users input startup parameters and get a funding success probability.
 */
function PredictionForm() {
    const [form, setForm] = useState({
        industry: '',
        team_size: '',
        startup_age: '',
        investor_count: '',
    });
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const payload = {
                industry: form.industry,
                team_size: parseInt(form.team_size, 10),
                startup_age: parseInt(form.startup_age, 10),
                investor_count: parseInt(form.investor_count, 10),
            };
            const data = await predictFunding(payload);
            setResult(data);
        } catch (err) {
            setError(err.response?.data?.detail || 'Prediction failed. Is the backend running?');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="glass-card prediction-card">
            <form onSubmit={handleSubmit} className="prediction-form">
                <div className="form-grid">
                    <div className="form-group">
                        <label className="form-label" htmlFor="industry">Industry</label>
                        <select
                            id="industry"
                            name="industry"
                            className="form-select"
                            value={form.industry}
                            onChange={handleChange}
                            required
                        >
                            <option value="">Select industry…</option>
                            {INDUSTRIES.map((ind) => (
                                <option key={ind} value={ind}>{ind}</option>
                            ))}
                        </select>
                    </div>

                    <div className="form-group">
                        <label className="form-label" htmlFor="team_size">Team Size</label>
                        <input
                            id="team_size"
                            name="team_size"
                            type="number"
                            className="form-input"
                            placeholder="e.g. 12"
                            min="1"
                            value={form.team_size}
                            onChange={handleChange}
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label className="form-label" htmlFor="startup_age">Startup Age (years)</label>
                        <input
                            id="startup_age"
                            name="startup_age"
                            type="number"
                            className="form-input"
                            placeholder="e.g. 3"
                            min="0"
                            value={form.startup_age}
                            onChange={handleChange}
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label className="form-label" htmlFor="investor_count">Investor Count</label>
                        <input
                            id="investor_count"
                            name="investor_count"
                            type="number"
                            className="form-input"
                            placeholder="e.g. 5"
                            min="0"
                            value={form.investor_count}
                            onChange={handleChange}
                            required
                        />
                    </div>
                </div>

                <button type="submit" className="btn btn-primary predict-btn" disabled={loading}>
                    {loading ? 'Analyzing…' : '🔮 Predict Funding Success'}
                </button>
            </form>

            {/* Result */}
            {result && (
                <div className="prediction-result animate-in">
                    <p className="result-label text-muted">Funding Success Probability</p>
                    <p className="result-value">
                        {(result.funding_success_probability * 100).toFixed(1)}%
                    </p>
                </div>
            )}

            {/* Error */}
            {error && (
                <div className="prediction-error animate-in">
                    <p className="text-danger">{error}</p>
                </div>
            )}
        </div>
    );
}

export default PredictionForm;
