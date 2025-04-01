const jwt = require('jsonwebtoken');
const User = require('../models/User');

/**
 * Middleware, joka suojaa reittejä autentikaatiolla
 * Tarkistaa, että käyttäjä on kirjautunut sisään
 */
exports.protect = async (req, res, next) => {
  let token;

  // Tarkista Authorization-header
  if (
    req.headers.authorization &&
    req.headers.authorization.startsWith('Bearer')
  ) {
    // Aseta token headerista
    token = req.headers.authorization.split(' ')[1];
  }
  // Tarkista myös mahdollinen cookie
  else if (req.cookies.token) {
    token = req.cookies.token;
  }

  // Tarkista että token on olemassa
  if (!token) {
    return res.status(401).json({
      success: false,
      message: 'Ei oikeutta tälle sivulle',
    });
  }

  try {
    // Vahvista token
    const decoded = jwt.verify(token, process.env.JWT_SECRET);

    // Hae käyttäjä token ID:llä ja lisää req.user
    req.user = await User.findById(decoded.id);

    next();
  } catch (error) {
    return res.status(401).json({
      success: false,
      message: 'Ei oikeutta tälle sivulle',
    });
  }
};

/**
 * Middleware, joka rajoittaa pääsyn tietyille rooleille
 * Käytetään protect-middlewaren jälkeen
 */
exports.authorize = (...roles) => {
  return (req, res, next) => {
    if (!roles.includes(req.user.role)) {
      return res.status(403).json({
        success: false,
        message: `Käyttäjäroolilla ${req.user.role} ei ole oikeutta tälle sivulle`,
      });
    }
    next();
  };
}; 