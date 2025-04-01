const mongoose = require('mongoose');

/**
 * Muodostaa yhteyden MongoDB-tietokantaan
 * @returns {Promise} MongoDB yhteyden lupaus
 */
const connectDB = async () => {
  try {
    const conn = await mongoose.connect(process.env.MONGO_URI);
    console.log(`MongoDB yhdistetty: ${conn.connection.host}`);
    return conn;
  } catch (error) {
    console.error(`Virhe: ${error.message}`);
    process.exit(1);
  }
};

module.exports = connectDB; 