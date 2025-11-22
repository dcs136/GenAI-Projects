# Gradio Gemini ChatBot Project

A simple ChatBot application using Google's Gemini API and Gradio web interface.

## Features

- 🤖 Powered by Google Gemini AI
- 🎨 Beautiful web interface using Gradio
- 💬 Multi-turn conversation support
- 🔄 Chat history management
- 📝 Easy to use and deploy

## Setup Instructions

### 1. Clone or Create Project Structure

```bash
mkdir gradio-gemini-chatbot
cd gradio-gemini-chatbot
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

The `.env` file already contains your API key configuration:

```
GOOGLE_API_KEY=AIzaSyCM8jQEXJ1QPbATWc1Ap9W_-0_JOfkBiC0
FLASK_ENV=development
FLASK_DEBUG=True
```

**Important:** Never commit the `.env` file to version control. It's already listed in `.gitignore`.

### 5. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:7860`

## Project Structure

```
gradio-gemini-chatbot/
├── app.py                 # Main application
├── .env                   # Environment variables (API keys)
├── .gitignore            # Git ignore rules
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Usage

1. Open your browser to `http://localhost:7860`
2. Type your message in the text box
3. Click "Send" or press Enter
4. The Gemini AI will respond
5. Use "Clear" button to reset conversation history

## Security Notes

- ✅ `.env` file is in `.gitignore` - API keys won't be committed
- ✅ Never share your API key
- ✅ Use environment variables for sensitive data
- ✅ Review Google's API usage and pricing

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GOOGLE_API_KEY` | Your Google Gemini API key |
| `FLASK_ENV` | Development environment |
| `FLASK_DEBUG` | Enable debug mode |

## Troubleshooting

### Issue: "GOOGLE_API_KEY not found"
- Make sure `.env` file exists in the project root
- Verify API key is correctly set
- Check that `python-dotenv` is installed

### Issue: "API quota exceeded"
- Check your Google Cloud API usage
- Wait for rate limit to reset
- Review pricing and usage limits

## Resources

- [Google Generative AI Python](https://github.com/google/generative-ai-python)
- [Gradio Documentation](https://www.gradio.app)
- [Google AI Studio](https://aistudio.google.com)

## License

This project is open source and available under the MIT License.
