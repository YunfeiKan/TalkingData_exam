import axios from 'axios';

// Use relative API path for compatibility with Docker and production
const API_BASE = process.env.REACT_APP_API_URL || '/api';

export const api = {
  // Session management
  listSessions: () => axios.get(`${API_BASE}/sessions`),
  createSession: (title, description) =>
    axios.post(`${API_BASE}/sessions`, { title, description }),
  getSession: (sessionId) => axios.get(`${API_BASE}/sessions/${sessionId}`),
  updateSession: (sessionId, data) =>
    axios.patch(`${API_BASE}/sessions/${sessionId}`, data),
  deleteSession: (sessionId) => axios.delete(`${API_BASE}/sessions/${sessionId}`),
  
  // Messages
  sendMessage: (sessionId, message) =>
    axios.post(`${API_BASE}/sessions/${sessionId}/messages`, { message }),
  
  // Health check
  health: () => axios.get(`${API_BASE}/health`)
};
