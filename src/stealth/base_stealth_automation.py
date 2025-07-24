"""
Base Stealth Automation Framework
Provides a reusable, platform-agnostic foundation for stealth web automation
"""

import os
import json
import time
import random
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import undetected_chromedriver as uc
from selenium_stealth import stealth
from fake_useragent import UserAgent


class BaseStealthAutomation(ABC):
    """
    Abstract base class for platform-agnostic stealth automation
    """
    
    def __init__(self, platform_config_path: str = None, headless: bool = True):
        self.platform_config = {}
        self.driver = None
        self.headless = headless
        self.user_agent = UserAgent()
        
        if platform_config_path and os.path.exists(platform_config_path):
            with open(platform_config_path, 'r') as f:
                self.platform_config = json.load(f)
    
    def _create_stealth_driver(self, user_data_dir: str = None) -> webdriver.Chrome:
        """
        Create a stealth-configured Chrome driver
        """
        options = uc.ChromeOptions()
        
        # Basic stealth options
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # User agent rotation
        options.add_argument(f"--user-agent={self.user_agent.random}")
        
        # Headless mode
        if self.headless:
            options.add_argument("--headless=new")
        
        # Custom user data directory for session persistence
        if user_data_dir:
            options.add_argument(f"--user-data-dir={user_data_dir}")
        
        # Create driver
        driver = uc.Chrome(options=options, version_main=None)
        
        # Apply stealth
        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True)
        
        self.driver = driver
        return driver
    
    def _find_element_with_fallback(self, selectors: List[str], timeout: int = 10) -> Optional[Any]:
        """
        Find element using multiple selector fallbacks
        """
        for selector in selectors:
            try:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                return element
            except TimeoutException:
                continue
        
        # Try XPath if CSS selectors fail
        for selector in selectors:
            if selector.startswith("//") or selector.startswith("("):
                try:
                    element = WebDriverWait(self.driver, timeout).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    return element
                except TimeoutException:
                    continue
        
        return None
    
    def _human_like_typing(self, element, text: str):
        """
        Type text with human-like delays
        """
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
    
    def _random_delay(self, min_seconds: float = 1.0, max_seconds: float = 3.0):
        """
        Add random delay to mimic human behavior
        """
        time.sleep(random.uniform(min_seconds, max_seconds))
    
    @abstractmethod
    def login(self, username: str, password: str) -> bool:
        """
        Platform-specific login implementation
        """
        pass
    
    @abstractmethod
    def is_logged_in(self) -> bool:
        """
        Check if user is currently logged in
        """
        pass
    
    def close(self):
        """
        Clean up resources
        """
        if self.driver:
            self.driver.quit()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
