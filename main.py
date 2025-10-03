"""FastAPI microservice for querying Perplexity AI."""

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from typing import Optional
import httpx
from perplexity_client import perplexity_client

app = FastAPI(
    title="Perplexity AI Microservice",
    description="A simple microservice for querying Perplexity AI",
    version="1.0.0"
)


class QueryRequest(BaseModel):
    """Request model for Perplexity AI queries."""
    message: str = Field(..., description="The question or prompt to send to Perplexity AI")
    model: Optional[str] = Field(None, description="Model to use (optional)")
    max_tokens: Optional[int] = Field(None, description="Maximum tokens in response (optional)")
    temperature: Optional[float] = Field(None, description="Response randomness 0-1 (optional)")
    system_message: Optional[str] = Field(None, description="Optional system message for context")


class QueryResponse(BaseModel):
    """Response model for Perplexity AI queries."""
    success: bool = Field(..., description="Whether the query was successful")
    response: Optional[str] = Field(None, description="The AI response text")
    error: Optional[str] = Field(None, description="Error message if query failed")
    model_used: Optional[str] = Field(None, description="The model that was used")


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str = Field(..., description="Service status")
    perplexity_api_accessible: bool = Field(..., description="Whether Perplexity API is accessible")


@app.get("/", response_model=dict)
async def root():
    """Root endpoint with service information."""
    return {
        "service": "Perplexity AI Microservice",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "query": "/query",
            "simple_query": "/simple-query"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    try:
        api_accessible = await perplexity_client.health_check()
        return HealthResponse(
            status="healthy" if api_accessible else "degraded",
            perplexity_api_accessible=api_accessible
        )
    except Exception as e:
        return HealthResponse(
            status="unhealthy",
            perplexity_api_accessible=False
        )


@app.post("/query", response_model=QueryResponse)
async def query_perplexity(request: QueryRequest):
    """
    Send a query to Perplexity AI with full control over parameters.
    """
    try:
        response = await perplexity_client.query(
            message=request.message,
            model=request.model,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            system_message=request.system_message
        )
        
        # Extract the response text
        if "choices" in response and len(response["choices"]) > 0:
            response_text = response["choices"][0]["message"]["content"]
            model_used = response.get("model", request.model)
            
            return QueryResponse(
                success=True,
                response=response_text,
                model_used=model_used
            )
        else:
            return QueryResponse(
                success=False,
                error="Unexpected response format from Perplexity API"
            )
            
    except httpx.HTTPError as e:
        return QueryResponse(
            success=False,
            error=f"HTTP error: {str(e)}"
        )
    except Exception as e:
        return QueryResponse(
            success=False,
            error=f"Unexpected error: {str(e)}"
        )


@app.post("/simple-query")
async def simple_query(request: Request):
    """
    Send a simple query to Perplexity AI and return just the response text.
    
    This endpoint accepts a plain string question in the request body.
    """
    try:
        # Read the raw request body and decode it as a plain string
        body = await request.body()
        question = body.decode('utf-8').strip('"')  # Remove surrounding quotes if present
        
        response_text = await perplexity_client.simple_query(question)
        return response_text
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/models")
async def get_available_models():
    """
    Get information about available Perplexity AI models.
    
    Note: This returns the commonly available models. Check Perplexity documentation for the most up-to-date list.
    """
    return {
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)