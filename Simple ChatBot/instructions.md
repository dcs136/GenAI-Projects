
 Hands-on with GenAI: Choosing the Right Model for Your Application (Gemini Edition)
 Welcome to this exciting guided project where you'll learn to build your first GenAI application and choose the right LLM for your application! In this 90-minute, hands-on workshop, you'll dive into the world of generative
 AI, leveraging powerful tools and best practices to create a robust and efficient application.
 **IMPORTANT: Gemini Edition** - This guide has been modified to use Google Gemini instead of IBM Watsonx. See setup instructions below.

 **Quick Setup Guide for Gemini**
 This guide has been adapted to use Google Gemini APIs. Key differences from the original Watson version:
 - **API Access**: Requires a Google Cloud project with Gemini API enabled (free tier available)
 - **Authentication**: Uses GOOGLE_API_KEY environment variable instead of Watson credentials
 - **Models**: Uses `gemini-1.5-flash` (fast, cost-efficient) and `gemini-1.5-pro` (advanced reasoning)
 - **Libraries**: Uses `google-generativeai` and `langchain-google-genai` instead of `langchain-ibm`
 - **No special tokens**: Gemini handles prompts naturally without Llama-style special tokens
 - **Full setup**: Estimated time ~15 minutes, including API key configuration
 Learning objectives
 By the end of this project, you will be able to:
 Develop a Flask web application integrated with AI capabilities
 Utilize the google-generativeai library to interact with advanced language models (Gemini)
 Implement LangChain's JsonOutputParser for structured AI outputs
 Apply prompt engineering techniques for generating actionable JSON responses
 Compare and evaluate different language models including Gemini Pro
 Enhance your application with modular and reusable AI integration code
 Let's embark on this journey to transform your development skills and create an intelligent, AI-driven application!
 Setting up your development environment
 Before we dive into development, let's set up your project environment in the Cloud IDE. This environment is based on Ubuntu 22.04 and provides all the tools you need to build your AI-driven Flask application.
 Step 1: Create your project directory
 Open the terminal in Cloud IDE and run:
 mkdir genai_flask_app
 cd genai_flask_app
 This creates a new directory for your project and navigates into it.
 Step 2: Set up a Python virtual environment
 Initialize a new Python virtual environment:
 python3.11 -m venv venv
 source venv/bin/activate
 about:blank
 1/19
11/20/25, 12:58 PM
 about:blank
 Step 3: Install the google-generativeai library
 With your virtual environment activated, install google-generativeai via:
 pip install google-generativeai langchain langchain-google-genai
 This command installs google-generativeai for Gemini API access, along with LangChain integration packages.
 Step 4: Set up your Gemini API key
 Export your Google API key as an environment variable:
 On Linux/Mac:
 export GOOGLE_API_KEY="your_api_key_here"
 On Windows PowerShell:
 $env:GOOGLE_API_KEY="your_api_key_here"
 Now that your environment is set up, you're ready to start building your GenAI application!
 Understanding AI models: A comparative overview
 Before we start coding, let's dive into Gemini models. Google's Gemini is a family of multimodal AI models with different sizes optimized for various use cases.

 **Gemini 1.5 Pro**
 Strengths:
 State-of-the-art performance across most tasks
 Supports 1 million token context window
 Multimodal capabilities (text, images, audio, video)
 Native tool use and function calling
 Best use cases:
 Complex reasoning and analysis tasks
 Long document processing and summarization
 Multimodal applications combining text and images

 **Gemini 1.5 Flash**
 Strengths:
 Optimized for speed and cost-efficiency
 Fast response times for real-time applications
 Still maintains high quality for most tasks
 Lower token costs than Pro
 Best use cases:
 Quick response applications
 High-volume API usage
 Latency-sensitive applications
 Classification and extraction tasks

 **Gemini 2.0 Flash** (latest, experimental)
 Strengths:
 Improved speed and efficiency
 Better tool use capabilities
 Latest improvements from Google AI
 Best use cases:
 Cutting-edge applications
 Research and experimentation

 Performance considerations
 When choosing a Gemini model, consider:
 1. Speed: Flash models are faster but Pro has better reasoning.
 2. Accuracy: Pro generally performs better on complex tasks; Flash is sufficient for most standard tasks.
 3. Cost: Flash costs significantly less; pricing varies by token count.
 4. Context Length: All Gemini models support large context windows (100k-1M tokens).
 5. Multimodal needs: All Gemini models support images, audio, and video.

 Understanding these trade-offs will help you choose the right Gemini model for your application.

 Using the Google Generative AI Python library

 Let's make our very first call to Gemini. We'll use the Gemini 1.5 Flash model, which offers excellent performance and cost-efficiency.

 Create the file capital.py:
 Open capital.py in IDE

 Let's start by adding in imports:

 import google.generativeai as genai
 import os

 This imports the required modules to authenticate and interact with the Gemini API.

 # Configure the API key
 api_key = os.getenv("GOOGLE_API_KEY")
 genai.configure(api_key=api_key)

 This sets up the API key for authentication. Make sure you've set the GOOGLE_API_KEY environment variable.

 # Initialize the model
 model = genai.GenerativeModel('gemini-1.5-flash')

 # Create generation config
 config = genai.types.GenerationConfig(
     max_output_tokens=100,
     temperature=0.7,
 )

 The config object defines key settings for how the model generates output:
 max_output_tokens: Maximum number of tokens in the response (similar to Watson's MAX_NEW_TOKENS)
 temperature: Controls randomness in responses. 0.0 = deterministic; 1.0+ = more creative. We use 0.7 for a balance.

 text = """
 Only reply with the answer. What is the capital of Canada?
 """

 response = model.generate_content(text, generation_config=config)
 print(response.text)

 Running this code you should get the expected answer:

 Ottawa.

 Great job - you've called your first Gemini model!

 Trying other Gemini models
 There are numerous LLMs available from IBM and other providers, each with its own strengths and use cases. New models are constantly emerging, so it's important to stay informed about the latest advancements in the
 field.
 How to choose the right LLM
 First of all, choosing an LLM model is deceptively complicated (it's a whole topic in itself). While it's tempting to focus on the specs alone—like token limits, training data, or number of parameters—these details will only
 take you so far. The real test comes when you evaluate how a model performs for your specific use cases.
 Here are some important factors to consider when selecting a model:
 Capabilities: Does the model meet your needs? For example, some models are multimodal, meaning they can handle images and text, whereas others are limited to text-only tasks.
 Cost: How much does it cost to use the model, including both input and output tokens? Balancing cost with performance is key to ensuring long-term value.
 about:blank
 5/19
11/20/25, 12:58 PM
 about:blank
 Speed: How quickly does the model generate responses? In some use cases, speed is just as important as accuracy, especially in real-time applications.
 Quality: How accurate and relevant are the model's outputs for your tasks? You'll need to run tests to evaluate if the responses meet your quality standards.
 Other considerations: Think about any specific vendors you may need to work with, licensing restrictions, or integrations with your existing systems.
 Ultimately, you'll want to experiment and run real-world tests to find the right fit for your needs. Specs can guide you, but hands-on testing against your own usecases is the only way to truly know if a model works for your
 unique scenarios.
 Now let's try and update our code using a newer LLM model, llama-3-2-1b-instruct.
 Make sure you still have capital.py open:
 Open capital.py in IDE
 Now simply update the model from ibm/granite-3-3-8b-instruct to meta-llama/llama-3-2-1b-instruct. The new code should look like the following:
 model = ModelInference(
    model_id='meta-llama/llama-3-2-1b-instruct',
    params=params,
    credentials=credentials,
    project_id="skills-network"
 )
 Now run the code in the terminal again:
 python capital.py
 Running the code, we get (note: You will probably get a slightly different output)
 “””
 A) Toronto
 B) Ottawa
 C) Vancouver
 D) Montreal
 The correct answer is B) Ottawa.
 Explanation: Ottawa is the capital city of Canada, located in the province of Ontario. It is home to the country's parliament and many national institutions. Toronto, Vancouver, and Montreal are all major cities
 in Canada, but they are not the capital.
 This question requires the ability to identify the correct answer by eliminating the incorrect options. The student needs to know that Ottawa is
 “””
 Hmm… not quite the answer we were expecting. Why is that? (Don't worry, we'll explain in the next section.)
 about:blank
 6/19
Try using different models and see what you come up with!
 Here's a list of some of the latest models available in WatsonX (as of October 21, 2024). Just replace the model_id in the code with one of the ones below and run the program again!
 Provider model ID Use Cases Context
 Length
 Price USD per million
 tokens
 IBM ibm/granite-3-8b-instruct Supports questions and answers (Q&A), summarization, classification, generation, extraction, RAG, and coding tasks. 4096 0.2
 IBM ibm/granite-3-2b-instruct Supports questions and answers (Q&A), summarization, classification, generation, extraction, RAG, and coding tasks. 4096 0.1
 IBM ibm/granite-20b-multilingual Supports Q&A, summarization, classification, generation, extraction, translation and RAG tasks in French, German,
 Portuguese, Spanish and English. 8192 0.6
 IBM ibm/granite-13b-instruct-v2 Supports Q&A, summarization, classification, generation, extraction and RAG tasks. 8192 0.6
 IBM ibm/granite-34b-code-instruct Task-specific model for code by generating, explaining and translating code from a natural language prompt. 8192 0.6
 IBM ibm/granite-20b-code-instruct Task-specific model for code by generating, explaining and translating code from a natural language prompt. 8192 0.6
 Meta meta-llama/llama-3-2-90b
vision-instruct
 Supports Q&A, summarization, classification, generation, extraction, translation and RAG tasks in French, German,
 Portuguese, Spanish and English. 128k 2.00
 Meta meta-llama/llama-3-2-11b-vision
instruct
 Supports image captioning, image-to-text transcription (OCR) including handwriting, data extraction and processing, context
 Q&A, object identification 128k 0.35
 Meta meta-llama/llama-3-2-1b-instruct Supports Q&A, summarization, generation, coding, classification, extraction, translation and RAG tasks in English, German,
 French, Italian, Portuguese, Hindi, Spanish, and Thai 128k 0.1
 Mistral mistralai/mistral-large Supports Q&A, summarization, generation, coding, classification, extraction, translation and RAG tasks in French, German,
 Italian, Spanish and English. 128k 10.00
 Google google/flan-t5-xl Supports Q&A, summarization, classification, generation, extraction and RAG tasks. Available for prompt-tuning 4096 0.6
 Tokenization and prompt formatting
 We missed a very important step. Llama uses special tokens to improve its functionality, control, and adaptability across diverse tasks. Without special tokens, Llama 3's responses can be unpredictable because it lacks the
 necessary cues to interpret the structure, context, or intent of the input. These tokens act as guides that tell the model how to respond.
 Llama 3
 Token name Description
 <|begin_of_text|> Specifies the start of the prompt.
 <|end_of_text|> Specifies the end of the prompt.
 <|start_header_id|> These tokens enclose the role for a particular message, always paired with <|end_header_id|>. The possible roles are: [system, user, assistant, and ipython].
 <|end_header_id|> Pairs with <|start_header_id|> to define role for a particular message
 <|eot_id|> End of turn. Represents when the model has determined that it has finished interacting with the user message that initiated its response. This token signals to the executor that the model has
 finished generating a response.
 Roles
 11/20/25, 12:58 PM about:blank
 about:blank 7/19
11/20/25, 12:58 PM
 about:blank
 In addition to prompt formatting, we need to understand the concept of roles (to be enclosed within the <|start_header_id|> and <|end_header_id|> tags). In Llama, there are 4 roles.
 System: Specifies the behavior, context, or personality of the assistant. It sets guidelines or instructions that shape how the assistant interacts, responds, and helps users. This can include the tone, formality, and any
 background knowledge needed to better assist.
 User: Represents the person interacting with the assistant. This role contains the queries, requests, or commands made by the user. For example, if the user asks, "What is the capital of France?" the assistant will
 generate a relevant response based on this input.
 Assistant: This is where the AI-generated response is provided. Based on the user's input and the system's instructions, the assistant crafts a reply here that meets the user’s needs.
 iPython: A new role introduced in Llama 3.1. This role is used to mark messages with the output of a tool call when sent back to the model from the executor. We won't be using this role here.
 Mixtral
 Token name
 <s>
 <\s>
 [INST]
 [/INST]
 Description
 Marks the start of a sentence or sequence.
 Marks the end of a sentence or sequence.
 Signifies the start of an instructional message or command. Typically used for instructions.
 Marks the end of the instructional message.
 Granite
 Token name
 <|system|>
 <|user|>
 <|assistant|>
 Description
 Identifies the instruction, commonly referred to as the system prompt for the foundation model.
 The query text to be answered.
 A cue at the end of the prompt that indicates that a generated answer is expected.
 Trying a second time
 So let's update our code to use the aforementioned special tokens.
 text = """
 <|begin_of_text|><|start_header_id|>system<|end_header_id|>
 You are an expert assistant who provides concise and accurate answers.<|eot_id|>
 <|start_header_id|>user<|end_header_id|>
 What is the capital of Canada?<|eot_id|>
 <|start_header_id|>assistant<|end_header_id|>
 """
 And we now see our output being:
 The capital of Canada is Ottawa.
 8/19
 about:blank
11/20/25, 12:58 PM
 about:blank
 So why did that happen?
 Remember, while LLM's are impressively versitile, they aren't yet fully equiped for true logical reasoning–yet!. They transform content into tokens and then predict the next token. This means that when asked, "Why did the
 chicken cross the road?" an LLM might respond with "Is a common riddle joke" just as likely as with "To get to the other side," as it"s selecting responses based on probability rather than understanding. By using special
 tokens to better define the role of the LLM, we gain tighter control over its responses, aligning outputs more closely with our intended outcomes.
 1. Now try doing it with other models.
 Click here for the answer
 What is LangChain?
 LangChain provides an abstraction layer over multiple language models, allowing developers to use a consistent API and set of tools to switch between or combine different models, depending on their needs. It includes
 built-in utilities for managing prompts, chaining responses, parsing outputs, and structuring conversations, making it a powerful toolkit for building sophisticated AI applications.
 Why use LangChain?
 Consistent and modular integration, with reusable components, simplify the integration of AI models into your application such as the ability to switch out models without major code changes.
 Structured Outputs with JSON Parsers help ensure that responses from the language model are consistent and easily parsed
 Support for multi-step workflows allows you to create complex, multi-step workflows that involve multiple prompts communicating with multiple different models
 Using LangChain in a GenAI application enables developers to build robust, efficient, and maintainable AI solutions by simplifying the management of model interactions and ensuring that outputs are structured and
 reliable. As a result, LangChain empowers developers to focus on higher-level functionality, enhancing the overall performance and usability of AI-driven applications.
 Creating your Flask application
 Now that we understand our AI models, let's start by creating the backbone of your Flask application. We'll set up a basic structure that we'll enhance with AI capabilities in the following steps.
 Before we start coding, let's install the Flask and LangChain libraries:
 pip install Flask langchain langchain-google-genai
 This command installs:
 Flask for web development
 LangChain libraries for advanced AI capabilities
 about:blank
 9/19
11/20/25, 12:58 PM
 about:blank
 Step 1: Create your main application file
 Create a new file named app.py:
 Open app.py in IDE
 Add the following code to set up a basic Flask app:
 from flask import Flask, request, jsonify
 app = Flask(__name__)
 @app.route('/generate', methods=['POST'])
 def generate():
 # This is where we'll add our AI logic later
 return jsonify({"message": "AI response will be generated here"})
 if __name__ == '__main__':
    app.run(debug=True)
 Let's break down this code:
 We import necessary modules from Flask.
 We create a Flask application instance.
 We define a route /generate that will handle POST requests. This is where our AI logic will go.
 For now, it returns a simple JSON response.
 The if __name__ == '__main__': block ensures the Flask development server runs when we execute this file directly.
 You've set up the foundation of your GenAI application. In the next sections, we'll integrate AI capabilities and enhance its functionality.
 Integrating AI models with LangChain
 Now, let's integrate AI capabilities into your Flask application using the langchain library and various language models. We'll focus on creating a modular structure for easy maintenance and expansion.
 Step 1: Create a model configuration file
 First, let's create a configuration file to store our model parameters and credentials. Create a new file named config.py:
 Open config.py in IDE
 Add the following code:
 from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

 # Model parameters
 PARAMETERS = {
     "temperature": 0.7,
     "max_output_tokens": 256,
 }

 # Google API configuration
 import os
 API_KEY = os.getenv("GOOGLE_API_KEY")

 # Model IDs
 GEMINI_FLASH_MODEL = "gemini-1.5-flash"
 GEMINI_PRO_MODEL = "gemini-1.5-pro"
 GEMINI_2_FLASH_MODEL = "gemini-2.0-flash"
 This configuration file centralizes our model settings, making it easier to manage and update them.
 Step 2: Create a model integration file
 Now, let's create a file to handle our AI model integration. Create a new file named model.py:
 Open model.py in IDE
 from langchain_ibm import ChatWatsonx
 from langchain.prompts import PromptTemplate
 from config import PARAMETERS, LLAMA3_MODEL_ID, GRANITE_MODEL_ID, MIXTRAL_MODEL_ID
 Let's break down the imports
 1. ChatWatsonx will be our interface to interact with IBM Watsonx AI models.
 2. PromptTemplate allows us to create dynamic prompts with placeholders for AI input.
 3. PARAMETERS, LLAMA3_MODEL_ID, etc. are the configuration values we defined earlier to set up our different AI models.
 # Function to initialize a model
 def initialize_model(model_id):
 return ChatWatsonx(
        model_id=model_id,
        url="https://us-south.ml.cloud.ibm.com",
        project_id="skills-network",
        params=PARAMETERS
 )
 # Initialize models
 llama3_llm = initialize_model(LLAMA3_MODEL_ID)
 granite_llm = initialize_model(GRANITE_MODEL_ID)
 mixtral_llm = initialize_model(MIXTRAL_MODEL_ID)
 We will once again initialize our models, this time we're going to take advantage of LangChain's ChatWatsonx, a wrapper for WatsonX API client.
 11/19
 about:blank
11/20/25, 12:58 PM
 about:blank
 # Prompt template
 llama3_template = PromptTemplate(
    template='''<|begin_of_text|><|start_header_id|>system<|end_header_id|>
 {system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>
 {user_prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
 ''',
    input_variables=["system_prompt", "user_prompt"]
 )
 granite_template = PromptTemplate(
    template="<|system|>{system_prompt}\n\<|user|>{user_prompt}\n<|assistant|>",
    input_variables=["system_prompt", "user_prompt"]
 )
 mixtral_template = PromptTemplate(
    template="<s>[INST]{system_prompt}\n{user_prompt}[/INST]",
    input_variables=["system_prompt", "user_prompt"]
 )
 To make our prompts more reusable and adaptable across our chats, we can use the PromptTemplate class. This allows us to define templates with placeholders that can be filled dynamically at runtime with specific inputs.
 By defining placeholders like system_prompt and user_prompt, these templates can be reused with different content, making them flexible for various interactions with AI models.
 def get_ai_response(model, template, system_prompt, user_prompt):
    chain = template | model
 return chain.invoke({'system_prompt':system_prompt, 'user_prompt':user_prompt})
 The functionget_ai_responseallows us to chain a prompt template and an AI model together. We can using the pipe operator|to directly take the output of the template and use that as the input of the model.
 # Model-specific response functions
 def llama3_response(system_prompt, user_prompt):
 return get_ai_response(llama3_llm, llama3_template, system_prompt, user_prompt)
 def granite_response(system_prompt, user_prompt):
 return get_ai_response(granite_llm, granite_template, system_prompt, user_prompt)
 def mixtral_response(system_prompt, user_prompt):
 return get_ai_response(mixtral_llm, mixtral_template, system_prompt, user_prompt)
 The model-specific functions each call this generic function with the respective models and templates, ensuring that the appropriate format is used for each AI model when generating responses.
 Let's break down this code:
 about:blank
 12/19
11/20/25, 12:58 PM
 about:blank
 1. We import necessary modules and our configuration.
 2. We define a function initialize_model to create model instances, promoting code reuse.
 3. We initialize our models using this function.
 4. We create prompt templates for each model, as they may have different preferred formats.
 5. The get_ai_response function handles the process of formatting prompts, getting responses
 6. We define model-specific response functions that use the general get_ai_response function.
 This modular approach allows for easy addition of new models or modification of existing ones.
 Sanity check
 That was a lot of code, before we move on, let's try running the code and see what we have. Let's give all our models a test run by calling them all together as a function.
 Create the file llm_test.py:
 Open llm_test.py in IDE
 from model import gemini_flash_response, gemini_pro_response

 def call_all_models(system_prompt, user_prompt):
     flash_result = gemini_flash_response(system_prompt, user_prompt)
     pro_result = gemini_pro_response(system_prompt, user_prompt)

     print("Gemini Flash Response:\n", flash_result)
     print("\nGemini Pro Response:\n", pro_result)

 # Example call to test all models
 call_all_models("You are a helpful assistant who provides concise and accurate answers", "What is the capital of Canada? Tell me a cool fact about it as well")
 And run the following:
 python llm_test.py
 If everything went well, you should get an output similar to the following:
 “”
 Llama3 Response:
 The capital of Canada is Ottawa.
 A cool fact about Ottawa is that it's home to the Rideau Canal, a UNESCO World Heritage Site and the oldest continuously operated canal in North America. During the winter months, the canal freezes over
 and becomes the world's largest naturally frozen ice skating rink, stretching 7.8 kilometers (4.8 miles) through the heart of the city.
 Granite Response:
 The capital of Canada is Ottawa. It's located on the south bank of the Ottawa River and is known for its historic architecture, museums, and vibrant cultural scene. A cool fact about Ottawa is that it's home to the
 13/19
 about:blank
11/20/25, 12:58 PM
 about:blank
 world's largest indoor ice-skating rink, the Rideau Canal Skateway, which is also a UNESCO World Heritage Site.
 Mixtral Response:
 The capital of Canada is Ottawa. A cool fact about Ottawa is that it is one of the coldest capitals in the world. During winter, temperatures can drop as low as -40°C (-40°F), making it a popular destination for
 winter sports and activities like ice skating on the Rideau Canal, which becomes the world's largest naturally frozen ice skating rink.
 “”
 Setting up JSON outputs
 There's an important step we need to address: Making sure the AI's output follows a well-defined format. This is essential for taking the output and seamlessly integrating it into other systems, like a website.
 We can use Pydantic to define a clear schema for the AI's response, ensuring consistent structure and validation. This enforces the correct format, making data integration smoother and more reliable.
 from pydantic import BaseModel, Field
 from langchain_core.output_parsers import JsonOutputParser
 We'll use BaseModel and Field to define our JSON output structure. To make our lives a bit easier, we will also useJsonOutputParserto automatically parse and validate the AI’s output into the structured format we’ve
 defined.
 Pydantic model
 # Define JSON output structure
 class AIResponse(BaseModel):
    summary: str = Field(description="Summary of the user\'s message")
    sentiment: int = Field(description="Sentiment score from 0 (negative) to 100 (positive)")
    response: str = Field(description="Suggested response to the user")
 To seamlessly integrate this structure into our code, we use the JsonOutputParser. This parser ensures that the output returned by the AI is automatically validated and parsed into theAIResponseformat.
 JSON Output Parser
 # JSON output parser
 json_parser = JsonOutputParser(pydantic_object=AIResponse)
 14/19
 about:blank
11/20/25, 12:58 PM
 about:blank
 Here, we define the expected output using the AIResponse Pydantic model, specifying fields like summary, sentiment, action, and response. The JsonOutputParser will ensure that the AI output conforms to this structure,
 providing well-formatted, validated data for further use in our application.
 Updating the chain
 def get_ai_response(model, template, system_prompt, user_prompt):
    chain = template | model | json_parser
 return chain.invoke({'system_prompt':system_prompt, 'user_prompt':user_prompt, 'format_prompt':json_parser.get_format_instructions()})
 You can see that we add the json_parser to our chain and call json_parser.get_format_instructions(), which will ultimately update our prompt with instructions to respond in well-structured JSON as defined by the
 AIResponse class.
 Putting it all together
 So let's add this to the chain! To do this, we need to addAIResponseandjson_parserto the top ofmodel.pyas well as adding adding another link to our chain object within get_ai_response. Your code should look like this:
 Open model.py in IDE
 from langchain_google_genai import ChatGoogleGenerativeAI
 from langchain.prompts import PromptTemplate
 from langchain_core.output_parsers import JsonOutputParser
 from pydantic import BaseModel, Field
 from config import PARAMETERS, API_KEY, GEMINI_FLASH_MODEL, GEMINI_PRO_MODEL
 import os

 # Define JSON output structure
 class AIResponse(BaseModel):
    summary: str = Field(description="Summary of the user's message")
    sentiment: int = Field(description="Sentiment score from 0 (negative) to 100 (positive)")
    response: str = Field(description="Suggested response to the user")

 # JSON output parser
 json_parser = JsonOutputParser(pydantic_object=AIResponse)

 # Function to initialize a model
 def initialize_model(model_id, api_key):
     return ChatGoogleGenerativeAI(
         model=model_id,
         google_api_key=api_key,
         temperature=PARAMETERS.get("temperature", 0.7),
     )

 # Initialize models
 api_key = os.getenv("GOOGLE_API_KEY")
 gemini_flash_llm = initialize_model(GEMINI_FLASH_MODEL, api_key)
 gemini_pro_llm = initialize_model(GEMINI_PRO_MODEL, api_key)

 # Prompt templates for Gemini (no special tokens needed)
 gemini_template = PromptTemplate(
    template="{system_prompt}\n\n{format_prompt}\n\nUser: {user_prompt}",
    input_variables=["system_prompt", "format_prompt", "user_prompt"]
 )

 def get_ai_response(model, template, system_prompt, user_prompt):
    chain = template | model | json_parser
    return chain.invoke({
        'system_prompt': system_prompt,
        'user_prompt': user_prompt,
        'format_prompt': json_parser.get_format_instructions()
    })

 # Model-specific response functions
 def gemini_flash_response(system_prompt, user_prompt):
     return get_ai_response(gemini_flash_llm, gemini_template, system_prompt, user_prompt)

 def gemini_pro_response(system_prompt, user_prompt):
     return get_ai_response(gemini_pro_llm, gemini_template, system_prompt, user_prompt)
 Exercise: Enhancing the JSON structure
 Now, let's practice enhancing our JSON structure. Your task is to add a new field to the AIResponse class that recommends the next step the support representative may take to resolve this issue.
 1. Update the AIResponse class in model.py.
 2. Modify the system prompt in app.py to include this new field.
 3. Test your changes with a variety of user messages.
 Click here for the answer
 Enhancing your Flask application with AI capabilities
 Now that we have our AI models set up, let's integrate them into our Flask application.
 Step 1: Update your Flask application
 Let's update app.py to use these AI capabilities:
 Open app.py in IDE
 Update the content of app.py with:
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
 Let's break down the changes:
 1. We import our model-specific response functions.
 2. In the /generate route, we now expect JSON input with "message" and "model" fields.
 3. We add error handling for missing inputs.
 4. We use a try-except block to handle potential errors in AI processing.
 5. We measure and include the processing time in the response.
 This setup allows us to handle requests for different models and provides robust error handling.
 Step 2: Create the simple HTML file
 Create the file templates/index.html:
 Open index.html in IDE
 Update the content of templates/index.html with:
 <!DOCTYPE html>
 <html>
 <head>
 <title>AI Assistant</title>
 </head>
 <body>
 <h1>AI Assistant</h1>
 <form id="ai-form">
 <label for="message">Message:</label><br>
 <textarea id="message" name="message" rows="4" cols="50"></textarea><br><br>
 <label for="model">Model:</label><br>
 <select id="model" name="model">
 <option value="gemini-flash">Gemini 1.5 Flash</option>
 <option value="gemini-pro">Gemini 1.5 Pro</option>
 </select><br><br>
 <input type="submit" value="Submit">
 </form>
 <br>
 <div id="response"></div>
 <script>
 17/19
 about:blank
11/20/25, 12:58 PM
 about:blank
        document.getElementById('ai-form').addEventListener('submit', function(event) {
            event.preventDefault();
 var message = document.getElementById('message').value;
 var model = document.getElementById('model').value;
            fetch('/generate', {
                method: 
'POST',
                headers: 
{
 'Content-Type': 'application/json',
 },
                body:
 JSON.stringify({
 'message': message,
 'model': model
 }),
 })
 .then(response => response.json())
 .then(data => {
 if(data.error){
                    document.getElementById('response').innerText = 'Error: ' + data.error;
 } else {
                    document.getElementById('response').innerText = 'Response: ' + data.response + '\nDuration: ' + data.duration.toFixed(2) + ' seconds' + '\nFull JSON: ' + JSON.stringify(data);
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
 This is some simple HTML that will give us a form allowing us to call the /generate endpoint, passing a message and model selection.
 Step 3: Testing your AI-enabled application
 First let's run our Flask application, execute:
 python app.py
 You should see output indicating that the Flask development server is running on port 5000.
 The Flask application is now running locally on Cloud IDE. To access it, click the following button:
 Test your application
 about:blank
 18/19
11/20/25, 12:58 PM
 about:blank
 Try this with different messages and models to see how the responses vary.
 Congratulations you've created your LLM-enabled Flask application!
 Conclusion and next steps
 Congratulations on completing this guided project! You've successfully built a backend for a GenAI application using Flask, integrated multiple AI models, and implemented structured JSON outputs for enhanced
 functionality.
 Key takeaways
 You've learned to set up a Flask application with AI capabilities.
 You've integrated and compared multiple Gemini models (Flash and Pro).
 You've implemented LangChain's JsonOutputParser for structured AI outputs.
 You've gained insights into prompt engineering and model performance analysis.
 You've created a modular and maintainable codebase for AI integration with Google Generative AI.

 Next steps
 To further enhance your skills and application:
 1. Implement caching: Add a caching mechanism to improve performance for repeated queries.
 2. Explore advanced LangChain features: Look into features like memory for maintaining conversation context.
 3. Add more models: Try integrating other Google AI models (Gemini 2.0, etc.).
 4. Implement A/B testing: Create a system to compare responses from Flash and Pro models.
 5. Enhance error handling: Implement more robust error handling and logging.
 6. Explore multimodal capabilities: Gemini models support images, audio, and video - try integrating those!

 Further learning
 Explore the Google Generative AI documentation for more advanced features.
 Dive deeper into LangChain for more sophisticated AI application architectures.
 Learn about prompt engineering techniques to improve AI model outputs.

 Remember, the field of GenAI is rapidly evolving. Keep experimenting, learning, and building to stay at the forefront of this exciting technology!

 Thank you for participating in this workshop. We hope you found it valuable and are inspired to continue your journey in AI-driven application development with Google Gemini!
 19/19
 about:blank