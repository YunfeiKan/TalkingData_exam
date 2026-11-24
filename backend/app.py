"""
Cloud Agent Assistant Workbench Backend
"""
import os
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "https://showmevibecode.up.railway.app/api/model/v1")
API_KEY = os.getenv("API_KEY", "exam_PDOKG1XU21r1sX6gK4Dxi-f_M6kdUjt96Ve-CKfL0VQ")
MODEL_NAME = os.getenv("MODEL_NAME", "linext-5.3-luna")
DATA_DIR = Path(os.getenv("DATA_DIR", "./data"))
DATA_DIR.mkdir(exist_ok=True)

SESSIONS_DIR = DATA_DIR / "sessions"
SESSIONS_DIR.mkdir(exist_ok=True)

# Session and Message Management
@dataclass
class Message:
    id: str
    role: str  # user or assistant
    content: str
    timestamp: str
    tool_calls: Optional[List[Dict[str, Any]]] = None

@dataclass
class Session:
    id: str
    title: str
    description: str
    created_at: str
    updated_at: str
    status: str  # active, completed, archived
    messages: List[Message]
    metadata: Dict[str, Any]

class SessionManager:
    @staticmethod
    def _session_path(session_id: str) -> Path:
        return SESSIONS_DIR / f"{session_id}.json"
    
    @staticmethod
    def create_session(title: str, description: str = "") -> Session:
        session_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        session = Session(
            id=session_id,
            title=title,
            description=description,
            created_at=now,
            updated_at=now,
            status="active",
            messages=[],
            metadata={"task_count": 0}
        )
        SessionManager.save_session(session)
        return session
    
    @staticmethod
    def save_session(session: Session) -> None:
        path = SessionManager._session_path(session.id)
        data = {
            "id": session.id,
            "title": session.title,
            "description": session.description,
            "created_at": session.created_at,
            "updated_at": datetime.utcnow().isoformat(),
            "status": session.status,
            "messages": [
                {
                    "id": msg.id,
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp,
                    "tool_calls": msg.tool_calls
                }
                for msg in session.messages
            ],
            "metadata": session.metadata
        }
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
    
    @staticmethod
    def load_session(session_id: str) -> Optional[Session]:
        path = SessionManager._session_path(session_id)
        if not path.exists():
            return None
        
        with open(path, 'r') as f:
            data = json.load(f)
        
        messages = [
            Message(
                id=msg.get("id", str(uuid.uuid4())),
                role=msg["role"],
                content=msg["content"],
                timestamp=msg.get("timestamp", datetime.utcnow().isoformat()),
                tool_calls=msg.get("tool_calls")
            )
            for msg in data.get("messages", [])
        ]
        
        return Session(
            id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            status=data.get("status", "active"),
            messages=messages,
            metadata=data.get("metadata", {})
        )
    
    @staticmethod
    def list_sessions() -> List[Session]:
        sessions = []
        for path in SESSIONS_DIR.glob("*.json"):
            session = SessionManager.load_session(path.stem)
            if session:
                sessions.append(session)
        return sorted(sessions, key=lambda s: s.created_at, reverse=True)

class AgentEngine:
    """Agent execution engine using external LLM API"""
    
    @staticmethod
    def call_llm(messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """Call the LLM API"""
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": MODEL_NAME,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 2000
        }
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/chat/completions",
                json=payload,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            else:
                return "Error: Unexpected API response format"
        except Exception as e:
            return f"Error calling LLM: {str(e)}"
    
    @staticmethod
    def process_message(session: Session, user_message: str) -> str:
        """Process user message and generate agent response"""
        # Build conversation history for context
        messages = []
        
        # Add system prompt
        system_prompt = """You are a helpful AI assistant in a cloud-based workbench.
You help users with:
1. Code development and debugging
2. File processing and analysis
3. Report writing and documentation
4. Data analysis and visualization
5. General task assistance

Be concise, practical, and provide working solutions. When appropriate, provide code snippets, file recommendations, or step-by-step guidance.
If the user asks for code, provide complete, runnable examples."""
        
        messages.append({
            "role": "system",
            "content": system_prompt
        })
        
        # Add conversation history
        for msg in session.messages[-10:]:  # Keep last 10 messages for context
            messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        # Get response from LLM
        response = AgentEngine.call_llm(messages)
        return response

# API Routes
@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "data_dir": str(DATA_DIR)
    })

@app.route("/api/sessions", methods=["GET"])
def list_sessions():
    """List all sessions"""
    sessions = SessionManager.list_sessions()
    return jsonify({
        "sessions": [
            {
                "id": s.id,
                "title": s.title,
                "description": s.description,
                "created_at": s.created_at,
                "updated_at": s.updated_at,
                "status": s.status,
                "message_count": len(s.messages),
                "metadata": s.metadata
            }
            for s in sessions
        ]
    })

@app.route("/api/sessions", methods=["POST"])
def create_session():
    """Create a new session"""
    data = request.json or {}
    title = data.get("title", "New Session")
    description = data.get("description", "")
    
    session = SessionManager.create_session(title, description)
    
    return jsonify({
        "id": session.id,
        "title": session.title,
        "description": session.description,
        "created_at": session.created_at,
        "status": session.status,
        "message_count": 0
    }), 201

@app.route("/api/sessions/<session_id>", methods=["GET"])
def get_session(session_id: str):
    """Get session details"""
    session = SessionManager.load_session(session_id)
    if not session:
        return jsonify({"error": "Session not found"}), 404
    
    return jsonify({
        "id": session.id,
        "title": session.title,
        "description": session.description,
        "created_at": session.created_at,
        "updated_at": session.updated_at,
        "status": session.status,
        "messages": [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp
            }
            for msg in session.messages
        ],
        "metadata": session.metadata
    })

@app.route("/api/sessions/<session_id>/messages", methods=["POST"])
def send_message(session_id: str):
    """Send a message and get agent response"""
    session = SessionManager.load_session(session_id)
    if not session:
        return jsonify({"error": "Session not found"}), 404
    
    data = request.json or {}
    user_content = data.get("message", "").strip()
    
    if not user_content:
        return jsonify({"error": "Message cannot be empty"}), 400
    
    # Add user message
    user_msg = Message(
        id=str(uuid.uuid4()),
        role="user",
        content=user_content,
        timestamp=datetime.utcnow().isoformat()
    )
    session.messages.append(user_msg)
    
    # Get agent response
    agent_response = AgentEngine.process_message(session, user_content)
    
    agent_msg = Message(
        id=str(uuid.uuid4()),
        role="assistant",
        content=agent_response,
        timestamp=datetime.utcnow().isoformat()
    )
    session.messages.append(agent_msg)
    
    # Update metadata
    session.metadata["task_count"] = session.metadata.get("task_count", 0) + 1
    
    # Save session
    SessionManager.save_session(session)
    
    return jsonify({
        "user_message": {
            "id": user_msg.id,
            "role": "user",
            "content": user_msg.content,
            "timestamp": user_msg.timestamp
        },
        "agent_message": {
            "id": agent_msg.id,
            "role": "assistant",
            "content": agent_response,
            "timestamp": agent_msg.timestamp
        }
    }), 201

@app.route("/api/sessions/<session_id>", methods=["PATCH"])
def update_session(session_id: str):
    """Update session metadata"""
    session = SessionManager.load_session(session_id)
    if not session:
        return jsonify({"error": "Session not found"}), 404
    
    data = request.json or {}
    
    if "title" in data:
        session.title = data["title"]
    if "description" in data:
        session.description = data["description"]
    if "status" in data:
        session.status = data["status"]
    
    SessionManager.save_session(session)
    
    return jsonify({
        "id": session.id,
        "title": session.title,
        "description": session.description,
        "status": session.status,
        "updated_at": session.updated_at
    })

@app.route("/api/sessions/<session_id>", methods=["DELETE"])
def delete_session(session_id: str):
    """Delete a session"""
    path = SessionManager._session_path(session_id)
    if path.exists():
        path.unlink()
        return jsonify({"status": "deleted"}), 200
    return jsonify({"error": "Session not found"}), 404

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
