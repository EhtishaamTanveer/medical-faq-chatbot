# src/utils/helpers.py
import re
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def sanitize_input(text):
    """Sanitize user input to prevent injection attacks"""
    # Remove any HTML/script tags
    sanitized = re.sub(r'<[^>]*>', '', text)
    return sanitized

def log_user_query(query, response):
    """Log user queries and responses for monitoring (no PII stored)"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Hash or anonymize the query if it might contain PII
    logger.info(f"[{timestamp}] Query length: {len(query)} chars, Response length: {len(response)} chars")

def categorize_medical_query(query):
    """Categorize the query into predefined medical topics"""
    query_lower = query.lower()
    
    categories = {
        "symptoms": ["symptom", "feel", "pain", "ache", "discomfort", "experiencing"],
        "medication": ["medicine", "drug", "prescription", "dosage", "pill", "medication", "side effect"],
        "reports": ["report", "test", "result", "level", "reading", "scan", "mri", "ct", "xray", "lab"],
        "general": ["what is", "how to", "can you explain", "tell me about"]
    }
    
    for category, keywords in categories.items():
        if any(keyword in query_lower for keyword in keywords):
            return category
    
    return "general"