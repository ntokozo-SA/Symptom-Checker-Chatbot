#!/usr/bin/env python3
"""
Startup script for the Symptom Checker API
This script provides an easy way to run the Flask application
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import flask_cors
        print("✅ All dependencies are installed!")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def start_server():
    """Start the Flask server"""
    print("🚀 Starting Symptom Checker API...")
    print("=" * 50)
    
    # Check if dependencies are installed
    if not check_dependencies():
        return False
    
    # Get the directory of this script
    script_dir = Path(__file__).parent.absolute()
    
    # Change to the script directory
    os.chdir(script_dir)
    
    # Start the Flask app
    try:
        print("📡 Starting Flask server on http://localhost:5000")
        print("🔄 Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Import and run the Flask app
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return True
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False

def open_frontend():
    """Open the frontend in a web browser"""
    frontend_path = Path(__file__).parent / "frontend.html"
    if frontend_path.exists():
        print("🌐 Opening frontend in browser...")
        webbrowser.open(f'file://{frontend_path.absolute()}')
    else:
        print("❌ Frontend file not found: frontend.html")

def main():
    """Main function"""
    print("🏥 Symptom Checker Chatbot")
    print("=" * 30)
    
    # Check if we should open the frontend
    open_browser = "--open" in sys.argv or "-o" in sys.argv
    
    # Start the server
    if start_server():
        if open_browser:
            # Wait a moment for the server to start
            time.sleep(2)
            open_frontend()
        return True
    else:
        return False

if __name__ == "__main__":
    main() 