#!/usr/bin/env python3
"""
Startup script for the DMS Dashboard API
Supports both development and production environments
"""
import os
import uvicorn
from app.main import app

if __name__ == "__main__":
    # Get port from environment variable (for production) or default to 8000
    port = int(os.getenv("PORT", 8000))
    # Only enable reload in development
    reload = os.getenv("ENVIRONMENT", "development") == "development"
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=reload,
        log_level="info"
    )
