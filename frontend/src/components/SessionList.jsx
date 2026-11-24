import React from 'react';

function SessionList({ sessions, activeSessionId, onSelectSession, onDeleteSession, loading }) {
  return (
    <div className="session-list">
      {loading && sessions.length === 0 ? (
        <div className="loading">Loading sessions...</div>
      ) : sessions.length === 0 ? (
        <div className="no-sessions">No sessions yet</div>
      ) : (
        <ul>
          {sessions.map((session) => (
            <li
              key={session.id}
              className={`session-item ${activeSessionId === session.id ? 'active' : ''}`}
            >
              <div
                className="session-content"
                onClick={() => onSelectSession(session.id)}
              >
                <div className="session-title">{session.title}</div>
                <div className="session-meta">
                  {session.message_count} messages
                </div>
              </div>
              <button
                className="delete-btn"
                onClick={(e) => {
                  e.stopPropagation();
                  onDeleteSession(session.id);
                }}
                title="Delete session"
              >
                ×
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default SessionList;
