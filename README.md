The project includes three process
1. Batch request GUI
2. Data analysis and visulization
3. Theoretical Model




# Batch request GUI

A feature-rich Python-based chatbot application that interfaces with various large language models. The application includes a user-friendly GUI, supports batch requests, and provides extensive configuration options.

## Features

- Interactive chat interface with AI models
- Support for multiple AI models (OpenAI, Anthropic, Gemini, etc.)
- Configurable API settings
- Batch request processing
- Settings persistence
- Response saving functionality

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd chatbot
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python src/main.py
```

2. Configure Settings:
   - Click the "Settings" button
   - Select your preferred AI model
   - Enter your API URL and API key
   - Adjust temperature and max tokens as needed
   - Add any default prompts
   - Save settings

3. Chat Features:
   - Type messages in the input field and press Enter or click Send
   - View conversation history in the chat display
   - Messages are color-coded for easy identification

4. Batch Processing:
   - Click the "Batch Request" button
   - Enter your prompt
   - Specify the number of requests and interval
   - Monitor progress with the progress bar
   - Save results to a JSON file

## Configuration

### Supported Models

- OpenAI Series (GPT-4, GPT-3.5-turbo)
- Anthropic Series (Claude-2)
- Google Gemini
- Kimi
- Spark

### Settings

- **Model ID**: Select from predefined AI models
- **API URL**: Endpoint URL for the selected model
- **API Key**: Authentication key for the API
- **Temperature**: Controls response randomness (0-1)
- **Max Tokens**: Maximum response length
- **Pre-Input**: Default prompt for all requests

### Batch Processing

- Set number of requests (1-100)
- Configure interval between requests (0.5-60 seconds)
- Save all responses with metadata
- Progress tracking during batch processing

## File Formats

### Saved Responses

Batch responses are saved in JSON format with the following structure:
```json
{
    "timestamp": "YYYYMMDD_HHMMSS",
    "settings": {
        "model": "selected-model",
        "temperature": 0.7,
        "max_tokens": 4096,
        "pre_input": "default-prompt"
    },
    "batch_config": {
        "prompt": "batch-prompt",
        "request_count": 5,
        "request_interval": 2.0
    },
    "responses": [
        "response1",
        "response2",
        ...
    ]
}
```

## Requirements

- Python 3.8+
- PyQt5
- requests
- python-dotenv

## Notes

- Ensure you have valid API credentials before using the application
- Monitor your API usage and rate limits
- Save important conversations and batch results
- Configure appropriate intervals for batch requests to avoid API throttling
"# MSDA7005_Group5_Source-codes_Cog" 
"# MSDA7005_Group5_Source-codes_Cog" 
