const express = require('express');
const router = express.Router();
const {
  getProjects,
  getProject,
  createProject,
  updateProject,
  deleteProject,
  addMember,
  removeMember,
} = require('../controllers/projectController');
const { protect, authorize } = require('../middleware/auth');

/**
 * @swagger
 * /api/projects:
 *   get:
 *     summary: Hakee kaikki käyttäjän projektit
 *     tags: [Projects]
 *     security:
 *       - bearerAuth: []
 *     responses:
 *       200:
 *         description: Projektit haettu onnistuneesti
 */
router.get('/', protect, getProjects);

/**
 * @swagger
 * /api/projects:
 *   post:
 *     summary: Luo uuden projektin
 *     tags: [Projects]
 *     security:
 *       - bearerAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - name
 *               - description
 *               - domain
 *             properties:
 *               name:
 *                 type: string
 *               description:
 *                 type: string
 *               domain:
 *                 type: string
 *               tags:
 *                 type: array
 *                 items:
 *                   type: string
 *     responses:
 *       201:
 *         description: Projekti luotu onnistuneesti
 */
router.post('/', protect, createProject);

/**
 * @swagger
 * /api/projects/{id}:
 *   get:
 *     summary: Hakee yksittäisen projektin
 *     tags: [Projects]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         schema:
 *           type: string
 *         required: true
 *         description: Projektin ID
 *     responses:
 *       200:
 *         description: Projekti haettu onnistuneesti
 */
router.get('/:id', protect, getProject);

/**
 * @swagger
 * /api/projects/{id}:
 *   put:
 *     summary: Päivittää projektin tiedot
 *     tags: [Projects]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         schema:
 *           type: string
 *         required: true
 *         description: Projektin ID
 *     requestBody:
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               name:
 *                 type: string
 *               description:
 *                 type: string
 *               domain:
 *                 type: string
 *               status:
 *                 type: string
 *                 enum: [draft, idea, evaluation, application, review, completed]
 *               tags:
 *                 type: array
 *                 items:
 *                   type: string
 *     responses:
 *       200:
 *         description: Projekti päivitetty onnistuneesti
 */
router.put('/:id', protect, updateProject);

/**
 * @swagger
 * /api/projects/{id}:
 *   delete:
 *     summary: Poistaa projektin
 *     tags: [Projects]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         schema:
 *           type: string
 *         required: true
 *         description: Projektin ID
 *     responses:
 *       200:
 *         description: Projekti poistettu onnistuneesti
 */
router.delete('/:id', protect, deleteProject);

/**
 * @swagger
 * /api/projects/{id}/members:
 *   post:
 *     summary: Lisää jäsenen projektiin
 *     tags: [Projects]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         schema:
 *           type: string
 *         required: true
 *         description: Projektin ID
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - email
 *               - role
 *             properties:
 *               email:
 *                 type: string
 *               role:
 *                 type: string
 *                 enum: [viewer, editor, admin]
 *     responses:
 *       200:
 *         description: Jäsen lisätty onnistuneesti
 */
router.post('/:id/members', protect, addMember);

/**
 * @swagger
 * /api/projects/{id}/members/{userId}:
 *   delete:
 *     summary: Poistaa jäsenen projektista
 *     tags: [Projects]
 *     security:
 *       - bearerAuth: []
 *     parameters:
 *       - in: path
 *         name: id
 *         schema:
 *           type: string
 *         required: true
 *         description: Projektin ID
 *       - in: path
 *         name: userId
 *         schema:
 *           type: string
 *         required: true
 *         description: Poistettavan käyttäjän ID
 *     responses:
 *       200:
 *         description: Jäsen poistettu onnistuneesti
 */
router.delete('/:id/members/:userId', protect, removeMember);

module.exports = router; 