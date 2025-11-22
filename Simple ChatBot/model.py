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

# Initialize models (lazy-loaded)
gemini_flash_llm = None
gemini_pro_llm = None

def initialize_model(model_id, api_key):
    return ChatGoogleGenerativeAI(
        model=model_id,
        google_api_key=api_key,
        temperature=PARAMETERS.get("temperature", 0.7),
    )

def get_models():
    global gemini_flash_llm, gemini_pro_llm
    if gemini_flash_llm is None:
        api_key = os.getenv("GOOGLE_API_KEY")
        gemini_flash_llm = initialize_model(GEMINI_FLASH_MODEL, api_key)
        gemini_pro_llm = initialize_model(GEMINI_PRO_MODEL, api_key)
    return gemini_flash_llm, gemini_pro_llm

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
    flash_model, _ = get_models()
    return get_ai_response(flash_model, gemini_template, system_prompt, user_prompt)

def gemini_pro_response(system_prompt, user_prompt):
    _, pro_model = get_models()
    return get_ai_response(pro_model, gemini_template, system_prompt, user_prompt)
