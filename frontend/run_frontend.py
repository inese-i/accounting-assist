#!/usr/bin/env python3
"""
Streamlit Frontend Runner
"""

import subprocess
import sys
import os

def main():
    """Run the Streamlit application"""
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(script_dir, "streamlit_app.py")
    
    print("🚀 Starting Streamlit Frontend...")
    print(f"📁 App location: {app_path}")
    print("🌐 The app will be available at: http://localhost:8501")
    print("⚠️  Make sure your FastAPI backend is running on http://localhost:8000")
    print()
    
    try:
        # Run Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", app_path,
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Streamlit app stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
