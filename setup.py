#!/usr/bin/env python3
"""
Setup script for Selenium-Telethon Easy Setup
"""

import os
import subprocess
import sys
from pathlib import Path


class EasySetup:
    """
    Automated setup for the entire framework
    """
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
    
    def check_python_version(self):
        """Check Python version compatibility"""
        if sys.version_info < (3, 8):
            print("❌ Python 3.8+ is required")
            return False
        print("✅ Python version compatible")
        return True
    
    def install_dependencies(self):
        """Install required packages"""
        print("📦 Installing dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Dependencies installed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False
    
    def create_directories(self):
        """Create necessary directories"""
        directories = [
            "config",
            "src/platforms",
            "examples",
            "tests",
            "docs",
            "logs",
            "data/screenshots",
            "data/sessions"
        ]
        
        for directory in directories:
            os.makedirs(self.base_dir / directory, exist_ok=True)
        
        print("✅ Directory structure created")
    
    def create_env_file(self):
        """Create .env file template"""
        env_content = """# Selenium-Telethon Easy Setup Configuration

# Telegram Configuration
TELEGRAM_API_ID=your_api_id_here
TELEGRAM_API_HASH=your_api_hash_here
TELEGRAM_CHANNELS=channel1,channel2,channel3

# Platform Credentials (add your platforms here)
PLATFORM_USERNAME=your_username
PLATFORM_PASSWORD=your_password

# Chrome Configuration
CHROME_USER_DATA_DIR=./chrome_user_data
HEADLESS=true

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/automation.log
"""
        
        with open(self.base_dir / ".env", "w") as f:
            f.write(env_content)
        
        print("✅ Created .env template")
    
    def create_quick_start_script(self):
        """Create quick start script"""
        script_content = """#!/usr/bin/env python3
# Quick start script for new platforms

import sys
import os
from pathlib import Path

def main():
    print("🚀 Selenium-Telethon Easy Setup - Quick Start")
    print("=" * 50)
    
    # Check if platform name provided
    if len(sys.argv) < 3:
        print("Usage: python quick_start.py <platform_name> <login_url>")
        print("Example: python quick_start.py binance https://binance.com/login")
        return
    
    platform_name = sys.argv[1]
    login_url = sys.argv[2]
    
    # Generate platform template
    os.system(f"python tools/generate_platform_template.py --name {platform_name} --url {login_url}")
    
    print(f"\n✅ Generated {platform_name} platform template")
    print("\nNext steps:")
    print(f"1. Edit config/{platform_name}_config.json")
    print(f"2. Set environment variables in .env")
    print(f"3. Run: python examples/{platform_name}_example.py")

if __name__ == "__main__":
    main()
"""
        
        with open(self.base_dir / "quick_start.py", "w") as f:
            f.write(script_content)
        
        # Make executable
        os.chmod(self.base_dir / "quick_start.py", 0o755)
        print("✅ Created quick_start.py")
    
    def create_init_files(self):
        """Create __init__.py files for Python packages"""
        init_files = [
            "src/__init__.py",
            "src/stealth/__init__.py",
            "src/platforms/__init__.py",
            "tools/__init__.py"
        ]
        
        for file in init_files:
            with open(self.base_dir / file, "w") as f:
                f.write("# Package initialization\n")
        
        print("✅ Created package init files")
    
    def run_setup(self):
        """Run complete setup"""
        print("🚀 Starting Selenium-Telethon Easy Setup...")
        print("=" * 50)
        
        if not self.check_python_version():
            return False
        
        if not self.install_dependencies():
            return False
        
        self.create_directories()
        self.create_env_file()
        self.create_quick_start_script()
        self.create_init_files()
        
        print("\n✅ Setup complete!")
        print("\nNext steps:")
        print("1. Edit .env file with your credentials")
        print("2. Run: python src/telegram_setup.py (for Telegram)")
        print("3. Run: python quick_start.py <platform> <url> (for new platform)")
        
        return True


def main():
    """Main setup function"""
    setup = EasySetup()
    setup.run_setup()


if __name__ == "__main__":
    main()
