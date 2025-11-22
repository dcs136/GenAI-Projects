import os

# Model configuration
PARAMETERS = {
    "temperature": 0.7,
    "max_output_tokens": 256,
}

# API configuration
API_KEY = os.getenv("GOOGLE_API_KEY")

# Available models
GEMINI_FLASH_MODEL = "gemini-2.5-flash"          # Latest flash model
GEMINI_PRO_MODEL = "gemini-2.5-pro"              # Latest pro model
