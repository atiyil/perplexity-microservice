# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Common Development Commands

### Running the Service
```bash
# Development server with auto-reload
python main.py

# Or using uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Environment Setup
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Docker Operations
```bash
# Build image
docker build -t perplexity-microservice .

# Run container
docker run -p 8000:8000 -e PERPLEXITY_API_KEY=your_key perplexity-microservice

# Health check
curl http://localhost:8000/health
```

### Testing the API
```bash
# Health check
curl http://localhost:8000/health

# Simple query
curl -X POST "http://localhost:8000/simple-query" \
  -H "Content-Type: application/json" \
  -d '"What is machine learning?"'

# Advanced query
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explain quantum computing",
    "max_tokens": 300,
    "temperature": 0.5,
    "system_message": "Explain concepts in simple terms"
  }'

# Get available models
curl http://localhost:8000/models
```

## Architecture Overview

This is a FastAPI-based microservice that provides a REST API wrapper around the Perplexity AI API.

### Core Components

- **`main.py`**: FastAPI application with endpoint definitions and request/response models using Pydantic
- **`perplexity_client.py`**: Async HTTP client for Perplexity AI API interactions using httpx
- **`config.py`**: Configuration management with support for environment variables and config files

### Key Architectural Patterns

- **Singleton Configuration**: Single global `config` instance loaded at startup
- **Singleton Client**: Single global `perplexity_client` instance for API interactions  
- **Async/Await**: All API interactions are asynchronous using httpx
- **Structured Error Handling**: Consistent error responses with success/failure indicators
- **Pydantic Models**: Type-safe request/response validation

### API Design

The service provides three main interaction patterns:

1. **Simple Query** (`/simple-query`): Accepts plain string, returns plain response
2. **Advanced Query** (`/query`): Full parameter control with structured request/response
3. **Health Check** (`/health`): Service status and API connectivity verification

### Configuration Strategy

Priority order for API key loading:
1. `PERPLEXITY_API_KEY` environment variable
2. `config.txt` file (supports both plain key and KEY=value format)
3. Falls back to error if neither found

## Important Implementation Details

### Error Handling Pattern
All endpoints use try/catch blocks that distinguish between:
- HTTP errors from Perplexity API (network/auth issues)
- Unexpected response formats (API contract changes)
- General exceptions (code bugs)

### Response Processing
The client expects Perplexity API responses in OpenAI-compatible format:
```python
response["choices"][0]["message"]["content"]
```

### Default Model Configuration
- Default model: `llama-3.1-sonar-small-128k-online`
- Supports both online (web search) and chat (context-only) models
- Model selection affects whether responses include real-time web data

### Security Considerations
- API key is loaded once at startup and stored in memory
- Docker image runs as non-root user
- Configuration files (`config.txt`) are git-ignored
- No API key logging or exposure in error messages