import json
from typing import Dict, Optional
from datetime import datetime, timedelta

# In-memory session store (use Redis for production)
session_storage: Dict[str, Dict] = {}

def get_session_id(message_sender: str, message_timestamp: str) -> str:
    """Generate consistent session ID"""
    # Simple hash based on sender and date
    date_str = message_timestamp.split('T')[0]
    return f"{message_sender}_{date_str}"

def save_session(session_id: str, data: Dict) -> None:
    """Save session data"""
    data['last_updated'] = datetime.now().isoformat()
    session_storage[session_id] = data

def load_session(session_id: str) -> Optional[Dict]:
    """Load session data"""
    return session_storage.get(session_id)

def initialize_session(session_id: str) -> Dict:
    """Initialize new session"""
    session_data = {
        "turn_count": 0,
        "created_at": datetime.now().isoformat(),
        "intelligence_extracted": False
    }
    save_session(session_id, session_data)
    return session_data
