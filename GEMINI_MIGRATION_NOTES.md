# Gemini Edition - Migration Notes

This document summarizes the changes made to adapt the original IBM Watsonx course to use Google Gemini APIs.

## Overview

The original course used:
- **IBM Watsonx AI** for model inference
- **Models**: Llama 3, Granite, Mixtral
- **Libraries**: `ibm-watsonx-ai`, `langchain-ibm`

This adapted version uses:
- **Google Generative AI** (Gemini)
- **Models**: Gemini 1.5 Flash, Gemini 1.5 Pro
- **Libraries**: `google-generativeai`, `langchain-google-genai`

## Key Changes

### 1. Installation & Setup

**Before (Watson)**:
```bash
pip install ibm-watsonx-ai
# Required authentication with Watson credentials and project IDs
```

**After (Gemini)**:
```bash
pip install google-generativeai langchain langchain-google-genai

# Environment setup
export GOOGLE_API_KEY="your_api_key_here"  # Linux/Mac
$env:GOOGLE_API_KEY="your_api_key_here"    # Windows PowerShell
```

### 2. Authentication & Configuration

**Before (Watson - config.py)**:
```python
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

CREDENTIALS = {
    "url": "https://us-south.ml.cloud.ibm.com",
    "project_id": "skills-network"
}

PARAMETERS = {
    GenParams.DECODING_METHOD: "greedy",
    GenParams.MAX_NEW_TOKENS: 256,
}

MODEL_IDS = {
    "llama3": "meta-llama/llama-3-2-11b-vision-instruct",
    "granite": "ibm/granite-3-8b-instruct",
    "mixtral": "mistralai/mistral-large"
}
```

**After (Gemini - config.py)**:
```python
import os

API_KEY = os.getenv("GOOGLE_API_KEY")

PARAMETERS = {
    "temperature": 0.7,
    "max_output_tokens": 256,
}

GEMINI_FLASH_MODEL = "gemini-1.5-flash"
GEMINI_PRO_MODEL = "gemini-1.5-pro"
GEMINI_2_FLASH_MODEL = "gemini-2.0-flash"
```

### 3. Model Initialization

**Before (Watson - model.py)**:
```python
from langchain_ibm import ChatWatsonx

def initialize_model(model_id):
    return ChatWatsonx(
        model_id=model_id,
        url="https://us-south.ml.cloud.ibm.com",
        project_id="skills-network",
        params=PARAMETERS
    )
```

**After (Gemini - model.py)**:
```python
from langchain_google_genai import ChatGoogleGenerativeAI

def initialize_model(model_id, api_key):
    return ChatGoogleGenerativeAI(
        model=model_id,
        google_api_key=api_key,
        temperature=PARAMETERS.get("temperature", 0.7),
    )
```

### 4. Prompt Formatting

**Before (Watson - special tokens required)**:
```python
# Llama format with special tokens
llama_template = PromptTemplate(
    template='''<|begin_of_text|><|start_header_id|>system<|end_header_id|>
{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>
{user_prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
''',
    input_variables=["system_prompt", "user_prompt"]
)

# Granite format
granite_template = PromptTemplate(
    template="<|system|>{system_prompt}\n<|user|>{user_prompt}\n<|assistant|>",
    input_variables=["system_prompt", "user_prompt"]
)
```

**After (Gemini - natural conversation style)**:
```python
# Single template for all Gemini models (no special tokens needed)
gemini_template = PromptTemplate(
    template="{system_prompt}\n\n{format_prompt}\n\nUser: {user_prompt}",
    input_variables=["system_prompt", "format_prompt", "user_prompt"]
)
```

### 5. Flask Integration

**Before (Watson - app.py)**:
```python
from model import llama3_response, granite_response, mixtral_response

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    model = data.get('model')
    
    if model == 'llama3':
        result = llama3_response(system_prompt, user_message)
    elif model == 'granite':
        result = granite_response(system_prompt, user_message)
    elif model == 'mixtral':
        result = mixtral_response(system_prompt, user_message)
```

**After (Gemini - app.py)**:
```python
from model import gemini_flash_response, gemini_pro_response

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    model = data.get('model')
    
    if model == 'gemini-flash':
        result = gemini_flash_response(system_prompt, user_message)
    elif model == 'gemini-pro':
        result = gemini_pro_response(system_prompt, user_message)
```

### 6. HTML Form Options

**Before (Watson)**:
```html
<select id="model" name="model">
    <option value="llama3">Llama3</option>
    <option value="granite">Granite</option>
    <option value="mixtral">Mixtral</option>
</select>
```

**After (Gemini)**:
```html
<select id="model" name="model">
    <option value="gemini-flash">Gemini 1.5 Flash</option>
    <option value="gemini-pro">Gemini 1.5 Pro</option>
</select>
```

## Model Comparison

| Aspect | Llama 3 | Granite | Mixtral | Gemini Flash | Gemini Pro |
|--------|---------|---------|---------|--------------|-----------|
| **Speed** | Medium | Medium | Fast | Very Fast | Medium |
| **Quality** | High | High | High | Good | Excellent |
| **Cost** | Low-Mid | Low-Mid | Mid | Low | Mid |
| **Context** | 128K | 8K-64K | 128K | 100K | 1M |
| **Multimodal** | Yes | No | No | Yes | Yes |
| **Setup** | Complex | Complex | Complex | Simple | Simple |

## Important Notes

### Free Tier
- Gemini API offers a **free tier** (60 requests/min, 1 million tokens/month)
- Get your free API key at: https://makersuite.google.com/app/apikey

### No Special Tokens
Unlike Llama models, Gemini doesn't require special token formatting. It handles natural conversation structure automatically.

### Rate Limits
Monitor your usage at https://console.cloud.google.com/gen-app-builder/

### Error Handling
Common issues:
```python
# Missing API key
# Solution: Set GOOGLE_API_KEY environment variable

# Rate limited
# Solution: Add delays between requests or upgrade to paid plan

# Invalid model name
# Solution: Use exact model IDs: "gemini-1.5-flash" or "gemini-1.5-pro"
```

## Testing

Test with the provided `llm_test.py`:
```bash
python llm_test.py
```

This will test both Gemini Flash and Pro models with a sample query about Canada's capital.

## Next Steps for Enhancement

1. **Add Streaming**: Gemini supports streaming responses for better UX
2. **Image Handling**: Use multimodal capabilities to process images
3. **Function Calling**: Leverage Gemini's native tool use capabilities
4. **Caching**: Implement LangChain's caching for repeated prompts
5. **Batch Processing**: Use Gemini Batch API for large-scale processing

## Troubleshooting

### "Failed to authenticate"
- Verify GOOGLE_API_KEY is correctly set
- Check API key is active in Google Cloud Console

### "Rate limit exceeded"
- Wait a few seconds before retrying
- Consider upgrading your Google Cloud plan

### "Model not found"
- Ensure model names are exact: `gemini-1.5-flash` or `gemini-1.5-pro`
- Check https://ai.google.dev/models for available models

## Resources

- [Google Generative AI API](https://ai.google.dev/)
- [LangChain Google Integration](https://python.langchain.com/docs/integrations/llms/google_generative_ai)
- [Gemini API Docs](https://ai.google.dev/docs)
- [Free API Key](https://makersuite.google.com/app/apikey)

## Questions or Issues?

If you encounter problems:
1. Check the API key is properly configured
2. Ensure all required libraries are installed
3. Review the Gemini documentation for the latest changes
4. Check Google Cloud console for quota/rate limit issues
