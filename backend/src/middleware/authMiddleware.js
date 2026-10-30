const jwt = require('jsonwebtoken');

const JWT_SECRET = process.env.JWT_SECRET || 'travelsync_super_secret_jwt_key_academic_project_2026';

/**
 * Middleware that requires a valid JWT token
 */
function requireAuth(req, res, next) {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({
      success: false,
      message: 'Authentication required. Please log in to access this feature.',
    });
  }

  const token = authHeader.split(' ')[1];
  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    return res.status(401).json({
      success: false,
      message: 'Your session has expired or is invalid. Please log in again.',
    });
  }
}

/**
 * Optional authentication: decodes token if provided, but does not block if omitted
 */
function optionalAuth(req, res, next) {
  const authHeader = req.headers.authorization;
  if (authHeader && authHeader.startsWith('Bearer ')) {
    const token = authHeader.split(' ')[1];
    try {
      const decoded = jwt.verify(token, JWT_SECRET);
      req.user = decoded;
    } catch (error) {
      // Ignore token verification error for optional auth
    }
  }
  next();
}

module.exports = {
  requireAuth,
  optionalAuth,
};
