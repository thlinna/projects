import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// Konfiguroi axios
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Lisää tokenin Authorization-headeriin
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Käyttäjähallinta
export const userAPI = {
  register: (userData) => api.post('/api/users', userData),
  login: (credentials) => api.post('/api/users/login', credentials),
  getMe: () => api.get('/api/users/me'),
  updateProfile: (userData) => api.put('/api/users', userData),
  updatePassword: (passwordData) => api.put('/api/users/password', passwordData),
  forgotPassword: (email) => api.post('/api/users/forgotpassword', { email }),
  resetPassword: (token, password) => api.put(`/api/users/resetpassword/${token}`, { password }),
};

// Projektihallinta
export const projectAPI = {
  getProjects: () => api.get('/api/projects'),
  getProject: (id) => api.get(`/api/projects/${id}`),
  createProject: (projectData) => api.post('/api/projects', projectData),
  updateProject: (id, projectData) => api.put(`/api/projects/${id}`, projectData),
  deleteProject: (id) => api.delete(`/api/projects/${id}`),
  addMember: (projectId, memberData) => api.post(`/api/projects/${projectId}/members`, memberData),
  removeMember: (projectId, userId) => api.delete(`/api/projects/${projectId}/members/${userId}`),
};

// Ideahallinta
export const ideaAPI = {
  getIdeas: (projectId) => api.get(`/api/projects/${projectId}/ideas`),
  getIdea: (id) => api.get(`/api/ideas/${id}`),
  createIdea: (ideaData) => api.post('/api/ideas', ideaData),
  updateIdea: (id, ideaData) => api.put(`/api/ideas/${id}`, ideaData),
  deleteIdea: (id) => api.delete(`/api/ideas/${id}`),
};

// Hakemushallinta
export const applicationAPI = {
  getApplications: (projectId) => api.get(`/api/projects/${projectId}/applications`),
  getApplication: (id) => api.get(`/api/applications/${id}`),
  createApplication: (applicationData) => api.post('/api/applications', applicationData),
  updateApplication: (id, applicationData) => api.put(`/api/applications/${id}`, applicationData),
  deleteApplication: (id) => api.delete(`/api/applications/${id}`),
  addSection: (applicationId, sectionData) => api.post(`/api/applications/${applicationId}/sections`, sectionData),
  updateSection: (applicationId, sectionId, sectionData) => api.put(`/api/applications/${applicationId}/sections/${sectionId}`, sectionData),
  deleteSection: (applicationId, sectionId) => api.delete(`/api/applications/${applicationId}/sections/${sectionId}`),
};

// Tekoälyagentit
export const agentAPI = {
  ideateWithIdeanikkari: (data) => api.post('/api/agents/ideanikkari', data),
  evaluateWithArvioija: (data) => api.post('/api/agents/arvioija', data),
  createApplicationWithHakija: (data) => api.post('/api/agents/hakija', data),
  reviewWithRahoittaja: (data) => api.post('/api/agents/rahoittaja', data),
};

export default api; 