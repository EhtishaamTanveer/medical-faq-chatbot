# src/models/model.py
import openai
from src.config import settings
import base64

class MedicalChatbot:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.model_name = "gpt-4o"
        self.max_tokens = settings.MAX_TOKENS
        self.temperature = settings.TEMPERATURE
        self.disclaimer = settings.MEDICAL_DISCLAIMER

        self.system_prompt = """
        You are a helpful medical information assistant that provides accurate, evidence-based information
        about medical symptoms, medications, and general health questions for **educational and research purposes only**. 
        You may describe anatomical structures, abnormalities, or technical aspects of medical images (like X-rays), **but do not provide a diagnosis**.
        
        Guidelines to follow:
        1. Provide accurate, evidence-based information from reliable sources
        2. Do not diagnose conditions or prescribe medications
        3. Clearly state when information is general and when a healthcare professional should be consulted
        4. Use simple, clear language to explain medical concepts
        5. If you don't know something or if it's outside your expertise, say so
        6. Format your responses in a readable way with bullet points for clarity when appropriate
        7. Reference past conversation context when appropriate
        8. If a medical image is provided, describe the image in detail, including anatomical structures and any abnormalities, but do not provide a diagnosis.
        
        Remember: You are providing information only, not medical advice. Hence, NEVER include language that implies professional medical advice.
        """

    def get_response(self, query, conversation_history=None, document_context=None, image_path=None):
        try:
            messages = [{"role": "system", "content": self.system_prompt}]

            if document_context:
                messages.append({
                    "role": "system",
                    "content": f"Document context:\n\n{document_context}"
                })

            if conversation_history:
                for user_msg, bot_msg in conversation_history:
                    messages.append({"role": "user", "content": user_msg})
                    messages.append({"role": "assistant", "content": bot_msg})

            if image_path:
                with open(image_path, "rb") as f:
                    image_bytes = f.read()

                messages.append({
                    "role": "user",
                    "content": [
                        {"type": "text", "text": query},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": "data:image/jpeg;base64," + base64.b64encode(image_bytes).decode()
                            }
                        }
                    ]
                })
            else:
                messages.append({"role": "user", "content": query})

            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )

            answer = response.choices[0].message.content.strip()
            return f"{answer}\n\n{self.disclaimer}"

        except Exception as e:
            return f"I'm sorry, I encountered an error while processing your question: {str(e)}"

