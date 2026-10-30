const aiService = require('../services/aiService');

/**
 * Health check controller
 */
async function getHealth(req, res, next) {
  try {
    const aiStatus = await aiService.checkAIHealth();
    res.json({
      status: 'healthy',
      gateway: 'TravelSync Node.js API Gateway',
      version: '1.0.0',
      timestamp: new Date().toISOString(),
      ai_service: aiStatus,
    });
  } catch (error) {
    next(error);
  }
}

/**
 * Generate trip plan
 */
async function generateTrip(req, res, next) {
  try {
    const { user_request, source, destination, duration_days, travelers, budget, interests, travel_style, trip_type, transport_mode } = req.body;

    if (!user_request || typeof user_request !== 'string' || user_request.trim().length === 0) {
      return res.status(400).json({
        success: false,
        error: 'Missing or invalid `user_request` prompt in request body.',
      });
    }

    const payload = {
      user_request: user_request.trim(),
      user_id: req.user?.id || null, // Associate with logged in user if available
      source,
      destination,
      duration_days: duration_days ? parseInt(duration_days, 10) : undefined,
      travelers: travelers ? parseInt(travelers, 10) : undefined,
      budget: budget ? parseFloat(budget) : undefined,
      interests: Array.isArray(interests) ? interests : undefined,
      travel_style: travel_style || 'balanced',
      trip_type: trip_type || 'leisure',
      transport_mode: transport_mode || 'flight',
    };

    const tripData = await aiService.generateTripPlan(payload);

    res.status(200).json({
      success: true,
      message: 'Travel plan generated successfully via LangGraph multi-agent orchestration.',
      data: tripData,
    });
  } catch (error) {
    next(error);
  }
}

/**
 * List saved trips (optionally filtered by authenticated user)
 */
async function getTrips(req, res, next) {
  try {
    const limit = req.query.limit ? parseInt(req.query.limit, 10) : 30;
    const userId = req.query.user_id || req.user?.id || null;
    const trips = await aiService.fetchSavedTrips(limit, userId);
    res.json({
      success: true,
      count: trips.length,
      data: trips,
    });
  } catch (error) {
    next(error);
  }
}

/**
 * Get trip by id
 */
async function getTripById(req, res, next) {
  try {
    const { id } = req.params;
    const tripDetails = await aiService.fetchTripById(id);
    res.json({
      success: true,
      data: tripDetails,
    });
  } catch (error) {
    next(error);
  }
}

/**
 * Get searchable destinations catalogue (50 Indian + 25 International)
 */
async function getDestinations(req, res, next) {
  try {
    const { query, country, region, category } = req.query;
    const destinations = await aiService.fetchDestinations({ query, country, region, category });
    res.json({
      success: true,
      count: destinations.length,
      data: destinations,
    });
  } catch (error) {
    next(error);
  }
}

/**
 * Get personal vehicle route directions
 */
async function getRouteDirections(req, res, next) {
  try {
    const { source, destination, travelers, is_round_trip } = req.query;
    if (!source || !destination) {
      return res.status(400).json({
        success: false,
        error: 'Missing required `source` or `destination` query parameters.',
      });
    }
    const route = await aiService.fetchRouteDirections({ source, destination, travelers, is_round_trip });
    res.json({
      success: true,
      data: route,
    });
  } catch (error) {
    next(error);
  }
}

/**
 * Get hotels
 */
async function getHotels(req, res, next) {
  try {
    const { city, max_price } = req.query;
    const hotels = await aiService.fetchHotels({ city, max_price });
    res.json({
      success: true,
      count: hotels.length,
      data: hotels,
    });
  } catch (error) {
    next(error);
  }
}

/**
 * Get agent logs for a trip
 */
async function getAgentLogs(req, res, next) {
  try {
    const { tripId } = req.params;
    const logs = await aiService.fetchAgentLogs(tripId);
    res.json({
      success: true,
      count: logs.length,
      data: logs,
    });
  } catch (error) {
    next(error);
  }
}

module.exports = {
  getHealth,
  generateTrip,
  getTrips,
  getTripById,
  getDestinations,
  getRouteDirections,
  getHotels,
  getAgentLogs,
};
