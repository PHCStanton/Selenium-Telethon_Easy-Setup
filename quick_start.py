#!/usr/bin/env python3
"""
Quick start script for new platform integration
"""

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
