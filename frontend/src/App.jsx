import React, { useState, useEffect } from 'react';
import { api } from './api';
import SessionList from './components/SessionList';
import ChatWindow from './components/ChatWindow';
import './App.css';

function App() {
  const [sessions, setSessions] = useState([]);
  const [activeSessionId, setActiveSessionId] = useState(null);
  const [activeSession, setActiveSession] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showNewSessionForm, setShowNewSessionForm] = useState(false);

  // Load sessions on mount
  useEffect(() => {
    loadSessions();
  }, []);

  // Load active session when ID changes
  useEffect(() => {
    if (activeSessionId) {
      loadSession(activeSessionId);
    }
  }, [activeSessionId]);

  const loadSessions = async () => {
    try {
      setLoading(true);
      const response = await api.listSessions();
      setSessions(response.data.sessions || []);
      setError(null);
    } catch (err) {
      setError('Failed to load sessions: ' + err.message);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const loadSession = async (sessionId) => {
    try {
      setLoading(true);
      const response = await api.getSession(sessionId);
      setActiveSession(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load session: ' + err.message);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateSession = async (title, description) => {
    try {
      setLoading(true);
      const response = await api.createSession(title, description);
      const newSession = {
        ...response.data,
        messages: []
      };
      setSessions([newSession, ...sessions]);
      setActiveSessionId(newSession.id);
      setShowNewSessionForm(false);
      setError(null);
    } catch (err) {
      setError('Failed to create session: ' + err.message);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async (message) => {
    if (!activeSessionId) return;
    
    try {
      setLoading(true);
      const response = await api.sendMessage(activeSessionId, message);
      
      // Update active session with new messages
      setActiveSession(prev => ({
        ...prev,
        messages: [
          ...prev.messages,
          response.data.user_message,
          response.data.agent_message
        ]
      }));
      
      // Reload sessions to update message count and updated_at
      await loadSessions();
      setError(null);
    } catch (err) {
      setError('Failed to send message: ' + err.message);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteSession = async (sessionId) => {
    if (!confirm('Are you sure you want to delete this session?')) return;
    
    try {
      await api.deleteSession(sessionId);
      setSessions(sessions.filter(s => s.id !== sessionId));
      if (activeSessionId === sessionId) {
        setActiveSessionId(null);
        setActiveSession(null);
      }
      setError(null);
    } catch (err) {
      setError('Failed to delete session: ' + err.message);
      console.error(err);
    }
  };

  return (
    <div className="app">
      <div className="sidebar">
        <div className="sidebar-header">
          <h1>🤖 Agent Workbench</h1>
          <button
            className="new-session-btn"
            onClick={() => setShowNewSessionForm(!showNewSessionForm)}
          >
            + New
          </button>
        </div>

        {showNewSessionForm && (
          <NewSessionForm
            onSubmit={handleCreateSession}
            onCancel={() => setShowNewSessionForm(false)}
          />
        )}

        <SessionList
          sessions={sessions}
          activeSessionId={activeSessionId}
          onSelectSession={setActiveSessionId}
          onDeleteSession={handleDeleteSession}
          loading={loading}
        />

        {error && <div className="error-message">{error}</div>}
      </div>

      <div className="main-content">
        {activeSession ? (
          <ChatWindow
            session={activeSession}
            onSendMessage={handleSendMessage}
            loading={loading}
          />
        ) : (
          <div className="empty-state">
            <div className="empty-icon">📝</div>
            <h2>Welcome to Agent Workbench</h2>
            <p>Create a new session or select an existing one to get started.</p>
          </div>
        )}
      </div>
    </div>
  );
}

function NewSessionForm({ onSubmit, onCancel }) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (title.trim()) {
      onSubmit(title, description);
      setTitle('');
      setDescription('');
    }
  };

  return (
    <form className="new-session-form" onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Session title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        autoFocus
      />
      <textarea
        placeholder="Description (optional)"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        rows="2"
      />
      <div className="form-buttons">
        <button type="submit" className="btn-submit">Create</button>
        <button type="button" className="btn-cancel" onClick={onCancel}>
          Cancel
        </button>
      </div>
    </form>
  );
}

export default App;
