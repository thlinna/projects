const mongoose = require('mongoose');

const IdeaSchema = new mongoose.Schema(
  {
    title: {
      type: String,
      required: [true, 'Idean otsikko on pakollinen'],
      trim: true,
      maxlength: [200, 'Otsikko voi olla enintään 200 merkkiä pitkä'],
    },
    description: {
      type: String,
      required: [true, 'Kuvaus on pakollinen'],
    },
    project: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Project',
      required: true,
    },
    creator: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',
    },
    status: {
      type: String,
      enum: ['draft', 'pending', 'reviewed', 'approved', 'rejected'],
      default: 'draft',
    },
    strengths: [{
      type: String,
    }],
    weaknesses: [{
      type: String,
    }],
    suggestions: [{
      type: String,
    }],
    tags: [{
      type: String,
      trim: true,
    }],
    // Ideanikkari-agentin tuottama
    isAIGenerated: {
      type: Boolean,
      default: false,
    },
    // Arvioija-agentin arviot
    reviews: [{
      reviewer: {
        type: String,
        enum: ['user', 'ai'],
        default: 'ai',
      },
      score: {
        type: Number,
        min: 0,
        max: 10,
      },
      comment: String,
      createdAt: {
        type: Date,
        default: Date.now,
      },
    }],
    // Keskusteluhistoria
    conversations: [{
      agent: {
        type: String,
        required: true,
        enum: ['ideanikkari', 'arvioija', 'hakija', 'rahoittaja', 'user'],
      },
      message: {
        type: String,
        required: true,
      },
      createdAt: {
        type: Date,
        default: Date.now,
      },
    }],
  },
  {
    timestamps: true,
  }
);

module.exports = mongoose.model('Idea', IdeaSchema); 