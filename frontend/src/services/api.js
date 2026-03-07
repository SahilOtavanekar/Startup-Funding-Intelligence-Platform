import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const API_KEY = import.meta.env.VITE_API_KEY || 'startup-intelligence-local-dev-key';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
        'x-api-key': API_KEY,
    },
});

/**
 * Predict funding success probability for a startup.
 * @param {Object} data - { industry, team_size, startup_age, investor_count }
 * @returns {Promise<Object>} - { funding_success_probability, feature_importance }
 */
export const predictFunding = async (data) => {
    const response = await api.post('/predict', data);
    return response.data;
};

/**
 * Fetch industry trends (funding distribution & growth).
 * @returns {Promise<Object>}
 */
export const getIndustryTrends = async () => {
    const response = await api.get('/industry-trends');
    return response.data;
};

/**
 * Fetch startup records from backend.
 * @returns {Promise<Array>}
 */
export const getStartups = async () => {
    const response = await api.get('/startups');
    return response.data;
};

export default api;
