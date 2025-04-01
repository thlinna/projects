const mongoose = require('mongoose');

const ProjectSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: [true, 'Projektin nimi on pakollinen'],
      trim: true,
      maxlength: [100, 'Nimi voi olla enintään 100 merkkiä pitkä'],
    },
    description: {
      type: String,
      required: [true, 'Kuvaus on pakollinen'],
      maxlength: [1000, 'Kuvaus voi olla enintään 1000 merkkiä pitkä'],
    },
    domain: {
      type: String,
      required: [true, 'Toimiala on pakollinen'],
      trim: true,
    },
    status: {
      type: String,
      enum: ['draft', 'idea', 'evaluation', 'application', 'review', 'completed'],
      default: 'draft',
    },
    owner: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',
      required: true,
    },
    members: [
      {
        user: {
          type: mongoose.Schema.Types.ObjectId,
          ref: 'User',
        },
        role: {
          type: String,
          enum: ['viewer', 'editor', 'admin'],
          default: 'viewer',
        },
      },
    ],
    ideas: [
      {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Idea',
      },
    ],
    applications: [
      {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Application',
      },
    ],
    tags: [
      {
        type: String,
        trim: true,
      },
    ],
  },
  {
    timestamps: true,
  }
);

// Virtuaalit

// Staattinen metodi hakeaksesi projektit käyttäjän ID:n perusteella
ProjectSchema.statics.getProjectsByUser = async function (userId) {
  return this.find({
    $or: [
      { owner: userId },
      { 'members.user': userId },
    ],
  }).populate('owner', 'name email');
};

module.exports = mongoose.model('Project', ProjectSchema); 