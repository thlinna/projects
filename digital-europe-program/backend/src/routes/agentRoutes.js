const express = require('express');
const router = express.Router();
const {
  ideateWithIdeanikkari,
  evaluateWithArvioija,
  createApplicationWithHakija,
  reviewWithRahoittaja,
} = require('../controllers/agentController');
const { protect } = require('../middleware/auth');

/**
 * @swagger
 * /api/agents/ideanikkari:
 *   post:
 *     summary: Ideoi Ideanikkari-agentin kanssa
 *     tags: [Agents]
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - projectId
 *               - message
 *             properties:
 *               projectId:
 *                 type: string
 *               message:
 *                 type: string
 *               domain:
 *                 type: string
 *               interests:
 *                 type: array
 *                 items:
 *                   type: string
 *     responses:
 *       200:
 *         description: Onnistunut ideointi
 */
router.post('/ideanikkari', protect, ideateWithIdeanikkari);

/**
 * @swagger
 * /api/agents/arvioija:
 *   post:
 *     summary: Arvioi idean Arvioija-agentin kanssa
 *     tags: [Agents]
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - ideaId
 *               - message
 *             properties:
 *               ideaId:
 *                 type: string
 *               message:
 *                 type: string
 *     responses:
 *       200:
 *         description: Onnistunut arviointi
 */
router.post('/arvioija', protect, evaluateWithArvioija);

/**
 * @swagger
 * /api/agents/hakija:
 *   post:
 *     summary: Luo hakemus Hakija-agentin kanssa
 *     tags: [Agents]
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - ideaId
 *               - projectId
 *               - message
 *             properties:
 *               ideaId:
 *                 type: string
 *               projectId:
 *                 type: string
 *               message:
 *                 type: string
 *     responses:
 *       200:
 *         description: Onnistunut hakemuksen luonti
 */
router.post('/hakija', protect, createApplicationWithHakija);

/**
 * @swagger
 * /api/agents/rahoittaja:
 *   post:
 *     summary: Arvioi hakemuksen Rahoittaja-agentin kanssa
 *     tags: [Agents]
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - applicationId
 *               - message
 *             properties:
 *               applicationId:
 *                 type: string
 *               message:
 *                 type: string
 *     responses:
 *       200:
 *         description: Onnistunut hakemuksen arviointi
 */
router.post('/rahoittaja', protect, reviewWithRahoittaja);

module.exports = router; 