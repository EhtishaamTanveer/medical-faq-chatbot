import gradio as gr
from src.models.model import MedicalChatbot
from src.utils.document_processor import DocumentProcessor

processor = DocumentProcessor()
chatbot = MedicalChatbot()
document_context = ""  # Holds extracted text from PDF

example_queries = [
    "What are common symptoms of diabetes?",
    "What does this X-ray show?",
    "Summarize the lab report I uploaded.",
    "Is there any sign of pneumonia in the X-ray?",
]

def create_gradio_app():
    with gr.Blocks(
        title="Medical FAQ Assistant",
        theme=gr.themes.Soft(),
        css="""
            body {
                background: linear-gradient(to bottom right, #f7e8ec, #c0e0f8);
                font-family: 'Garamond', serif;
            }

            .gr-block.gr-box {
                border-radius: 16px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
                padding: 30px;
                max-width: 850px;
                margin: 40px auto;
                background: white;
            }

            .disclaimer {
                background-color: #fffbe6;
                border-left: 4px solid #ffcc00;
                padding: 12px 16px;
                margin-top: 30px;
                border-radius: 8px;
                font-size: 0.9rem;
                line-height: 1.5;
            }

            .chatbot .message.user {
                text-align: right;
                margin: 10px 0;
            }

            .chatbot .message.bot {
                display: flex;
                align-items: flex-start;
                gap: 10px;
                margin: 10px 0;
            }

            .chatbot .message.bot img {
                width: 32px;
                height: 32px;
                border-radius: 50%;
                margin-top: 4px;
            }

            .bubble {
                padding: 10px 14px;
                border-radius: 16px;
                display: inline-block;
                max-width: 75%;
                font-size: 0.95rem;
            }

            .user .bubble {
                background: #3399cc;
                color: white;
                border-bottom-right-radius: 0;
            }

            .bot .bubble {
                background: #f0fff4;
                color: #2b4d3f;
                border-bottom-left-radius: 0;
            }
        """
    ) as app:
        gr.Markdown("<h1 style='text-align: center; color: #3399cc;'>🩺 Medical FAQ Assistant</h1>")
        gr.Markdown(
            "<p style='text-align: center; font-size: 1.05rem;'>This chatbot provides general medical information about symptoms, medications, and health topics.<br>It is not a substitute for professional medical advice, diagnosis, or treatment.</p>"
        )

        chatbot_ui = gr.Chatbot(
            show_label=False,
            label="Chat",
            avatar_images=(None, "static/img/avatar.webp"),
            bubble_full_width=False,
            render_markdown=True,
            height=500,
            elem_classes=["chatbot"]
        )

        with gr.Row():
            user_input = gr.Textbox(placeholder="Type your medical question here...", scale=8)
            image_input = gr.Image(type="filepath", label=None)
            file_input = gr.File(file_types=[".pdf"], label=None)
            submit_btn = gr.Button("Send", scale=1)

        with gr.Row():
            gr.Examples(example_queries, inputs=user_input)

        gr.Markdown(
            "<div class='disclaimer'><strong>❗ Disclaimer:</strong><br>This chatbot provides general medical information for educational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for medical concerns.</div>"
        )

        # 🔁 Chat logic
        def chat_submit(message, history, image_path, file):
            global document_context

            if not message.strip():
                return "", history

            # Limit history to last 4 exchanges
            history = history or []
            clipped_history = history[-4:]

            # Process PDF if uploaded
            if file is not None:
                document_context = processor.extract_text(file.name)
            else:
                document_context = ""

            # Process image (filepath or None)
            image_path = image_path if image_path else None
            
            # Add this just before calling the model
            prefixed_query = f"""This image or document is being shared for educational and research purposes only.
            Please describe what you see, focusing on anatomical structures, visual patterns, or general abnormalities.

            DO NOT provide a diagnosis or medical opinion.

            {message}
            """

            # Get response from chatbot
            response = chatbot.get_response(
                query=prefixed_query,
                conversation_history=clipped_history,
                document_context=document_context,
                image_path=image_path
            )

            clipped_history.append([message, response])
            return "", clipped_history

        submit_btn.click(
            chat_submit,
            inputs=[user_input, chatbot_ui, image_input, file_input],
            outputs=[user_input, chatbot_ui]
        )

        user_input.submit(
            chat_submit,
            inputs=[user_input, chatbot_ui, image_input, file_input],
            outputs=[user_input, chatbot_ui]
        )

    return app

# Standalone
if __name__ == "__main__":
    app = create_gradio_app()
    app.launch()
