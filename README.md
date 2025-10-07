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
  "model": "sonar",
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
  "model_used": "sonar",
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
    "sonar",
    "sonar-pro",
    "sonar-reasoning"
  ],
  "default_model": "sonar",
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
- **Default Model:** `sonar`
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
        "model": "sonar-pro"
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

## Related Project: MCP Server

### Overview

A companion MCP (Model Context Protocol) server is available for AI assistants:

🔗 **GitHub**: [atiyil/simple-mcp-server](https://github.com/atiyil/simple-mcp-server)  
📁 **Local**: `~/dev/simple-mcp-server`

The MCP server provides direct integration with AI assistants like Claude Desktop and Cline, allowing them to query Perplexity AI as a tool. It shares the same Perplexity client library but operates independently via the Model Context Protocol.

### Key Differences

| Feature | FastAPI Service | MCP Server |
|---------|----------------|------------|
| **Protocol** | HTTP REST API | MCP (stdio) |
| **Port** | 8000 | N/A (stdio) |
| **Use Case** | Web apps, APIs, scripts | AI assistants (Claude, Cline) |
| **Interface** | HTTP endpoints | Tool calls |
| **Authentication** | Direct API key | Environment variable |
| **Models** | `sonar`, `sonar-pro`, `sonar-reasoning` | `sonar`, `sonar-pro`, `sonar-reasoning` |

### Using Both Together

You can run both services simultaneously without conflicts:

**Terminal 1 - FastAPI Service (for HTTP API):**
```bash
cd ~/dev/perplexity
source venv/bin/activate
python main.py
# Available at http://localhost:8000
```

**Terminal 2 - MCP Server Testing (optional):**
```bash
cd ~/dev/simple-mcp-server
source venv/bin/activate
PERPLEXITY_API_KEY=your_key npx @modelcontextprotocol/inspector python mcp_server.py
# Inspector at http://localhost:6274
```

**AI Assistants (automatic):**
Claude Desktop and Cline will automatically start the MCP server when needed, no manual intervention required.

### When to Use Each

**Use FastAPI Service when:**
- Building web applications
- Creating custom scripts or automation
- Need HTTP API access
- Want to integrate with non-MCP tools
- Building microservices architecture

**Use MCP Server when:**
- Using Claude Desktop
- Using Cline (VS Code extension)
- Want AI assistants to query Perplexity directly
- Need seamless tool integration in conversations
- Working within MCP-compatible environments

### Setup MCP Server

Quick setup for the MCP server:

```bash
# Clone or navigate to the MCP server
cd ~/dev/simple-mcp-server

# Create virtual environment and install dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Test with MCP Inspector
PERPLEXITY_API_KEY=your_key npx @modelcontextprotocol/inspector python mcp_server.py
```

For Claude Desktop configuration, add to `~/Library/Application Support/Claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "perplexity": {
      "command": "python",
      "args": ["/Users/your_username/dev/simple-mcp-server/mcp_server.py"],
      "env": {
        "PERPLEXITY_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

See the [MCP Server README](https://github.com/atiyil/simple-mcp-server) for complete documentation.

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