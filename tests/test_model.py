# tests/test_model.py
import pytest
from unittest.mock import patch, MagicMock
from src.models.model import MedicalChatbot
from src.utils.helpers import sanitize_input, categorize_medical_query

# Test the MedicalChatbot class
@pytest.fixture
def chatbot():
    with patch('openai.ChatCompletion.create') as mock_create:
        # Mock the OpenAI API response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Test response"))]
        mock_create.return_value = mock_response
        
        yield MedicalChatbot()

def test_chatbot_initialization(chatbot):
    assert chatbot.model_name is not None
    assert chatbot.system_prompt is not None
    assert "medical" in chatbot.system_prompt.lower()

def test_chatbot_get_response(chatbot):
    response = chatbot.get_response("What are the symptoms of the flu?")
    assert response is not None
    assert "Test response" in response
    assert "DISCLAIMER" in response

# Test helper functions
def test_sanitize_input():
    input_text = "<script>alert('XSS')</script> What are the symptoms of the flu?"
    sanitized = sanitize_input(input_text)
    assert "<script>" not in sanitized
    assert "What are the symptoms of the flu?" in sanitized

def test_categorize_medical_query():
    # Test symptom category
    assert categorize_medical_query("I have pain in my back") == "symptoms"
    
    # Test medication category
    assert categorize_medical_query("What are side effects of aspirin?") == "medication"
    
    # Test reports category
    assert categorize_medical_query("What does high cholesterol in my blood test mean?") == "reports"
    
    # Test general category
    assert categorize_medical_query("Can you explain what diabetes is?") == "general"