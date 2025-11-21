# Troubleshooting & FAQ - Gemini Edition

## Installation Issues

### Issue: `ModuleNotFoundError: No module named 'google'`

**Solution:**
```bash
# Make sure virtual environment is activated
# Then install all dependencies
pip install google-generativeai langchain langchain-google-genai Flask pydantic

# Or install from requirements.txt
pip install -r requirements.txt
```

### Issue: `ImportError: cannot import name 'ChatGoogleGenerativeAI'`

**Solution:** Update langchain packages
```bash
pip install --upgrade langchain langchain-google-genai
```

---

## Authentication Issues

### Issue: "Failed to authenticate" or "Invalid API key"

**Cause:** GOOGLE_API_KEY not set or invalid

**Solution:**
1. Get a fresh API key: https://makersuite.google.com/app/apikey
2. Set it correctly:
   - **Windows PowerShell:**
     ```powershell
     $env:GOOGLE_API_KEY = "paste_your_key_here"
     ```
   - **Linux/Mac:**
     ```bash
     export GOOGLE_API_KEY="paste_your_key_here"
     ```
3. Verify it's set:
   - Windows: `echo $env:GOOGLE_API_KEY`
   - Linux/Mac: `echo $GOOGLE_API_KEY`

### Issue: API key works in command line but not in Flask app

**Cause:** Environment variables not passed to Flask process

**Solution:** Set in `config.py` instead:
```python
import os

# Option 1: From environment variable
API_KEY = os.getenv("GOOGLE_API_KEY")

# Option 2: Hard-coded (NOT RECOMMENDED for production)
# API_KEY = "your_key_here"

# Verify it loaded
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set")
```

---

## Rate Limiting & Quota Issues

### Issue: "Resource has been exhausted" or "Rate limit exceeded"

**Cause:** Too many requests in short time

**Solutions:**
1. **Wait a few seconds** before retrying
2. **Add delays** between requests:
   ```python
   import time
   time.sleep(2)  # Wait 2 seconds between requests
   ```
3. **Check your quota:**
   - Go to: https://console.cloud.google.com/gen-app-builder/
   - Select your project
   - Check "API quotas"
4. **Upgrade your plan:**
   - Free tier: 60 requests/minute
   - Paid tier: Higher limits (https://ai.google.dev/pricing)

### Issue: "Quota exceeded for quota metric"

**Solution:** Upgrade to paid plan or wait for quota reset (usually daily)

---

## Model Issues

### Issue: "model not found" or "400 Bad Request"

**Cause:** Invalid model name

**Solution:** Use exact model names:
```python
# ✅ Correct
"gemini-1.5-flash"
"gemini-1.5-pro"
"gemini-2.0-flash"

# ❌ Wrong
"Gemini 1.5 Flash"
"gemini-flash"
"gemini_1_5_flash"
```

### Issue: Model returns incomplete or truncated response

**Cause:** `max_output_tokens` too low

**Solution:** Increase it in `config.py`:
```python
PARAMETERS = {
    "temperature": 0.7,
    "max_output_tokens": 512,  # Increase from 256
}
```

### Issue: Model gives inconsistent or creative responses

**Cause:** Temperature too high

**Solution:** Lower temperature in `config.py`:
```python
PARAMETERS = {
    "temperature": 0.3,  # Lower = more deterministic (0-1)
    "max_output_tokens": 256,
}
```

Temperature ranges:
- `0.0-0.3`: Deterministic, factual
- `0.3-0.7`: Balanced
- `0.7-1.0`: Creative, varied

---

## Flask Application Issues

### Issue: "Address already in use" when running `python app.py`

**Cause:** Port 5000 already in use

**Solution:** Use different port in `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Use 5001 instead
```

### Issue: "No such file or directory" for `index.html`

**Cause:** Incorrect folder structure

**Solution:** Create this structure:
```
genai_flask_app/
├── app.py
├── config.py
├── model.py
├── templates/
│   └── index.html
└── venv/
```

### Issue: Form submission returns blank response

**Cause:** JavaScript fetch error

**Solution:** Check browser console (F12) for errors
- Verify `/generate` endpoint exists in app.py
- Check CORS headers if needed
- Verify model selection matches app.py

---

## JSON Parsing Issues

### Issue: "JSON parsing error" or "Invalid JSON response"

**Cause:** Model output doesn't match expected format

**Solution:** Make sure prompt includes format instructions:
```python
def get_ai_response(model, template, system_prompt, user_prompt):
    chain = template | model | json_parser
    return chain.invoke({
        'system_prompt': system_prompt,
        'user_prompt': user_prompt,
        'format_prompt': json_parser.get_format_instructions()  # Important!
    })
```

### Issue: "KeyError: 'response'" when accessing result

**Cause:** JSON doesn't have expected fields

**Solution:** Update AIResponse class to match what you need:
```python
class AIResponse(BaseModel):
    summary: str = Field(description="Summary of the message")
    sentiment: int = Field(description="Sentiment 0-100")
    response: str = Field(description="AI response")
    next_step: str = Field(description="Recommended next action")  # Add new fields
```

---

## Performance Issues

### Issue: Slow responses from Gemini

**Solution:**
1. Use **Gemini Flash** instead of Pro (faster)
2. Lower `max_output_tokens`
3. Increase `temperature` (counterintuitively slightly faster)
4. Check your internet connection

### Issue: Application crashes after 30 seconds

**Cause:** Request timeout

**Solution:** Increase Flask timeout:
```python
if __name__ == '__main__':
    app.run(debug=True, timeout=120)  # 120 second timeout
```

---

## Integration Issues

### Issue: "chatgoogleGenerativeAI is not defined"

**Cause:** Missing import

**Solution:** Add to `model.py`:
```python
from langchain_google_genai import ChatGoogleGenerativeAI
```

### Issue: PromptTemplate not working correctly

**Cause:** Variable names don't match template

**Solution:** Ensure consistency:
```python
# Template
gemini_template = PromptTemplate(
    template="{system_prompt}\n{user_prompt}",
    input_variables=["system_prompt", "user_prompt"]  # Must match!
)

# Usage
chain.invoke({'system_prompt': sp, 'user_prompt': up})  # Same names!
```

---

## Debugging Tips

### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# This will show detailed API calls
```

### Test Individual Components

```python
# Test 1: Can we connect to API?
import google.generativeai as genai
genai.configure(api_key="YOUR_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content("Hello")
print(response.text)

# Test 2: Does LangChain work?
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key="YOUR_KEY")
result = llm.invoke("Hello")
print(result)

# Test 3: Does Flask work?
# Just run: python app.py
# Visit: http://localhost:5000
```

### Check API Usage

Visit https://console.cloud.google.com/gen-app-builder/ and check:
- API quotas
- Usage graphs
- Error logs

---

## Common Pitfalls

### ❌ Pitfall 1: Hardcoding API keys
```python
# DON'T DO THIS
API_KEY = "AIzaSyD..."  # Exposed in git!
```

**✅ Better:**
```python
API_KEY = os.getenv("GOOGLE_API_KEY")  # From environment
```

### ❌ Pitfall 2: No error handling
```python
# DON'T DO THIS
result = llm.invoke(text)  # Will crash if API fails
```

**✅ Better:**
```python
try:
    result = llm.invoke(text)
except Exception as e:
    print(f"Error: {e}")
    return {"error": str(e)}
```

### ❌ Pitfall 3: Ignoring rate limits
```python
# DON'T DO THIS
for i in range(1000):
    model.generate_content(prompt)  # Too many requests!
```

**✅ Better:**
```python
import time
for i in range(1000):
    model.generate_content(prompt)
    time.sleep(1)  # Rate limit control
```

### ❌ Pitfall 4: Mixing up variable names
```python
# DON'T DO THIS
template.invoke({'system': sp, 'user': up})  # Wrong variable names!
```

**✅ Better:**
```python
# Template says {"system_prompt", "user_prompt"}
template.invoke({'system_prompt': sp, 'user_prompt': up})
```

---

## Getting Help

1. **Check the docs:**
   - [Gemini API Docs](https://ai.google.dev/docs)
   - [LangChain Docs](https://python.langchain.com/)

2. **Review error messages carefully** - they often tell you exactly what's wrong

3. **Check the sample code** - run the examples from QUICK_START.md first

4. **Enable debug logging** to see what's happening

5. **Test one piece at a time** - don't try everything together

---

## Quick Checklist

- [ ] API key obtained from https://makersuite.google.com/app/apikey
- [ ] Environment variable set: `$env:GOOGLE_API_KEY = "key"`
- [ ] Virtual environment activated: `.\venv\Scripts\Activate.ps1`
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Folder structure correct with `templates/` folder
- [ ] `index.html` in `templates/` folder
- [ ] Model names exact: `gemini-1.5-flash` or `gemini-1.5-pro`
- [ ] No API rate limiting (check quota)
- [ ] Flask running without errors

---

**Still stuck?** Double-check the GEMINI_MIGRATION_NOTES.md for Watson → Gemini changes!
