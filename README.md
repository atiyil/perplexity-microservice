# Perplexity AI Microservice

A simple FastAPI microservice for querying Perplexity AI. This service provides a RESTful API interface to interact with Perplexity's AI models.

## Features

- FastAPI-based REST API
- Configurable Perplexity AI integration
- Health check endpoint
- Support for multiple Perplexity models
- Flexible query parameters (temperature, max_tokens, system messages)
- Simple and advanced query endpoints
- Comprehensive error handling

## Setup

### Prerequisites

- Python 3.8+
- Perplexity AI API key

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd ~/dev/perplexity
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your API key:**
   
   Edit the `config.txt` file and replace `your_perplexity_api_key_here` with your actual Perplexity AI API key:
   ```
   PERPLEXITY_API_KEY=your_actual_api_key_here
   ```
   
   Alternatively, you can set it as an environment variable:
   ```bash
   export PERPLEXITY_API_KEY=your_actual_api_key_here
   ```

### Running the Service

Start the development server:
```bash
python main.py
```

Or use uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The service will be available at: `http://localhost:8000`

## API Documentation

Once the service is running, you can access:
- Interactive API documentation: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

### Endpoints

#### GET `/`
Returns service information and available endpoints.

**Response:**
```json
{
  "service": "Perplexity AI Microservice",
  "version": "1.0.0",
  "endpoints": {
    "health": "/health",
    "query": "/query",
    "simple_query": "/simple-query"
  }
}
```

#### GET `/health`
Health check endpoint that verifies service status and Perplexity API connectivity.

**Response:**
```json
{
  "status": "healthy",
  "perplexity_api_accessible": true
}
```

#### POST `/query`
Send a query to Perplexity AI with full parameter control.

**Request Body:**
```json
{
  "message": "What is machine learning?",
  "model": "llama-3.1-sonar-small-128k-online",
  "max_tokens": 500,
  "temperature": 0.7,
  "system_message": "You are a helpful AI assistant."
}
```

**Response:**
```json
{
  "success": true,
  "response": "Machine learning is a subset of artificial intelligence...",
  "model_used": "llama-3.1-sonar-small-128k-online",
  "error": null
}
```

#### POST `/simple-query`
Send a simple query with default parameters.

**Request:**
```bash
curl -X POST "http://localhost:8000/simple-query" \
  -H "Content-Type: application/json" \
  -d '"What is the weather today?"'
```

**Response:**
```json
{
  "response": "I don't have access to real-time weather data..."
}
```

#### GET `/models`
Get information about available Perplexity AI models.

**Response:**
```json
{
  "available_models": [
    "llama-3.1-sonar-small-128k-online",
    "llama-3.1-sonar-small-128k-chat",
    "llama-3.1-sonar-large-128k-online",
    "llama-3.1-sonar-large-128k-chat",
    "llama-3.1-8b-instruct",
    "llama-3.1-70b-instruct"
  ],
  "default_model": "llama-3.1-sonar-small-128k-online",
  "note": "Check Perplexity AI documentation for the most current model list"
}
```

## Configuration

The service supports configuration through:

1. **Environment Variables:**
   - `PERPLEXITY_API_KEY`: Your Perplexity AI API key

2. **Configuration File (`config.txt`):**
   ```
   PERPLEXITY_API_KEY=your_api_key_here
   ```

### Default Configuration
- **Base URL:** `https://api.perplexity.ai`
- **Default Model:** `llama-3.1-sonar-small-128k-online`
- **Max Tokens:** `1000`
- **Temperature:** `0.7`

## Example Usage

### Using curl

1. **Simple query:**
   ```bash
   curl -X POST "http://localhost:8000/simple-query" \
     -H "Content-Type: application/json" \
     -d '"Explain quantum computing briefly"'
   ```

2. **Advanced query:**
   ```bash
   curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{
       "message": "Explain quantum computing",
       "max_tokens": 300,
       "temperature": 0.5,
       "system_message": "Explain concepts in simple terms"
     }'
   ```

### Using Python requests

```python
import requests

# Simple query
response = requests.post(
    "http://localhost:8000/simple-query",
    json="What is FastAPI?"
)
print(response.json())

# Advanced query
response = requests.post(
    "http://localhost:8000/query",
    json={
        "message": "What is FastAPI?",
        "max_tokens": 500,
        "temperature": 0.3,
        "model": "llama-3.1-sonar-large-128k-online"
    }
)
print(response.json())
```

## Project Structure

```
perplexity/
├── main.py              # FastAPI application and endpoints
├── config.py            # Configuration management
├── config.txt           # API key configuration file
├── perplexity_client.py # Perplexity AI client
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .gitignore          # Git ignore rules
```

## Development

### Adding New Features

1. **New endpoints:** Add them to `main.py`
2. **Configuration:** Update `config.py`
3. **API client changes:** Modify `perplexity_client.py`

### Error Handling

The service includes comprehensive error handling:
- HTTP errors from Perplexity API
- Configuration errors (missing API key)
- Unexpected response formats
- Network timeouts

## Deployment

For production deployment, consider:

1. **Environment Variables:** Use environment variables instead of config files
2. **HTTPS:** Enable HTTPS for security
3. **Rate Limiting:** Implement rate limiting
4. **Monitoring:** Add logging and monitoring
5. **Docker:** Use the provided Dockerfile for containerization

## License

This project is open source and available under the MIT License.