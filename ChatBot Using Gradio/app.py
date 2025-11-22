"""
Gradio ChatBot Interface using Google Gemini API
"""

import os
import gradio as gr
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Google Gemini API
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables. Please set it in .env file.")

genai.configure(api_key=API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")


# Gradio expects: [{'role': 'user', 'content': '...'}, {'role': 'assistant', 'content': '...'}]
def chat_with_gemini(message, history):
    try:
        # Convert Gradio history to Gemini format
        gemini_history = []
        for msg in history:
            if msg['role'] == 'user':
                gemini_history.append({"role": "user", "parts": [msg['content']]})
            elif msg['role'] == 'assistant':
                gemini_history.append({"role": "model", "parts": [msg['content']]})
        conversation = model.start_chat(history=gemini_history)
        response = conversation.send_message(message)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def gradio_chat(user_message, history):
    response = chat_with_gemini(user_message, history)
    history = history + [
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": response}
    ]
    return "", history

with gr.Blocks() as demo:
    gr.Markdown("# 🤖 Gemini ChatBot\nChat with Google's Gemini AI")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Type your message...")
    clear = gr.Button("Clear Chat")

    def reset():
        return [], ""

    msg.submit(gradio_chat, [msg, chatbot], [msg, chatbot])
    clear.click(reset, [], [chatbot, msg])

demo.launch(server_name="0.0.0.0", server_port=7861)


@app.route('/')
def index():
    """Render the main chat interface."""
    return render_template('index.html')
