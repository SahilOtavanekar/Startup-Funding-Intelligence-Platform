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

export const getAvailableIndustries = async () => {
    const response = await api.get('/api/discovery/industries');
    return response.data;
};

export const getAvailableLocations = async () => {
    const response = await api.get('/api/discovery/locations');
    return response.data;
};

export const getIndustryRoadmap = async (industry) => {
    const response = await api.get('/api/discovery/roadmap', { params: { industry } });
    return response.data;
};

export const getTrendingStartups = async (industry = null, location = null) => {
    const params = {};
    if (industry && industry !== 'All') params.industry = industry;
    if (location && location !== 'All') params.location = location;
    const response = await api.get('/api/discovery/trending', { params });
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
 * Fetch startup records from backend with optional filters.
 * @returns {Promise<Object>}
 */
export const getStartups = async (search = '', industry = '') => {
    const params = {};
    if (search) params.search = search;
    if (industry && industry !== 'All') params.industry = industry;
    const response = await api.get('/startups', { params });
    return response.data;
};

export default api;
