import React, { useState, useEffect, useRef } from 'react';

function ChatWindow({ session, onSendMessage, loading }) {
  const [message, setMessage] = useState('');
  const messagesEndRef = useRef(null);

  useEffect(() => {
    scrollToBottom();
  }, [session.messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim()) {
      onSendMessage(message);
      setMessage('');
    }
  };

  return (
    <div className="chat-window">
      <div className="chat-header">
        <div className="chat-title">{session.title}</div>
        {session.description && (
          <div className="chat-description">{session.description}</div>
        )}
      </div>

      <div className="messages-container">
        {session.messages.length === 0 ? (
          <div className="empty-messages">
            <p>No messages yet. Start a conversation!</p>
          </div>
        ) : (
          session.messages.map((msg) => (
            <div key={msg.id} className={`message message-${msg.role}`}>
              <div className="message-role">
                {msg.role === 'user' ? '👤 You' : '🤖 Agent'}
              </div>
              <div className="message-content">
                {msg.content.split('\n').map((line, idx) => (
                  <div key={idx}>{line}</div>
                ))}
              </div>
              <div className="message-time">
                {new Date(msg.timestamp).toLocaleTimeString()}
              </div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      <form className="message-input-form" onSubmit={handleSubmit}>
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type your message here... (Press Enter to send, Shift+Enter for new line)"
          onKeyPress={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              handleSubmit(e);
            }
          }}
          disabled={loading}
          rows="3"
        />
        <button
          type="submit"
          className="send-btn"
          disabled={loading || !message.trim()}
        >
          {loading ? 'Sending...' : 'Send'}
        </button>
      </form>
    </div>
  );
}

export default ChatWindow;
