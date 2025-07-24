"""
Telegram/Telethon Setup Module
Provides easy setup for Telegram bot integration
"""

import os
import json
import asyncio
from typing import Dict, Optional
from pathlib import Path

from telethon import TelegramClient
from telethon.sessions import StringSession


class TelegramSetup:
    """
    Easy setup for Telegram bot integration using Telethon
    """
    
    def __init__(self, api_id: int = None, api_hash: str = None):
        self.api_id = api_id or int(os.getenv("TELEGRAM_API_ID", "0"))
        self.api_hash = api_hash or os.getenv("TELEGRAM_API_HASH", "")
        self.session_name = "selenium_telethon_session"
        self.config_path = "config/telegram_config.json"
        
    async def create_session(self) -> str:
        """
        Create a new Telegram session and return the session string
        """
        if not self.api_id or not self.api_hash:
            raise ValueError("API ID and Hash are required. Set TELEGRAM_API_ID and TELEGRAM_API_HASH environment variables.")
        
        print("🔐 Creating new Telegram session...")
        print("Please enter your phone number when prompted.")
        
        client = TelegramClient(StringSession(), self.api_id, self.api_hash)
        await client.start()
        
        session_string = client.session.save()
        
        # Save session string to config
        config = {
            "session_string": session_string,
            "api_id": self.api_id,
            "api_hash": self.api_hash,
            "session_name": self.session_name,
            "created_at": str(__import__('datetime').datetime.now())
        }
        
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print("✅ Session created and saved to config/telegram_config.json")
        return session_string
    
    def load_session(self) -> Optional[Dict[str, any]]:
        """
        Load existing session configuration
        """
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return None
    
    async def test_connection(self) -> bool:
        """
        Test the Telegram connection
        """
        config = self.load_session()
        if not config:
            print("❌ No session found. Please create a session first.")
            return False
        
        try:
            session = StringSession(config["session_string"])
            client = TelegramClient(session, config["api_id"], config["api_hash"])
            await client.connect()
            
            me = await client.get_me()
            print(f"✅ Connected as {me.first_name} (@{me.username})")
            await client.disconnect()
            return True
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def create_env_template(self):
        """
        Create .env template file
        """
        env_content = """# Telegram Configuration
TELEGRAM_API_ID=your_api_id_here
TELEGRAM_API_HASH=your_api_hash_here

# Optional: Specific channels to monitor
TELEGRAM_CHANNELS=channel1,channel2,channel3

# Optional: Session file location
TELEGRAM_SESSION_FILE=telegram_session.session
"""
        
        with open(".env.template", "w") as f:
            f.write(env_content)
        
        print("✅ Created .env.template file")
    
    def create_channels_config(self, channels: list = None):
        """
        Create channels configuration file
        """
        if channels is None:
            channels = ["binary_trading_club", "forex_signals", "crypto_alerts"]
        
        config = {
            "channels": channels,
            "monitoring": {
                "enabled": True,
                "check_interval": 5,
                "max_messages": 100
            },
            "filtering": {
                "keywords": ["buy", "sell", "signal", "trade", "entry", "exit"],
                "excluded_words": ["spam", "scam", "fake"]
            }
        }
        
        os.makedirs("config", exist_ok=True)
        with open("config/channels.json", "w") as f:
            json.dump(config, f, indent=2)
        
        print("✅ Created config/channels.json")


async def setup_telegram():
    """
    Interactive setup for Telegram integration
    """
    setup = TelegramSetup()
    
    print("🚀 Telegram Setup Wizard")
    print("=" * 30)
    
    # Check if session exists
    if setup.load_session():
        print("📱 Existing session found")
        if await setup.test_connection():
            print("✅ Session is active")
            return
    
    # Create new session
    print("\n🔐 Creating new session...")
    api_id = input("Enter your API ID: ").strip()
    api_hash = input("Enter your API Hash: ").strip()
    
    setup.api_id = int(api_id)
    setup.api_hash = api_hash
    
    await setup.create_session()
    await setup.test_connection()
    
    # Create additional configs
    setup.create_env_template()
    setup.create_channels_config()
    
    print("\n✅ Setup complete!")
    print("📁 Files created:")
    print("   - config/telegram_config.json")
    print("   - config/channels.json")
    print("   - .env.template")


def main():
    """Main function for command-line usage"""
    asyncio.run(setup_telegram())


if __name__ == "__main__":
    main()
