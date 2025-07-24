# Selenium-Telethon Easy Setup 🚀

A complete, portable framework for stealth web automation with Telegram integration. This package provides everything you need to quickly set up automated web interactions and Telegram bot monitoring.

## 📦 What's Included

- **Base Stealth Framework** - Platform-agnostic stealth automation
- **Template Generator** - One-command platform setup
- **Selector Discovery** - Automated selector identification
- **Telegram Integration** - Easy Telethon setup
- **Complete Examples** - Ready-to-use templates

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or copy this directory
git clone <repository-url> Selenium-Telethon-Easy-Setup
cd Selenium-Telethon-Easy-Setup

# Install dependencies
pip install -r requirements.txt
```

### 2. Telegram Setup (Optional)

```bash
# Interactive setup
python src/telegram_setup.py

# Or manual setup
export TELEGRAM_API_ID=your_api_id
export TELEGRAM_API_HASH=your_api_hash
```

### 3. Platform Integration

#### Method 1: Template Generator (Recommended)
```bash
# Generate complete platform template
python tools/generate_platform_template.py --name "binance" --url "https://binance.com/login"
```

#### Method 2: Selector Discovery
```bash
# Discover selectors automatically
python tools/selector_discovery.py --url "https://platform.com/login"
```

## 📁 Directory Structure

```
Selenium-Telethon-Easy-Setup/
├── src/
│   ├── stealth/
│   │   └── base_stealth_automation.py  # Core stealth framework
│   ├── telegram_setup.py               # Telegram integration
│   └── platforms/                      # Generated platform classes
├── tools/
│   ├── generate_platform_template.py   # Template generator
│   └── selector_discovery.py           # Selector discovery
├── config/
│   ├── telegram_config.json           # Telegram session
│   ├── channels.json                 # Channel monitoring
│   └── [platform]_config.json       # Platform configs
├── examples/
│   └── [platform]_example.py         # Usage examples
├── tests/
│   └── test_[platform]_stealth.py   # Platform tests
└── docs/
    └── [platform]_integration.md    # Platform guides
```

## 🛠️ Usage Examples

### Basic Platform Integration

```python
from src.platforms.binance_stealth import BinanceStealthAutomation

# Initialize
automation = BinanceStealthAutomation(headless=False)

# Create driver
automation._create_stealth_driver()

# Login
success = automation.login("username", "password")
print(f"Login: {'Success' if success else 'Failed'}")

# Cleanup
automation.close()
```

### Telegram Monitoring

```python
from telethon import TelegramClient
import json

# Load configuration
with open('config/telegram_config.json') as f:
    config = json.load(f)

# Create client
client = TelegramClient(
    StringSession(config['session_string']),
    config['api_id'],
    config['api_hash']
)

# Use client...
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```bash
# Telegram
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_CHANNELS=channel1,channel2,channel3

# Platform credentials
PLATFORM_USERNAME=your_username
PLATFORM_PASSWORD=your_password
```

## 🎯 Platform Integration Guide

### Step 1: Generate Template
```bash
python tools/generate_platform_template.py --name "myplatform" --url "https://myplatform.com/login"
```

### Step 2: Configure Selectors
Edit `config/myplatform_config.json` with the correct selectors for your platform.

### Step 3: Test Integration
```bash
python examples/myplatform_example.py
```

## 📊 Advanced Features

### Custom Stealth Configuration
```python
from src.stealth.base_stealth_automation import BaseStealthAutomation

class CustomPlatform(BaseStealthAutomation):
    def login(self, username, password):
        # Custom login logic
        pass
    
    def is_logged_in(self):
        # Custom verification
        pass
```

### Telegram Channel Monitoring
```python
from src.telegram_setup import TelegramSetup

setup = TelegramSetup()
await setup.create_session()
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Test specific platform
pytest tests/test_binance_stealth.py -v
```

## 📝 Troubleshooting

### Common Issues

1. **Chrome Driver Issues**
   ```bash
   # Update ChromeDriver
   pip install --upgrade webdriver-manager
   ```

2. **Telegram Session Issues**
   ```bash
   # Recreate session
   python src/telegram_setup.py
   ```

3. **Selector Issues**
   ```bash
   # Rediscover selectors
   python tools/selector_discovery.py --url "https://platform.com/login"
   ```

## 🔄 Migration Guide

To move this to another project:

1. **Copy the entire directory** to your new project
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Run setup**: `python src/telegram_setup.py` (if using Telegram)
4. **Generate platform**: `python tools/generate_platform_template.py --name platform --url url`

## 📈 Performance Tips

- Use headless mode for production: `headless=True`
- Implement proper error handling
- Use session persistence for faster logins
- Monitor resource usage with logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your platform integration
4. Submit a pull request

## 📄 License

MIT License - Feel free to use in your projects!

## 🆘 Support

- Check the `docs/` folder for platform-specific guides
- Review `examples/` for usage patterns
- Test with `tests/` before production use
