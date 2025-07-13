#!/usr/bin/env python3
"""
Simple Flask app runner for deployment.
This version handles database connection failures gracefully.
"""

import os
import sys

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def run_app():
    try:
        from app import app
        
        print("🚀 Starting Portfolio Application...")
        print("🌐 Access your portfolio at:")
        
        port = int(os.getenv('PORT', 5000))
        host = os.getenv('HOST', '0.0.0.0')
        
        if host == '0.0.0.0':
            print(f"   Local:    http://localhost:{port}")
            print(f"   Network:  http://0.0.0.0:{port}")
        else:
            print(f"   {host}:{port}")
        
        print("-" * 50)
        print("💡 Use Ctrl+C to stop the server")
        print("-" * 50)
        
        # Run the app
        app.run(
            host=host,
            port=port,
            debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
        )
        
    except ImportError as e:
        print(f"❌ Error importing app: {e}")
        print("💡 Make sure you're in the correct directory")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting app: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_app()
