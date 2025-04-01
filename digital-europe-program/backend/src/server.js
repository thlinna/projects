const express = require('express');
const dotenv = require('dotenv');
const cors = require('cors');
const helmet = require('helmet');
const xss = require('xss-clean');
const rateLimit = require('express-rate-limit');
const mongoose = require('mongoose');
const morgan = require('morgan');
const swaggerJsDoc = require('swagger-jsdoc');
const swaggerUi = require('swagger-ui-express');

// Lataa ympäristömuuttujat
dotenv.config();

// Luo Express app
const app = express();

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cors());
app.use(helmet());
app.use(xss());

// Rate limiting
const limiter = rateLimit({
  windowMs: 10 * 60 * 1000, // 10 minuuttia
  max: 100, // rajoita jokaista IP:tä 100 pyyntöön per ikkuna
});
app.use(limiter);

// Lokitus
if (process.env.NODE_ENV === 'development') {
  app.use(morgan('dev'));
}

// Swagger määritys
const swaggerOptions = {
  swaggerDefinition: {
    openapi: '3.0.0',
    info: {
      title: 'Digital Europe Program API',
      version: '1.0.0',
      description: 'API-dokumentaatio Digital Europe Program rahoitushakemustyökalulle',
    },
    servers: [
      {
        url: `http://localhost:${process.env.PORT || 5000}`,
        description: 'Kehityspalvelin',
      },
    ],
  },
  apis: ['./src/routes/*.js'],
};

const swaggerDocs = swaggerJsDoc(swaggerOptions);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocs));

// Ensisijainen reitti
app.get('/', (req, res) => {
  res.json({
    message: 'Tervetuloa Digital Europe Program API:in',
  });
});

// API-reitit
app.use('/api/users', require('./routes/userRoutes'));
app.use('/api/projects', require('./routes/projectRoutes'));
app.use('/api/agents', require('./routes/agentRoutes'));

// Määrittele portti
const PORT = process.env.PORT || 5000;

// Tietokantayhteys ja palvelimen käynnistys
mongoose
  .connect(process.env.MONGO_URI)
  .then(() => {
    app.listen(PORT, () => {
      console.log(`Palvelin käynnissä portissa ${PORT} (${process.env.NODE_ENV})`);
    });
  })
  .catch((err) => {
    console.error('MongoDB yhteysongelma:', err.message);
    process.exit(1);
  });

// Käsittele käsittelemättömät promise-poikkeukset
process.on('unhandledRejection', (err) => {
  console.error('Käsittelemätön Promise-poikkeus:', err.message);
  // Sulje palvelin hallitusti ja lopeta prosessi
  process.exit(1);
}); 