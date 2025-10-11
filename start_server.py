#!/usr/bin/env python3
"""
Startup script for Lead Follow-up AI Agent
Run this from the root directory to start the server
"""

import os
import sys
import uvicorn
from pathlib import Path

def main():
    """Start the FastAPI server"""
    # Get the current directory
    current_dir = Path(__file__).parent.absolute()
    
    # Change to the app directory
    app_dir = current_dir / "app"
    if not app_dir.exists():
        print("❌ Error: app directory not found!")
        print(f"   Current directory: {current_dir}")
        print(f"   Looking for: {app_dir}")
        sys.exit(1)
    
    # Change to app directory
    os.chdir(app_dir)
    
    print("🚀 Starting Lead Follow-up AI Agent...")
    print(f"📁 Working directory: {app_dir}")
    print("🌐 Server will be available at: http://localhost:8000")
    print("📚 API documentation: http://localhost:8000/docs")
    print("🔍 Health check: http://localhost:8000/api/v1/health")
    print("\n" + "=" * 50)
    
    try:
        # Start the server
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()



