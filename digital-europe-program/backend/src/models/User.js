const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

const UserSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: [true, 'Nimi on pakollinen'],
      trim: true,
      maxlength: [50, 'Nimi voi olla enintään 50 merkkiä pitkä'],
    },
    email: {
      type: String,
      required: [true, 'Sähköposti on pakollinen'],
      unique: true,
      match: [
        /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/,
        'Anna kelvollinen sähköpostiosoite',
      ],
    },
    password: {
      type: String,
      required: [true, 'Salasana on pakollinen'],
      minlength: [6, 'Salasanan tulee olla vähintään 6 merkkiä pitkä'],
      select: false,
    },
    role: {
      type: String,
      enum: ['user', 'member', 'admin'],
      default: 'user',
    },
    resetPasswordToken: String,
    resetPasswordExpire: Date,
  },
  {
    timestamps: true,
  }
);

// Salaa salasanan ennen tallennusta
UserSchema.pre('save', async function (next) {
  if (!this.isModified('password')) {
    next();
  }

  const salt = await bcrypt.genSalt(10);
  this.password = await bcrypt.hash(this.password, salt);
});

// Allekirjoita JWT ja palauta
UserSchema.methods.getSignedJwtToken = function () {
  return jwt.sign(
    { id: this._id, role: this.role },
    process.env.JWT_SECRET,
    {
      expiresIn: process.env.JWT_EXPIRE,
    }
  );
};

// Vertaa käyttäjän antamaa salasanaa hashattuun salasanaan
UserSchema.methods.matchPassword = async function (enteredPassword) {
  return await bcrypt.compare(enteredPassword, this.password);
};

module.exports = mongoose.model('User', UserSchema); 