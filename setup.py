#!/usr/bin/env python3
"""
AI Legal Oracle - Quick Setup Script
=====================================
This script will install all required dependencies for your enhanced legal AI app.
"""

import subprocess
import sys
import os

def run_command(command):
    """Run a command and return success status"""
    try:
        subprocess.check_call(command, shell=True)
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("🚀 AI Legal Oracle - Quick Setup Script")
    print("=" * 45)
    print()
    
    # Install core dependencies
    print("📦 Installing core dependencies...")
    if run_command("pip install -r requirements_safe.txt"):
        print("✅ Core dependencies installed successfully!")
    else:
        print("❌ Failed to install core dependencies")
        return
    
    print()
    
    # Install optional dependencies
    print("🔧 Installing optional dependencies...")
    
    optional_packages = [
        ("python-docx", "DOCX file support"),
        ("matplotlib", "Chart generation"),
        ("wordcloud", "Word cloud visualizations")
    ]
    
    for package, description in optional_packages:
        print(f"Installing {package} for {description}...")
        if run_command(f"pip install {package}"):
            print(f"✅ {package} installed successfully!")
        else:
            print(f"⚠️ Failed to install {package} (optional)")
    
    print()
    print("✅ Setup complete!")
    print()
    print("🚀 To run your enhanced app:")
    print("   streamlit run enhanced_app.py")
    print()
    print("💡 Make sure to create a .env file with your OpenAI API key:")
    print("   OPENAI_API_KEY=your_api_key_here")
    print()
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("📝 Creating sample .env file...")
        with open('.env', 'w') as f:
            f.write("# AI Legal Oracle Environment Variables\n")
            f.write("# Replace 'your_openai_api_key_here' with your actual API key\n")
            f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
        print("✅ Sample .env file created. Please edit it with your API key.")
    
    print("\n🎉 Your AI Legal Oracle is ready to launch!")

if __name__ == "__main__":
    main()