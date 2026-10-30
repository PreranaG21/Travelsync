const express = require('express');
const router = express.Router();
const tripController = require('../controllers/tripController');
const { optionalAuth } = require('../middleware/authMiddleware');

router.get('/health', tripController.getHealth);
router.post('/generate-trip', optionalAuth, tripController.generateTrip);
router.post('/plan-trip', optionalAuth, tripController.generateTrip);
router.post('/trips/plan', optionalAuth, tripController.generateTrip);
router.get('/trips', optionalAuth, tripController.getTrips);
router.get('/trips/:id', tripController.getTripById);
router.get('/destinations', tripController.getDestinations);
router.get('/route-directions', tripController.getRouteDirections);
router.get('/hotels', tripController.getHotels);
router.get('/agent-logs/:tripId', tripController.getAgentLogs);

module.exports = router;
