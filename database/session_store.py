import json
from typing import Dict, Optional
from datetime import datetime
import hashlib

# In-memory session store (use Redis for production)
session_storage: Dict[str, Dict] = {}

def get_session_id(message_sender: str, message_timestamp: str) -> str:
    """Generate consistent session ID with error handling"""
    try:
        # Convert timestamp to string if it's not
        timestamp_str = str(message_timestamp)
        
        # Try to extract date from ISO format
        if 'T' in timestamp_str:
            date_str = timestamp_str.split('T')[0]
        else:
            # Fallback: use current date
            date_str = datetime.now().strftime('%Y-%m-%d')
        
        # Create session ID
        session_id = f"{message_sender}_{date_str}"
        
        return session_id
        
    except Exception as e:
        # Ultimate fallback: generate hash-based ID
        print(f"⚠️ Session ID generation error: {e}")
        unique_string = f"{message_sender}_{message_timestamp}_{datetime.now().isoformat()}"
        return hashlib.md5(unique_string.encode()).hexdigest()

def save_session(session_id: str, data: Dict) -> None:
    """Save session data with error handling"""
    try:
        data['last_updated'] = datetime.now().isoformat()
        session_storage[session_id] = data
    except Exception as e:
        print(f"❌ Session save error: {e}")

def load_session(session_id: str) -> Optional[Dict]:
    """Load session data"""
    try:
        return session_storage.get(session_id)
    except Exception as e:
        print(f"❌ Session load error: {e}")
        return None

def initialize_session(session_id: str) -> Dict:
    """Initialize new session with error handling"""
    try:
        session_data = {
            "turn_count": 0,
            "created_at": datetime.now().isoformat(),
            "intelligence_extracted": False
        }
        save_session(session_id, session_data)
        return session_data
    except Exception as e:
        print(f"❌ Session init error: {e}")
        return {
            "turn_count": 0,
            "created_at": datetime.now().isoformat(),
            "intelligence_extracted": False
        }
