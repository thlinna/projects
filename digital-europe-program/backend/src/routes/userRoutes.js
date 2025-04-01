const express = require('express');
const router = express.Router();
const { 
  register, 
  login, 
  getMe, 
  updateDetails,
  updatePassword,
  forgotPassword,
  resetPassword
} = require('../controllers/userController');
const { protect } = require('../middleware/auth');

/**
 * @swagger
 * /api/users/register:
 *   post:
 *     summary: Rekisteröi uuden käyttäjän
 *     tags: [Users]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - name
 *               - email
 *               - password
 *             properties:
 *               name:
 *                 type: string
 *               email:
 *                 type: string
 *               password:
 *                 type: string
 *     responses:
 *       200:
 *         description: Käyttäjä rekisteröity onnistuneesti
 */
router.post('/register', register);

/**
 * @swagger
 * /api/users/login:
 *   post:
 *     summary: Kirjaa käyttäjän sisään
 *     tags: [Users]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - email
 *               - password
 *             properties:
 *               email:
 *                 type: string
 *               password:
 *                 type: string
 *     responses:
 *       200:
 *         description: Kirjautuminen onnistui
 */
router.post('/login', login);

/**
 * @swagger
 * /api/users/me:
 *   get:
 *     summary: Hakee kirjautuneen käyttäjän tiedot
 *     tags: [Users]
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: Käyttäjätiedot haettu onnistuneesti
 */
router.get('/me', protect, getMe);

/**
 * @swagger
 * /api/users/updatedetails:
 *   put:
 *     summary: Päivittää käyttäjän tiedot
 *     tags: [Users]
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               name:
 *                 type: string
 *               email:
 *                 type: string
 *     responses:
 *       200:
 *         description: Tiedot päivitetty onnistuneesti
 */
router.put('/updatedetails', protect, updateDetails);

/**
 * @swagger
 * /api/users/updatepassword:
 *   put:
 *     summary: Päivittää käyttäjän salasanan
 *     tags: [Users]
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - currentPassword
 *               - newPassword
 *             properties:
 *               currentPassword:
 *                 type: string
 *               newPassword:
 *                 type: string
 *     responses:
 *       200:
 *         description: Salasana päivitetty onnistuneesti
 */
router.put('/updatepassword', protect, updatePassword);

/**
 * @swagger
 * /api/users/forgotpassword:
 *   post:
 *     summary: Aloittaa salasanan palautusprosessin
 *     tags: [Users]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - email
 *             properties:
 *               email:
 *                 type: string
 *     responses:
 *       200:
 *         description: Palautuslinkki lähetetty sähköpostiin
 */
router.post('/forgotpassword', forgotPassword);

/**
 * @swagger
 * /api/users/resetpassword/{resettoken}:
 *   put:
 *     summary: Palauttaa salasanan tokenia käyttäen
 *     tags: [Users]
 *     parameters:
 *       - in: path
 *         name: resettoken
 *         schema:
 *           type: string
 *         required: true
 *         description: Salasanan palautustoken
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - password
 *             properties:
 *               password:
 *                 type: string
 *     responses:
 *       200:
 *         description: Salasana palautettu onnistuneesti
 */
router.put('/resetpassword/:resettoken', resetPassword);

module.exports = router; 