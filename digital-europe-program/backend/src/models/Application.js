const mongoose = require('mongoose');

const ApplicationSchema = new mongoose.Schema(
  {
    title: {
      type: String,
      required: [true, 'Hakemuksen otsikko on pakollinen'],
      trim: true,
      maxlength: [200, 'Otsikko voi olla enintään 200 merkkiä pitkä'],
    },
    project: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Project',
      required: true,
    },
    baseIdea: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Idea',
    },
    owner: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',
      required: true,
    },
    status: {
      type: String,
      enum: ['draft', 'review', 'finalized', 'submitted'],
      default: 'draft',
    },
    // Hakemuksen osiot
    sections: [
      {
        title: {
          type: String,
          required: true,
        },
        content: {
          type: String,
          required: true,
        },
        order: {
          type: Number,
          default: 0,
        },
      },
    ],
    // Rahoittaja-agentin arviot
    reviews: [
      {
        reviewer: {
          type: String,
          enum: ['user', 'ai'],
          default: 'ai',
        },
        overallScore: {
          type: Number,
          min: 0,
          max: 100,
        },
        sectionScores: [
          {
            section: String,
            score: {
              type: Number,
              min: 0,
              max: 10,
            },
            comments: String,
          },
        ],
        strengths: [String],
        weaknesses: [String],
        improvements: [String],
        createdAt: {
          type: Date,
          default: Date.now,
        },
      },
    ],
    // Keskusteluhistoria
    conversations: [
      {
        agent: {
          type: String,
          required: true,
          enum: ['hakija', 'rahoittaja', 'user'],
        },
        message: {
          type: String,
          required: true,
        },
        createdAt: {
          type: Date,
          default: Date.now,
        },
      },
    ],
    // Metatiedot
    metaData: {
      fundingAmount: {
        type: Number,
      },
      duration: {
        type: String,
      },
      startDate: {
        type: Date,
      },
      endDate: {
        type: Date,
      },
      partners: [
        {
          name: String,
          role: String,
        },
      ],
      targetProgramPriorities: [String],
    },
    // Versiohistoria
    versions: [
      {
        version: Number,
        createdAt: {
          type: Date,
          default: Date.now,
        },
        createdBy: {
          type: mongoose.Schema.Types.ObjectId,
          ref: 'User',
        },
        snapshot: Object,
      },
    ],
  },
  {
    timestamps: true,
  }
);

module.exports = mongoose.model('Application', ApplicationSchema); 