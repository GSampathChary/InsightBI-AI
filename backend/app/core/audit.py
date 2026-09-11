"""
InsightBI AI — Security Audit Logger (backend/app/core/audit.py)
Logs structured security events (logins, access denied events, role changes).
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional

AUDIT_LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "logs"))
os.makedirs(AUDIT_LOG_DIR, exist_ok=True)
AUDIT_LOG_FILE = os.path.join(AUDIT_LOG_DIR, "security_audit.log")

class AuditLogger:
    def __init__(self, log_file: str = AUDIT_LOG_FILE):
        self.log_file = log_file

    def log_event(self, event_type: str, user_email: str, status: str, details: Optional[Dict[str, Any]] = None):
        """Writes structured JSON audit entry to log file."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "user_email": user_email,
            "status": status,
            "details": details or {}
        }
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

audit_logger = AuditLogger()

def log_security_event(event_type: str, user_email: str, status: str, details: Optional[Dict[str, Any]] = None):
    audit_logger.log_event(event_type, user_email, status, details)
