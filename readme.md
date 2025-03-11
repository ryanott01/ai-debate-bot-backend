# AI Chat Model Microservice

A lightweight Flask microservice that integrates with multiple AI chat model providers (OpenAI, Anthropic, Google) for local content generation.

## Features

- Simple local setup with Flask development server
- Support for multiple model providers:
  - OpenAI (GPT models)
  - Anthropic (Claude models)
  - Google (Gemini models)
- API key management through environment variables
- Stateless design (no database)
- Clean REST API for interacting with AI models
- Easy to add or remove providers and models

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/ai-chat-microservice.git
cd ai-chat-microservice
```

2. **Create a virtual environment and activate it:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Set up your configuration:**

   - Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

   - Edit `.env` to add your API keys:
   ```
   OPENAI_API_KEY=sk-your-openai-api-key-here
   ANTHROPIC_API_KEY=sk-ant-your-anthropic-api-key-here
   GOOGLE_API_KEY=your-google-api-key-here
   ```

   Note: You only need to set API keys for the providers you want to use.

## Starting the Server

Start the Flask development server:

```bash
python app.py
```

The server will run on http://localhost:4000 by default (configurable in `.env`).

## API Documentation

### List Providers

Get all configured providers.

```
GET /providers
```

Response:
```json
{
  "providers": ["openai", "anthropic", "google"]
}
```

### List All Models

Get all available models from all configured providers.

```
GET /models
```

Response:
```json
{
  "openai": [
    {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo"},
    {"id": "gpt-4", "name": "GPT-4"},
    {"id": "gpt-4-turbo", "name": "GPT-4 Turbo"}
  ],
  "anthropic": [
    {"id": "claude-3-opus-20240229", "name": "Claude 3 Opus"},
    {"id": "claude-3-sonnet-20240229", "name": "Claude 3 Sonnet"},
    {"id": "claude-3-haiku-20240307", "name": "Claude 3 Haiku"},
    {"id": "claude-3.5-sonnet-20240620", "name": "Claude 3.5 Sonnet"}
  ]
}
```

### List Models for a Specific Provider

Get models for a specific provider.

```
GET /models/{provider}
```

Response:
```json
{
  "provider": "anthropic",
  "models": [
    {"id": "claude-3-opus-20240229", "name": "Claude 3 Opus"},
    {"id": "claude-3-sonnet-20240229", "name": "Claude 3 Sonnet"},
    {"id": "claude-3-haiku-20240307", "name": "Claude 3 Haiku"},
    {"id": "claude-3.5-sonnet-20240620", "name": "Claude 3.5 Sonnet"}
  ]
}
```

### Generate Response

Send a prompt to a model and get a response.

```
POST /generate
```

Request Body:
```json
{
  "provider": "openai",
  "model": "gpt-3.5-turbo",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Tell me a joke about programming."}
  ],
  "options": {
    "temperature": 0.7,
    "max_tokens": 500
  }
}
```

Response:
```json
{
  "provider": "openai",
  "model": "gpt-3.5-turbo",
  "response": "Why do programmers prefer dark mode? Because light attracts bugs!",
  "usage": {
    "prompt_tokens": 29,
    "completion_tokens": 15,
    "total_tokens": 44
  }
}
```

## Adding or Modifying Models

### Adding New Models to Existing Providers

To add new models to an existing provider, update the `_models` list in the provider's class:

```python
# Example: Adding a new OpenAI model in providers/openai_provider.py
def __init__(self, api_key: str):
    self.client = openai.OpenAI(api_key=api_key)
    self._models = [
        {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo"},
        {"id": "gpt-4", "name": "GPT-4"},
        {"id": "gpt-4-turbo", "name": "GPT-4 Turbo"},
        # Add your new model here:
        {"id": "gpt-4-1106-preview", "name": "GPT-4 Turbo Preview"}
    ]
```

### Updating Existing Models

To update an existing model (e.g., to update the model ID or display name):

```python
# Example: Updating a Claude model in providers/anthropic_provider.py
def __init__(self, api_key: str):
    self.client = anthropic.Anthropic(api_key=api_key)
    self._models = [
        # Updated model ID for Claude 3 Opus
        {"id": "claude-3-opus-20240229-v2", "name": "Claude 3 Opus v2"},
        {"id": "claude-3-sonnet-20240229", "name": "Claude 3 Sonnet"},
        {"id": "claude-3-haiku-20240307", "name": "Claude 3 Haiku"}
    ]
```

### Adding a New Provider

To add a completely new AI provider:

1. **Create a new provider class** in the `providers` directory:

```python
# providers/new_provider.py
from typing import List, Dict, Any
from .base import BaseProvider

class NewProvider(BaseProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self._models = [
            {"id": "model-1", "name": "Model 1"},
            {"id": "model-2", "name": "Model 2"}
        ]

    @property
    def name(self) -> str:
        return "new_provider"

    @property
    def available_models(self) -> List[Dict[str, str]]:
        return self._models

    def generate(self, model: str, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        # Implement the logic to call your provider's API
        # Process messages and return the response
        response = "Your implementation here"

        return {
            "provider": self.name,
            "model": model,
            "response": response
        }
```

2. **Update `providers/__init__.py`** to import and register your provider:

```python
# Add import at the top
from .new_provider import NewProvider

# Add registration in register_configured_providers function
if app.config.get("NEW_PROVIDER_API_KEY"):
    try:
        register_provider(NewProvider(app.config["NEW_PROVIDER_API_KEY"]))
        print("✅ NewProvider registered successfully")
    except Exception as e:
        print(f"❌ Failed to register NewProvider: {str(e)}")
```

3. **Update `config.py`** to read the API key:

```python
# Add this line in configure_app function
app.config["NEW_PROVIDER_API_KEY"] = os.environ.get("NEW_PROVIDER_API_KEY", "")
```

4. **Update `.env.example`** to include the new provider's API key:

```
# New Provider API Key
NEW_PROVIDER_API_KEY=
```

### Removing a Provider

To remove a provider, you can either:

1. **Leave the API key empty** in your `.env` file (easiest method)
2. **Comment out or remove** the provider registration in `providers/__init__.py`
3. **Use the `unregister_provider` function** to dynamically remove a provider:

```python
from providers import unregister_provider

# Example: Remove the OpenAI provider
unregister_provider("openai")
```

## Testing with Python

Here's a simple Python script to test generating a response with Claude:

```python
import requests
import json

# Generate a response using Anthropic's Claude
response = requests.post('http://localhost:4000/generate', json={
    "provider": "anthropic",
    "model": "claude-3-haiku-20240307",
    "messages": [
        {"role": "user", "content": "Explain the concept of REST APIs in simple terms."}
    ],
    "options": {
        "max_tokens": 300
    }
})

# Print the response
result = response.json()
print(json.dumps(result, indent=2))
print("\nResponse content:")
print(result["response"])
```

## Troubleshooting

### API Key Issues

If you're having issues with API keys:

1. Verify your API keys are correctly set in the `.env` file
2. Check the server logs for any error messages during provider registration
3. Make sure you're using the correct API key format for each provider (OpenAI keys start with `sk-`, Anthropic keys start with `sk-ant-`)

### Port Conflicts

If port 4000 is already in use:

1. Change the `PORT` value in your `.env` file
2. Restart the server

### Provider-Specific Issues

If a specific provider is not working:

1. Check if the provider was successfully registered (look for "✅ [Provider] registered successfully" in the logs)
2. Verify your API key has the necessary permissions for the models you're trying to use
3. Make sure you're using model IDs that are correctly formatted and available

## Examples with curl

### List Providers
```bash
curl http://localhost:4000/providers
```

### List Models from OpenAI
```bash
curl http://localhost:4000/models/openai
```

### Generate Response with GPT-4
```bash
curl -X POST http://localhost:4000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "openai",
    "model": "gpt-4",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "What are three interesting facts about the ocean?"}
    ],
    "options": {
      "temperature": 0.7,
      "max_tokens": 300
    }
  }'
```

### Generate Response with Claude
```bash
curl -X POST http://localhost:4000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "anthropic",
    "model": "claude-3-haiku-20240307",
    "messages": [
      {"role": "user", "content": "Explain quantum computing in simple terms."}
    ],
    "options": {
      "max_tokens": 300
    }
  }'
```
