const openaiService = require('../services/openaiService');
const Idea = require('../models/Idea');
const Project = require('../models/Project');
const Application = require('../models/Application');
const User = require('../models/User');

/**
 * @desc    Ideoi Ideanikkari-agentin kanssa
 * @route   POST /api/agents/ideanikkari
 * @access  Private
 */
exports.ideateWithIdeanikkari = async (req, res) => {
  try {
    const { projectId, message, domain, interests } = req.body;

    // Tarkista, että projekti on olemassa
    const project = await Project.findById(projectId);
    if (!project) {
      return res.status(404).json({
        success: false,
        message: 'Projektia ei löydy',
      });
    }

    // Tarkista, että käyttäjällä on oikeus projektiin
    if (
      project.owner.toString() !== req.user.id && 
      !project.members.some(m => m.user.toString() === req.user.id)
    ) {
      return res.status(403).json({
        success: false,
        message: 'Ei oikeutta tähän projektiin',
      });
    }

    // Käytä OpenAI-palvelua vastauksen luomiseen
    const promptData = {
      domain: domain || project.domain,
      interests: interests || [],
      projectDetails: `Projektin nimi: ${project.name}\nKuvaus: ${project.description}`
    };

    const response = await openaiService.createCompletion('ideanikkari', message, promptData);

    // Tallenna idea tietokantaan
    const idea = await Idea.create({
      title: `Idea: ${message.substring(0, 50)}...`,
      description: response,
      project: projectId,
      creator: req.user.id,
      status: 'draft',
      isAIGenerated: true,
      conversations: [
        {
          agent: 'user',
          message,
        },
        {
          agent: 'ideanikkari',
          message: response,
        },
      ],
    });

    // Päivitä projekti
    project.ideas.push(idea._id);
    await project.save();

    res.status(200).json({
      success: true,
      data: {
        response,
        idea,
      },
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
 * @desc    Arvioi idean Arvioija-agentin kanssa
 * @route   POST /api/agents/arvioija
 * @access  Private
 */
exports.evaluateWithArvioija = async (req, res) => {
  try {
    const { ideaId, message } = req.body;

    // Tarkista, että idea on olemassa
    const idea = await Idea.findById(ideaId).populate('project');
    if (!idea) {
      return res.status(404).json({
        success: false,
        message: 'Ideaa ei löydy',
      });
    }

    // Tarkista, että käyttäjällä on oikeus ideaan
    const project = idea.project;
    if (
      project.owner.toString() !== req.user.id && 
      !project.members.some(m => m.user.toString() === req.user.id)
    ) {
      return res.status(403).json({
        success: false,
        message: 'Ei oikeutta tähän ideaan',
      });
    }

    // Käytä OpenAI-palvelua vastauksen luomiseen
    const promptData = {
      ideaDetails: `Idean nimi: ${idea.title}\nKuvaus: ${idea.description}`,
      projectDetails: `Projektin nimi: ${project.name}\nKuvaus: ${project.description}\nToimiala: ${project.domain}`
    };

    const response = await openaiService.createCompletion('arvioija', message, promptData);

    // Etsi vahvuudet, heikkoudet ja parannusehdotukset vastauksesta (yksinkertaistettu toteutus)
    const strengths = [];
    const weaknesses = [];
    const suggestions = [];

    // Päivitä idea
    idea.status = 'reviewed';
    idea.conversations.push(
      {
        agent: 'user',
        message,
      },
      {
        agent: 'arvioija',
        message: response,
      }
    );

    // Lisää arviointi
    idea.reviews.push({
      reviewer: 'ai',
      score: 7, // Oletusarviointi
      comment: response,
    });

    await idea.save();

    res.status(200).json({
      success: true,
      data: {
        response,
        idea,
      },
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
 * @desc    Luo hakemus Hakija-agentin kanssa
 * @route   POST /api/agents/hakija
 * @access  Private
 */
exports.createApplicationWithHakija = async (req, res) => {
  try {
    const { ideaId, projectId, message } = req.body;

    // Tarkista, että projekti ja idea ovat olemassa
    const project = await Project.findById(projectId);
    if (!project) {
      return res.status(404).json({
        success: false,
        message: 'Projektia ei löydy',
      });
    }

    const idea = await Idea.findById(ideaId);
    if (!idea) {
      return res.status(404).json({
        success: false,
        message: 'Ideaa ei löydy',
      });
    }

    // Tarkista, että käyttäjällä on oikeus projektiin
    if (
      project.owner.toString() !== req.user.id && 
      !project.members.some(m => 
        m.user.toString() === req.user.id && 
        ['admin', 'editor'].includes(m.role)
      )
    ) {
      return res.status(403).json({
        success: false,
        message: 'Ei oikeutta tähän projektiin',
      });
    }

    // Käytä OpenAI-palvelua vastauksen luomiseen
    const promptData = {
      ideaDetails: `Idean nimi: ${idea.title}\nKuvaus: ${idea.description}`,
      projectDetails: `Projektin nimi: ${project.name}\nKuvaus: ${project.description}\nToimiala: ${project.domain}`
    };

    const response = await openaiService.createCompletion('hakija', message, promptData);

    // Luo hakemus
    const application = await Application.create({
      title: `Hakemus: ${idea.title}`,
      project: projectId,
      baseIdea: ideaId,
      owner: req.user.id,
      status: 'draft',
      sections: [
        {
          title: 'Projektin kuvaus',
          content: response,
          order: 0,
        },
      ],
      conversations: [
        {
          agent: 'user',
          message,
        },
        {
          agent: 'hakija',
          message: response,
        },
      ],
    });

    // Päivitä projekti
    project.applications.push(application._id);
    await project.save();

    res.status(200).json({
      success: true,
      data: {
        response,
        application,
      },
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
 * @desc    Arvioi hakemuksen Rahoittaja-agentin kanssa
 * @route   POST /api/agents/rahoittaja
 * @access  Private
 */
exports.reviewWithRahoittaja = async (req, res) => {
  try {
    const { applicationId, message } = req.body;

    // Tarkista, että hakemus on olemassa
    const application = await Application.findById(applicationId).populate('project');
    if (!application) {
      return res.status(404).json({
        success: false,
        message: 'Hakemusta ei löydy',
      });
    }

    // Tarkista, että käyttäjällä on oikeus hakemukseen
    const project = application.project;
    if (
      project.owner.toString() !== req.user.id && 
      !project.members.some(m => m.user.toString() === req.user.id)
    ) {
      return res.status(403).json({
        success: false,
        message: 'Ei oikeutta tähän hakemukseen',
      });
    }

    // Koosta hakemuksen sisältö
    let applicationContent = '';
    for (const section of application.sections) {
      applicationContent += `## ${section.title}\n${section.content}\n\n`;
    }

    // Käytä OpenAI-palvelua vastauksen luomiseen
    const promptData = {
      applicationDetails: `Hakemuksen nimi: ${application.title}\n\n${applicationContent}`,
      projectDetails: `Projektin nimi: ${project.name}\nKuvaus: ${project.description}\nToimiala: ${project.domain}`
    };

    const response = await openaiService.createCompletion('rahoittaja', message, promptData);

    // Päivitä hakemus
    application.status = 'review';
    application.conversations.push(
      {
        agent: 'user',
        message,
      },
      {
        agent: 'rahoittaja',
        message: response,
      }
    );

    // Lisää arviointi (yksinkertaistettu)
    application.reviews.push({
      reviewer: 'ai',
      overallScore: 75, // Oletusarviointi
      strengths: ['Vahva innovaatioulottuvuus'],
      weaknesses: ['Toteutussuunnitelmaa voisi tarkentaa'],
      improvements: ['Lisää konkreettisia mittareita vaikuttavuudelle'],
      createdAt: Date.now(),
    });

    await application.save();

    res.status(200).json({
      success: true,
      data: {
        response,
        application,
      },
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: 'Palvelinvirhe',
      error: error.message,
    });
  }
}; 