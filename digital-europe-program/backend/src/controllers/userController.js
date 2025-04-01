const User = require('../models/User');
const crypto = require('crypto');
const bcrypt = require('bcryptjs');

/**
 * @desc    Rekisteröi käyttäjän
 * @route   POST /api/users/register
 * @access  Public
 */
exports.register = async (req, res) => {
  try {
    const { name, email, password } = req.body;

    // Tarkista onko käyttäjä jo olemassa
    const userExists = await User.findOne({ email });

    if (userExists) {
      return res.status(400).json({
        success: false,
        message: 'Sähköposti on jo käytössä',
      });
    }

    // Luo käyttäjä
    const user = await User.create({
      name,
      email,
      password,
    });

    // Luo ja lähetä token
    sendTokenResponse(user, 201, res);
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Palvelinvirhe',
      error: error.message,
    });
  }
};

/**
 * @desc    Kirjaa käyttäjän sisään
 * @route   POST /api/users/login
 * @access  Public
 */
exports.login = async (req, res) => {
  try {
    const { email, password } = req.body;

    // Validoi tiedot
    if (!email || !password) {
      return res.status(400).json({
        success: false,
        message: 'Anna sähköposti ja salasana',
      });
    }

    // Tarkista käyttäjä
    const user = await User.findOne({ email }).select('+password');

    if (!user) {
      return res.status(401).json({
        success: false,
        message: 'Virheelliset kirjautumistiedot',
      });
    }

    // Tarkista salasana
    const isMatch = await user.matchPassword(password);

    if (!isMatch) {
      return res.status(401).json({
        success: false,
        message: 'Virheelliset kirjautumistiedot',
      });
    }

    // Luo ja lähetä token
    sendTokenResponse(user, 200, res);
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Palvelinvirhe',
      error: error.message,
    });
  }
};

/**
 * @desc    Hakee kirjautuneen käyttäjän
 * @route   GET /api/users/me
 * @access  Private
 */
exports.getMe = async (req, res) => {
  try {
    const user = await User.findById(req.user.id);

    res.status(200).json({
      success: true,
      data: user,
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Palvelinvirhe',
      error: error.message,
    });
  }
};

/**
 * @desc    Päivittää käyttäjän tiedot
 * @route   PUT /api/users/updatedetails
 * @access  Private
 */
exports.updateDetails = async (req, res) => {
  try {
    const fieldsToUpdate = {
      name: req.body.name,
      email: req.body.email,
    };

    const user = await User.findByIdAndUpdate(req.user.id, fieldsToUpdate, {
      new: true,
      runValidators: true,
    });

    res.status(200).json({
      success: true,
      data: user,
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Palvelinvirhe',
      error: error.message,
    });
  }
};

/**
 * @desc    Päivittää käyttäjän salasanan
 * @route   PUT /api/users/updatepassword
 * @access  Private
 */
exports.updatePassword = async (req, res) => {
  try {
    const user = await User.findById(req.user.id).select('+password');

    // Tarkista nykyinen salasana
    if (!(await user.matchPassword(req.body.currentPassword))) {
      return res.status(401).json({
        success: false,
        message: 'Nykyinen salasana on virheellinen',
      });
    }

    user.password = req.body.newPassword;
    await user.save();

    sendTokenResponse(user, 200, res);
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Palvelinvirhe',
      error: error.message,
    });
  }
};

/**
 * @desc    Aloittaa salasanan palautuksen
 * @route   POST /api/users/forgotpassword
 * @access  Public
 */
exports.forgotPassword = async (req, res) => {
  try {
    const user = await User.findOne({ email: req.body.email });

    if (!user) {
      return res.status(404).json({
        success: false,
        message: 'Käyttäjää ei löydy',
      });
    }

    // Luo resetointitoken
    const resetToken = crypto.randomBytes(20).toString('hex');

    // Hashattu token ja aseta voimassaoloaika
    user.resetPasswordToken = crypto
      .createHash('sha256')
      .update(resetToken)
      .digest('hex');
    
    user.resetPasswordExpire = Date.now() + 10 * 60 * 1000; // 10 minuuttia

    await user.save({ validateBeforeSave: false });

    // Tässä vaiheessa normaalisti lähetettäisiin sähköposti, mutta yksinkertaisuuden
    // vuoksi palautamme vain tokenin
    res.status(200).json({
      success: true,
      data: resetToken,
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Palvelinvirhe',
      error: error.message,
    });
  }
};

/**
 * @desc    Palauttaa salasanan tokenia käyttäen
 * @route   PUT /api/users/resetpassword/:resettoken
 * @access  Public
 */
exports.resetPassword = async (req, res) => {
  try {
    // Hae hashattu token
    const resetPasswordToken = crypto
      .createHash('sha256')
      .update(req.params.resettoken)
      .digest('hex');

    const user = await User.findOne({
      resetPasswordToken,
      resetPasswordExpire: { $gt: Date.now() },
    });

    if (!user) {
      return res.status(400).json({
        success: false,
        message: 'Virheellinen token tai token on vanhentunut',
      });
    }

    // Aseta uusi salasana
    user.password = req.body.password;
    user.resetPasswordToken = undefined;
    user.resetPasswordExpire = undefined;
    await user.save();

    sendTokenResponse(user, 200, res);
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Palvelinvirhe',
      error: error.message,
    });
  }
};

/**
 * Apufunktio tokenin luomiseen ja lähettämiseen
 */
const sendTokenResponse = (user, statusCode, res) => {
  // Luo token
  const token = user.getSignedJwtToken();

  const options = {
    expires: new Date(
      Date.now() + process.env.JWT_COOKIE_EXPIRE * 24 * 60 * 60 * 1000
    ),
    httpOnly: true,
  };

  // Aseta secure-flag jos tuotannossa
  if (process.env.NODE_ENV === 'production') {
    options.secure = true;
  }

  res
    .status(statusCode)
    .cookie('token', token, options)
    .json({
      success: true,
      token,
    });
}; 