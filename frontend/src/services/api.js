import axios from 'axios';

// Base API URL falls back to relative /api (handled by Vite proxy in dev) or full URL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 90000, // 90 seconds to allow full multi-agent reasoning & external APIs
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor: attach JWT token if available
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('travelsync_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor: handle network & gateway errors cleanly
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (!error.response) {
      // Unreachable server / Network error
      error.friendlyMessage =
        'TravelSync could not connect to the planning service. Please make sure the TravelSync services are running and try again.';
      console.error('[API Connection Error] Server unreachable:', error.message);
    } else {
      const serverMsg =
        error.response.data?.error ||
        error.response.data?.message ||
        error.response.data?.detail;

      if (error.response.status === 401) {
        error.friendlyMessage = serverMsg || 'Authentication required. Please log in.';
      } else if (error.response.status === 404) {
        error.friendlyMessage = serverMsg || 'Requested resource was not found.';
      } else if (error.response.status >= 500) {
        error.friendlyMessage =
          serverMsg ||
          'The server encountered an error processing your request. Please try again.';
      } else {
        error.friendlyMessage = serverMsg || error.message;
      }
      console.error(`[API Error ${error.response.status}]`, error.friendlyMessage, error.response.data);
    }
    return Promise.reject(error);
  }
);

/**
 * Health check
 */
export async function getSystemHealth() {
  try {
    const res = await apiClient.get('/health');
    return res.data;
  } catch (error) {
    throw new Error(error.friendlyMessage || error.message);
  }
}

/**
 * Auth Endpoints
 */
export async function registerUser(userData) {
  try {
    const res = await apiClient.post('/auth/register', userData);
    return res.data;
  } catch (error) {
    throw new Error(error.friendlyMessage || error.message);
  }
}

export async function loginUser(credentials) {
  try {
    const res = await apiClient.post('/auth/login', credentials);
    return res.data;
  } catch (error) {
    throw new Error(error.friendlyMessage || error.message);
  }
}

export async function getCurrentUser() {
  try {
    const res = await apiClient.get('/auth/me');
    return res.data;
  } catch (error) {
    throw new Error(error.friendlyMessage || error.message);
  }
}

/**
 * Generates trip itinerary using Multi-Agent LangGraph system
 */
export async function generateTrip(payload) {
  try {
    const res = await apiClient.post('/generate-trip', payload);
    return res.data.data;
  } catch (error) {
    throw new Error(error.friendlyMessage || error.message);
  }
}

/**
 * Fetches saved trips
 */
export async function getSavedTrips(limit = 30) {
  try {
    const res = await apiClient.get('/trips', { params: { limit } });
    return res.data.data || res.data;
  } catch (error) {
    throw new Error(error.friendlyMessage || error.message);
  }
}

/**
 * Fetches trip details by id
 */
export async function getTripById(tripId) {
  try {
    const res = await apiClient.get(`/trips/${tripId}`);
    return res.data.data || res.data;
  } catch (error) {
    throw new Error(error.friendlyMessage || error.message);
  }
}

/**
 * Fetches hotel dataset
 */
export async function getHotels(params = {}) {
  try {
    const res = await apiClient.get('/hotels', { params });
    return res.data.data || res.data;
  } catch (error) {
    return [];
  }
}

/**
 * Fetches agent logs for a trip
 */
export async function getAgentLogs(tripId) {
  try {
    const res = await apiClient.get(`/agent-logs/${tripId}`);
    return res.data.data || res.data;
  } catch (error) {
    return [];
  }
}

/**
 * Fetches destinations catalogue with optional search/region/category filters
 */
export async function getDestinations(params = {}) {
  try {
    const res = await apiClient.get('/destinations', { params });
    return res.data.data || res.data || [];
  } catch (error) {
    console.error('Failed to load destinations:', error);
    return [];
  }
}

/**
 * Fetches route directions and navigation info
 */
export async function getRouteDirections(params = {}) {
  try {
    const res = await apiClient.get('/route-directions', { params });
    return res.data.data || res.data;
  } catch (error) {
    throw new Error(error.friendlyMessage || error.message);
  }
}

