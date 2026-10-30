const axios = require('axios');
const path = require('path');
require('dotenv').config({ path: path.resolve(__dirname, '../../../.env') });

const AI_SERVICE_URL = process.env.AI_SERVICE_URL || 'http://127.0.0.1:8000';

const aiClient = axios.create({
  baseURL: AI_SERVICE_URL,
  timeout: 90000, // 90s timeout for complete multi-agent pipeline
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Pings the Python AI Service health check endpoint
 */
async function checkAIHealth() {
  try {
    const res = await aiClient.get('/ai/health');
    return { status: 'connected', data: res.data };
  } catch (error) {
    return { status: 'disconnected', error: error.message };
  }
}

/**
 * Forwards travel request to Python FastAPI multi-agent engine
 */
async function generateTripPlan(payload) {
  try {
    const response = await aiClient.post('/ai/plan-trip', payload);
    return response.data;
  } catch (error) {
    if (error.response) {
      const detail = error.response.data?.detail || JSON.stringify(error.response.data);
      throw new Error(`AI Engine error (${error.response.status}): ${detail}`);
    } else if (error.code === 'ECONNREFUSED' || error.request) {
      throw new Error('AI Service is not reachable. Please ensure the Python FastAPI service is running on port 8000.');
    } else {
      throw new Error(`Trip generation failed: ${error.message}`);
    }
  }
}

/**
 * Retrieves past trips
 */
async function fetchSavedTrips(limit = 30, userId = null) {
  try {
    const params = { limit };
    if (userId) params.user_id = userId;
    const response = await aiClient.get('/ai/trips', { params });
    return response.data;
  } catch (error) {
    throw new Error(`Failed to fetch trips: ${error.message}`);
  }
}

/**
 * Retrieves trip details by id
 */
async function fetchTripById(tripId) {
  try {
    const response = await aiClient.get(`/ai/trips/${tripId}`);
    return response.data;
  } catch (error) {
    if (error.response?.status === 404) {
      throw new Error(`Trip ${tripId} not found`);
    }
    throw new Error(`Failed to fetch trip ${tripId}: ${error.message}`);
  }
}

/**
 * Queries hotel dataset
 */
async function fetchHotels(params = {}) {
  try {
    const response = await aiClient.get('/ai/hotels', { params });
    return response.data;
  } catch (error) {
    return [];
  }
}

/**
 * Retrieves agent transparency logs
 */
async function fetchAgentLogs(tripId) {
  try {
    const response = await aiClient.get(`/ai/agent-logs/${tripId}`);
    return response.data;
  } catch (error) {
    return [];
  }
}

/**
 * Queries destinations catalogue (50 Indian + 25 International)
 */
async function fetchDestinations(params = {}) {
  try {
    const response = await aiClient.get('/ai/destinations', { params });
    return response.data;
  } catch (error) {
    logger?.error ? logger.error(`Failed to fetch destinations: ${error.message}`) : console.error(error);
    return [];
  }
}

/**
 * Queries real OSRM drivable route directions and cost breakdown
 */
async function fetchRouteDirections(params = {}) {
  try {
    const response = await aiClient.get('/ai/route-directions', { params });
    return response.data;
  } catch (error) {
    if (error.response?.data?.detail) {
      throw new Error(error.response.data.detail);
    }
    throw new Error(`Route calculation failed: ${error.message}`);
  }
}

/**
 * Auth support - User proxying / management with database
 */
async function registerUser(userData) {
  try {
    const response = await aiClient.post('/ai/auth/register', userData);
    return response.data;
  } catch (error) {
    if (error.response?.data?.detail) {
      throw new Error(error.response.data.detail);
    }
    throw error;
  }
}

async function verifyUserLogin(email, password) {
  try {
    const response = await aiClient.post('/ai/auth/login', { email, password });
    return response.data;
  } catch (error) {
    if (error.response?.data?.detail) {
      throw new Error(error.response.data.detail);
    }
    throw error;
  }
}

async function getUserProfile(userId) {
  try {
    const response = await aiClient.get(`/ai/auth/user/${userId}`);
    return response.data;
  } catch (error) {
    if (error.response?.data?.detail) {
      throw new Error(error.response.data.detail);
    }
    throw error;
  }
}

module.exports = {
  checkAIHealth,
  generateTripPlan,
  fetchSavedTrips,
  fetchTripById,
  fetchDestinations,
  fetchRouteDirections,
  fetchHotels,
  fetchAgentLogs,
  registerUser,
  verifyUserLogin,
  getUserProfile,
};
