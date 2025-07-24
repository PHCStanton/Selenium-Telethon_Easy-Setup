#!/usr/bin/env python3
"""
Selector Discovery Tool
Automatically discovers stable selectors for web platforms
"""

import json
import time
from typing import List, Dict, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import undetected_chromedriver as uc


class SelectorDiscovery:
    """
    Discovers and validates selectors for web platforms
    """
    
    def __init__(self, url: str, headless: bool = True):
        self.url = url
        self.headless = headless
        self.driver = None
        self.discovered_selectors = {}
    
    def _create_driver(self):
        """Create Chrome driver for discovery"""
        options = uc.ChromeOptions()
        if self.headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        self.driver = uc.Chrome(options=options)
    
    def discover_login_selectors(self) -> Dict[str, List[str]]:
        """
        Discover selectors for login form elements
        """
        if not self.driver:
            self._create_driver()
        
        self.driver.get(self.url)
        time.sleep(3)  # Wait for page load
        
        selectors = {
            "username": [],
            "password": [],
            "submit": [],
            "login_verification": []
        }
        
        # Discover username/email fields
        username_selectors = [
            "input[type='email']",
            "input[name='email']",
            "input[name='username']",
            "input[name='user']",
            "input[id='email']",
            "input[id='username']",
            "input[placeholder*='email' i]",
            "input[placeholder*='user' i]",
            "input[placeholder*='login' i]"
        ]
        selectors["username"] = self._find_valid_selectors(username_selectors)
        
        # Discover password fields
        password_selectors = [
            "input[type='password']",
            "input[name='password']",
            "input[name='pass']",
            "input[id='password']",
            "input[placeholder*='password' i]",
            "input[placeholder*='pass' i]"
        ]
        selectors["password"] = self._find_valid_selectors(password_selectors)
        
        # Discover submit buttons
        submit_selectors = [
            "button[type='submit']",
            "button[class*='login' i]",
            "button[class*='signin' i]",
            "button[class*='submit' i]",
            "input[type='submit']",
            "button[id*='login' i]",
            "button[id*='signin' i]",
            "button[aria-label*='login' i]",
            "button[aria-label*='signin' i]"
        ]
        selectors["submit"] = self._find_valid_selectors(submit_selectors)
        
        # Discover login verification elements
        verification_selectors = [
            "[class*='dashboard' i]",
            "[class*='account' i]",
            "[href*='dashboard' i]",
            "[href*='account' i]",
            "[class*='profile' i]",
            "[class*='user' i]"
        ]
        selectors["login_verification"] = self._find_valid_selectors(verification_selectors)
        
        self.discovered_selectors = selectors
        return selectors
    
    def _find_valid_selectors(self, selectors: List[str]) -> List[str]:
        """Find valid selectors that exist on the page"""
        valid_selectors = []
        
        for selector in selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    valid_selectors.append(selector)
            except:
                continue
        
        return valid_selectors
    
    def generate_config(self) -> Dict[str, Any]:
        """Generate configuration based on discovered selectors"""
        if not self.discovered_selectors:
            self.discover_login_selectors()
        
        config = {
            "platform_name": "new_platform",
            "urls": {
                "login": self.url,
                "dashboard": self.url.replace("/login", "/dashboard"),
                "base": "/".join(self.url.split("/")[:3])
            },
            "selectors": self.discovered_selectors,
            "stealth": {
                "enabled": True,
                "platform_specific": {
                    "custom_headers": {},
                    "additional_delays": [1, 3]
                }
            }
        }
        
        return config
    
    def save_config(self, filename: str = None):
        """Save discovered selectors to config file"""
        if not filename:
            filename = f"config/discovered_selectors.json"
        
        config = self.generate_config()
        
        with open(filename, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Configuration saved to {filename}")
    
    def print_report(self):
        """Print discovery report"""
        if not self.discovered_selectors:
            self.discover_login_selectors()
        
        print("\n🔍 Selector Discovery Report")
        print("=" * 50)
        
        for element_type, selectors in self.discovered_selectors.items():
            print(f"\n{element_type.upper()}:")
            if selectors:
                for selector in selectors:
                    print(f"  - {selector}")
            else:
                print("  ❌ No selectors found")
    
    def close(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()


def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Discover selectors for web platforms")
    parser.add_argument("--url", required=True, help="Login URL to analyze")
    parser.add_argument("--output", help="Output config file path")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    
    args = parser.parse_args()
    
    discovery = SelectorDiscovery(args.url, headless=args.headless)
    
    try:
        discovery.print_report()
        
        if args.output:
            discovery.save_config(args.output)
        else:
            discovery.save_config()
            
    finally:
        discovery.close()


if __name__ == "__main__":
    main()
