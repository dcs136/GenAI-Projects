# Quick Start Guide - Gemini Edition

Get your GenAI Flask app running in 15 minutes!

## 1. Get Your API Key (2 minutes)

1. Visit https://makersuite.google.com/app/apikey
2. Click "Get API Key"
3. Create a new project or select existing one
4. Copy the API key

## 2. Set Up Your Environment (5 minutes)

### On Windows (PowerShell):
```powershell
# Create project directory
mkdir genai_flask_app
cd genai_flask_app

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Set API key
$env:GOOGLE_API_KEY = "YOUR_API_KEY_HERE"

# Install dependencies
pip install google-generativeai langchain langchain-google-genai Flask pydantic
```

### On Linux/Mac:
```bash
# Create project directory
mkdir genai_flask_app
cd genai_flask_app

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Set API key
export GOOGLE_API_KEY="YOUR_API_KEY_HERE"

# Install dependencies
pip install google-generativeai langchain langchain-google-genai Flask pydantic
```

## 3. Create the Files

### File 1: `config.py`
```python
import os

# Model configuration
PARAMETERS = {
    "temperature": 0.7,
    "max_output_tokens": 256,
}

# API configuration
API_KEY = os.getenv("GOOGLE_API_KEY")

# Available models
GEMINI_FLASH_MODEL = "gemini-1.5-flash"  # Fast & cost-effective
GEMINI_PRO_MODEL = "gemini-1.5-pro"      # Advanced reasoning
```

### File 2: `model.py`
```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from config import PARAMETERS, API_KEY, GEMINI_FLASH_MODEL, GEMINI_PRO_MODEL
import os

# Define output structure
class AIResponse(BaseModel):
    summary: str = Field(description="Summary of the user's message")
    sentiment: int = Field(description="Sentiment score from 0 (negative) to 100 (positive)")
    response: str = Field(description="Suggested response to the user")

json_parser = JsonOutputParser(pydantic_object=AIResponse)

# Initialize models
def initialize_model(model_id, api_key):
    return ChatGoogleGenerativeAI(
        model=model_id,
        google_api_key=api_key,
        temperature=PARAMETERS.get("temperature", 0.7),
    )

api_key = os.getenv("GOOGLE_API_KEY")
gemini_flash_llm = initialize_model(GEMINI_FLASH_MODEL, api_key)
gemini_pro_llm = initialize_model(GEMINI_PRO_MODEL, api_key)

# Prompt template
gemini_template = PromptTemplate(
    template="{system_prompt}\n\n{format_prompt}\n\nUser: {user_prompt}",
    input_variables=["system_prompt", "format_prompt", "user_prompt"]
)

# Response function
def get_ai_response(model, template, system_prompt, user_prompt):
    chain = template | model | json_parser
    return chain.invoke({
        'system_prompt': system_prompt,
        'user_prompt': user_prompt,
        'format_prompt': json_parser.get_format_instructions()
    })

# Model-specific functions
def gemini_flash_response(system_prompt, user_prompt):
    return get_ai_response(gemini_flash_llm, gemini_template, system_prompt, user_prompt)

def gemini_pro_response(system_prompt, user_prompt):
    return get_ai_response(gemini_pro_llm, gemini_template, system_prompt, user_prompt)
```

### File 3: `app.py`
```python
from flask import Flask, request, jsonify, render_template
from model import gemini_flash_response, gemini_pro_response
import time

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    user_message = data.get('message')
    model = data.get('model')

    if not user_message or not model:
        return jsonify({"error": "Missing message or model selection"}), 400

    system_prompt = "You are an AI assistant helping with customer inquiries. Provide a helpful and concise response."
    start_time = time.time()

    try:
        if model == 'gemini-flash':
            result = gemini_flash_response(system_prompt, user_message)
        elif model == 'gemini-pro':
            result = gemini_pro_response(system_prompt, user_message)
        else:
            return jsonify({"error": "Invalid model selection"}), 400

        result['duration'] = time.time() - start_time
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

### File 4: Create `templates/index.html`
```html
<!DOCTYPE html>
<html>
<head>
    <title>Gemini AI Assistant</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; }
        textarea { width: 100%; padding: 10px; }
        select { padding: 10px; font-size: 16px; }
        button { padding: 10px 20px; background-color: #4285f4; color: white; border: none; cursor: pointer; }
        #response { margin-top: 20px; padding: 15px; background-color: #f0f0f0; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>Gemini AI Assistant</h1>
    <form id="ai-form">
        <label for="message">Message:</label><br>
        <textarea id="message" name="message" rows="4" cols="50" required></textarea><br><br>
        <label for="model">Model:</label><br>
        <select id="model" name="model">
            <option value="gemini-flash">Gemini 1.5 Flash (Fast)</option>
            <option value="gemini-pro">Gemini 1.5 Pro (Advanced)</option>
        </select><br><br>
        <button type="submit">Submit</button>
    </form>
    <div id="response"></div>
    <script>
        document.getElementById('ai-form').addEventListener('submit', function(event) {
            event.preventDefault();
            var message = document.getElementById('message').value;
            var model = document.getElementById('model').value;
            fetch('/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 'message': message, 'model': model })
            })
            .then(response => response.json())
            .then(data => {
                if(data.error){
                    document.getElementById('response').innerText = 'Error: ' + data.error;
                } else {
                    document.getElementById('response').innerHTML = '<strong>Response:</strong> ' + data.response + 
                        '<br><strong>Sentiment:</strong> ' + data.sentiment + '/100' +
                        '<br><strong>Duration:</strong> ' + data.duration.toFixed(2) + 's';
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                document.getElementById('response').innerText = 'Error: ' + error;
            });
        });
    </script>
</body>
</html>
```

## 4. Run Your App (1 minute)

```bash
# From your project directory
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

Open `http://localhost:5000` in your browser!

## 5. Test Your App

Try these prompts:
- "Hello! I'm having trouble with my account"
- "How do I reset my password?"
- "Can you explain machine learning?"

Watch how Flash responds quickly vs Pro with more detailed answers!

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "API key not valid" | Verify key at https://makersuite.google.com/app/apikey |
| "Module not found" | Run `pip install -r requirements.txt` |
| "GOOGLE_API_KEY not set" | Make sure to set environment variable |
| "Rate limited" | Wait a few seconds or upgrade your API quota |

## Next Steps

- Add image support (Gemini is multimodal!)
- Implement caching for faster responses
- Add conversation history/memory
- Deploy to Google Cloud Run (free tier!)

## Resources

- 📚 [Gemini API Docs](https://ai.google.dev/docs)
- 🔑 [Get API Key](https://makersuite.google.com/app/apikey)
- 🐍 [LangChain Docs](https://python.langchain.com/)
- 💬 [Sample Prompts](https://ai.google.dev/examples)

Happy building! 🚀
