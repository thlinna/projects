const Project = require('../models/Project');
const User = require('../models/User');

/**
 * @desc    Hakee kaikki käyttäjän projektit
 * @route   GET /api/projects
 * @access  Private
 */
exports.getProjects = async (req, res) => {
  try {
    // Hae projektit, joissa käyttäjä on omistaja tai jäsen
    const projects = await Project.getProjectsByUser(req.user.id);

    res.status(200).json({
      success: true,
      count: projects.length,
      data: projects,
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
 * @desc    Hakee yksittäisen projektin
 * @route   GET /api/projects/:id
 * @access  Private
 */
exports.getProject = async (req, res) => {
  try {
    const project = await Project.findById(req.params.id)
      .populate('owner', 'name email')
      .populate('members.user', 'name email')
      .populate('ideas')
      .populate('applications');

    if (!project) {
      return res.status(404).json({
        success: false,
        message: 'Projektia ei löydy',
      });
    }

    // Tarkista, että käyttäjällä on oikeus projektiin
    if (
      project.owner._id.toString() !== req.user.id && 
      !project.members.some(m => m.user._id.toString() === req.user.id)
    ) {
      return res.status(403).json({
        success: false,
        message: 'Ei oikeutta tähän projektiin',
      });
    }

    res.status(200).json({
      success: true,
      data: project,
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
 * @desc    Luo uuden projektin
 * @route   POST /api/projects
 * @access  Private
 */
exports.createProject = async (req, res) => {
  try {
    // Lisää käyttäjä projektin omistajaksi
    req.body.owner = req.user.id;

    const project = await Project.create(req.body);

    res.status(201).json({
      success: true,
      data: project,
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
 * @desc    Päivittää projektin
 * @route   PUT /api/projects/:id
 * @access  Private
 */
exports.updateProject = async (req, res) => {
  try {
    let project = await Project.findById(req.params.id);

    if (!project) {
      return res.status(404).json({
        success: false,
        message: 'Projektia ei löydy',
      });
    }

    // Tarkista, että käyttäjällä on oikeudet muokata
    if (
      project.owner.toString() !== req.user.id && 
      !project.members.some(m => 
        m.user.toString() === req.user.id && 
        ['admin', 'editor'].includes(m.role)
      )
    ) {
      return res.status(403).json({
        success: false,
        message: 'Ei oikeutta muokata tätä projektia',
      });
    }

    project = await Project.findByIdAndUpdate(req.params.id, req.body, {
      new: true,
      runValidators: true,
    });

    res.status(200).json({
      success: true,
      data: project,
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
 * @desc    Poistaa projektin
 * @route   DELETE /api/projects/:id
 * @access  Private
 */
exports.deleteProject = async (req, res) => {
  try {
    const project = await Project.findById(req.params.id);

    if (!project) {
      return res.status(404).json({
        success: false,
        message: 'Projektia ei löydy',
      });
    }

    // Vain omistaja voi poistaa projektin
    if (project.owner.toString() !== req.user.id) {
      return res.status(403).json({
        success: false,
        message: 'Ei oikeutta poistaa tätä projektia',
      });
    }

    await project.remove();

    res.status(200).json({
      success: true,
      data: {},
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
 * @desc    Lisää jäsenen projektiin
 * @route   POST /api/projects/:id/members
 * @access  Private
 */
exports.addMember = async (req, res) => {
  try {
    const { email, role } = req.body;
    
    // Etsi projekti
    const project = await Project.findById(req.params.id);

    if (!project) {
      return res.status(404).json({
        success: false,
        message: 'Projektia ei löydy',
      });
    }

    // Tarkista, että käyttäjällä on oikeudet lisätä jäseniä
    if (
      project.owner.toString() !== req.user.id && 
      !project.members.some(m => 
        m.user.toString() === req.user.id && 
        m.role === 'admin'
      )
    ) {
      return res.status(403).json({
        success: false,
        message: 'Ei oikeutta lisätä jäseniä tähän projektiin',
      });
    }

    // Etsi käyttäjä sähköpostilla
    const user = await User.findOne({ email });

    if (!user) {
      return res.status(404).json({
        success: false,
        message: 'Käyttäjää ei löydy annetulla sähköpostilla',
      });
    }

    // Tarkista, onko käyttäjä jo jäsen
    if (
      project.owner.toString() === user._id.toString() ||
      project.members.some(m => m.user.toString() === user._id.toString())
    ) {
      return res.status(400).json({
        success: false,
        message: 'Käyttäjä on jo projektin jäsen',
      });
    }

    // Lisää käyttäjä projektiin
    project.members.push({
      user: user._id,
      role,
    });

    await project.save();

    res.status(200).json({
      success: true,
      data: project,
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
 * @desc    Poistaa jäsenen projektista
 * @route   DELETE /api/projects/:id/members/:userId
 * @access  Private
 */
exports.removeMember = async (req, res) => {
  try {
    // Etsi projekti
    const project = await Project.findById(req.params.id);

    if (!project) {
      return res.status(404).json({
        success: false,
        message: 'Projektia ei löydy',
      });
    }

    // Tarkista, että käyttäjällä on oikeudet poistaa jäseniä
    // (omistaja, admin tai käyttäjä poistaa itsensä)
    if (
      project.owner.toString() !== req.user.id && 
      !project.members.some(m => 
        m.user.toString() === req.user.id && 
        m.role === 'admin'
      ) &&
      req.user.id !== req.params.userId
    ) {
      return res.status(403).json({
        success: false,
        message: 'Ei oikeutta poistaa jäseniä tästä projektista',
      });
    }

    // Poista jäsen
    project.members = project.members.filter(
      m => m.user.toString() !== req.params.userId
    );

    await project.save();

    res.status(200).json({
      success: true,
      data: project,
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Palvelinvirhe',
      error: error.message,
    });
  }
}; 