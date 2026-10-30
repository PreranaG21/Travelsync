const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const path = require('path');
require('dotenv').config({ path: path.resolve(__dirname, '../../.env') });

const tripRoutes = require('./routes/tripRoutes');
const authRoutes = require('./routes/authRoutes');
const tripController = require('./controllers/tripController');
const { errorHandler, notFoundHandler } = require('./middleware/errorHandler');

const app = express();
const PORT = process.env.PORT || 5000;

// Middlewares
app.use(cors({
  origin: true,
  credentials: true,
}));
app.use(express.json());
app.use(morgan('dev'));

// Direct health check & API Routes
app.get('/health', tripController.getHealth);
app.use('/api/auth', authRoutes);
app.use('/api', tripRoutes);

// Root greeting
app.get('/', (req, res) => {
  res.json({
    brand: 'TravelSync',
    tagline: 'Plan Smarter. Travel Better.',
    description: 'AI Travel Planner Using Multi-Agent System (API Gateway)',
    endpoints: {
      health: 'GET /api/health',
      auth: {
        register: 'POST /api/auth/register',
        login: 'POST /api/auth/login',
        me: 'GET /api/auth/me',
      },
      generate_trip: 'POST /api/generate-trip',
      trips: 'GET /api/trips',
      trip_details: 'GET /api/trips/:id',
      hotels: 'GET /api/hotels',
      agent_logs: 'GET /api/agent-logs/:tripId',
    },
  });
});

// 404 & Error Handlers
app.use(notFoundHandler);
app.use(errorHandler);

if (process.env.NODE_ENV !== 'test') {
  app.listen(PORT, () => {
    console.log(`====================================================`);
    console.log(` TravelSync Node.js API Gateway running on port ${PORT}`);
    console.log(` Target AI Service: ${process.env.AI_SERVICE_URL || 'http://127.0.0.1:8000'}`);
    console.log(` Health Check: http://localhost:${PORT}/api/health`);
    console.log(`====================================================`);
  });
}

module.exports = app;
