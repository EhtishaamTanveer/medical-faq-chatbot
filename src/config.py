import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Model Configuration
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", 500))
    TEMPERATURE = float(os.getenv("TEMPERATURE", 0.3))
    
    # Application Settings
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    
    # Medical disclaimer that will be added to responses
    MEDICAL_DISCLAIMER = """
    DISCLAIMER: This information is for educational purposes only and is not intended as a substitute 
    for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician 
    or other qualified health provider with any questions regarding a medical condition.
    """

settings = Settings()