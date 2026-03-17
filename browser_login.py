#!/usr/bin/env python3

import json
import time
from pathlib import Path
from datetime import datetime, timedelta

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    from selenium.webdriver.edge.options import Options as EdgeOptions
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

try:
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.firefox import GeckoDriverManager
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.firefox.service import Service as FirefoxService
    from selenium.webdriver.edge.service import Service as EdgeService
    WEBDRIVER_MANAGER_AVAILABLE = True
except ImportError:
    WEBDRIVER_MANAGER_AVAILABLE = False

def find_browser_executable(browser_name):
    import shutil
    import platform
    
    system = platform.system().lower()
    
    executables = {
        'chrome': [
            'google-chrome', 'chrome', 'chromium', 'chromium-browser',
            'Google Chrome', 'Chrome'
        ],
        'firefox': [
            'firefox', 'firefox-esr', 'Firefox'
        ],
        'edge': [
            'microsoft-edge', 'msedge', 'edge'
        ]
    }
    
    if system == 'windows':
        import os
        common_paths = {
            'chrome': [
                r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
            ],
            'firefox': [
                r'C:\Program Files\Mozilla Firefox\firefox.exe',
                r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe',
            ],
            'edge': [
                r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
            ]
        }
        
        if browser_name in common_paths:
            for path in common_paths[browser_name]:
                if os.path.exists(path):
                    return path
    
    if browser_name in executables:
        for exe_name in executables[browser_name]:
            exe_path = shutil.which(exe_name)
            if exe_path:
                return exe_path
    
    return None

def get_driver(browser='auto', headless=False):
    if browser == 'auto':
        for browser_name in ['chrome', 'firefox', 'edge']:
            exe_path = find_browser_executable(browser_name)
            if exe_path:
                print(f"  ✓ Found {browser_name.title()}: {exe_path}")
                browser = browser_name
                break
        else:
            raise RuntimeError(
                "❌ No browser found!\n"
                "Please install Chrome, Firefox, or Edge"
            )
    
    print(f"  🌐 Using: {browser.title()}")
    
    if WEBDRIVER_MANAGER_AVAILABLE:
        try:
            if browser == 'chrome':
                options = ChromeOptions()
                if headless:
                    options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                
                service = ChromeService(ChromeDriverManager().install())
                return webdriver.Chrome(service=service, options=options)
                
            elif browser == 'firefox':
                options = FirefoxOptions()
                if headless:
                    options.add_argument('--headless')
                
                service = FirefoxService(GeckoDriverManager().install())
                return webdriver.Firefox(service=service, options=options)
                
            elif browser == 'edge':
                options = EdgeOptions()
                if headless:
                    options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                
                service = EdgeService(EdgeChromiumDriverManager().install())
                return webdriver.Edge(service=service, options=options)
                
        except Exception as e:
            print(f"  ⚠️  webdriver-manager failed: {e}")
            print(f"  Trying manual method...")
    
    exe_path = find_browser_executable(browser)
    if not exe_path:
        raise RuntimeError(f"❌ {browser.title()} not found!")
    
    if browser == 'chrome':
        options = ChromeOptions()
        options.binary_location = exe_path
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        return webdriver.Chrome(options=options)
        
    elif browser == 'firefox':
        options = FirefoxOptions()
        options.binary_location = exe_path
        if headless:
            options.add_argument('--headless')
        return webdriver.Firefox(options=options)
        
    elif browser == 'edge':
        options = EdgeOptions()
        options.binary_location = exe_path
        if headless:
            options.add_argument('--headless')
        return webdriver.Edge(options=options)
    
    raise ValueError(f"Unknown browser: {browser}")

def wait_for_login(driver, timeout=300):
    print("\n" + "="*60)
    print("🌐 Browser opened - Complete the login:")
    print("="*60)
    print("  1. Login with Microsoft SSO")
    print("  2. Enter email, password, and OTP code")
    print("  3. Wait for SATU dashboard to load")
    print("="*60)
    print("\n⏳ Waiting for SATU dashboard... (timeout: 5 minutes)")
    
    start_time = time.time()
    last_url = ""
    
    while time.time() - start_time < timeout:
        current_url = driver.current_url
        
        if current_url != last_url:
            print(f"\n  📍 {current_url[:80]}...")
            last_url = current_url
        
        if 'satu.telkomuniversity.ac.id/home' in current_url:
            print("\n✅ SATU dashboard detected!")
            time.sleep(3)
            return True
        
        elapsed = int(time.time() - start_time)
        if elapsed % 10 == 0 and elapsed > 0:
            print(f"  ⏳ {elapsed}s / {timeout}s", end='\r')
        
        time.sleep(1)
    
    print("\n❌ Timeout - login not completed")
    return False

def extract_bearer_token(driver):
    print("\n🔑 Extracting bearer token from localStorage...")
    
    try:
        current_url = driver.current_url
        print(f"  Current page: {current_url}")
        
        if 'satu.telkomuniversity.ac.id' not in current_url:
            print("  ⚠️  Not on SATU page, navigating...")
            driver.get('https://satu.telkomuniversity.ac.id/home')
            time.sleep(3)
        
        print("  Checking localStorage...")
        local_storage = driver.execute_script("""
            const storage = {};
            for (let i = 0; i < localStorage.length; i++) {
                const key = localStorage.key(i);
                const value = localStorage.getItem(key);
                storage[key] = value;
            }
            return storage;
        """)
        
        if not local_storage:
            print("  ❌ localStorage is empty!")
            return None
        
        print(f"  ✓ Found {len(local_storage)} items in localStorage")
        
        bearer_token = None
        token_key = None
        
        for key, value in local_storage.items():
            print(f"    - {key}: {str(value)[:60]}...")
            
            if not value:
                continue
            
            if key.lower() in ['access_token', 'accesstoken', 'token', 'bearer', 'authtoken']:
                if isinstance(value, str) and len(value) > 20:
                    bearer_token = value
                    token_key = key
                    print(f"  ✅ Found token in key: {key}")
                    break
            
            if isinstance(value, str) and (value.startswith('{') or value.startswith('[')):
                try:
                    parsed = json.loads(value)
                    if isinstance(parsed, dict):
                        for field in ['access_token', 'accessToken', 'token', 'bearerToken', 'jwt', 'authToken']:
                            if field in parsed and parsed[field]:
                                bearer_token = parsed[field]
                                token_key = f"{key}.{field}"
                                print(f"  ✅ Found token in {key}.{field}")
                                break
                        if bearer_token:
                            break
                except:
                    pass
            
            if isinstance(value, str):
                parts = value.split('.')
                if len(parts) == 3 and all(len(p) > 10 for p in parts):
                    bearer_token = value
                    token_key = key
                    print(f"  ✅ Found JWT-like token in: {key}")
                    break
        
        if bearer_token:
            print(f"\n  🎯 Bearer token found!")
            print(f"     Source: {token_key}")
            print(f"     Preview: {bearer_token[:40]}...{bearer_token[-20:]}")
            return bearer_token
        else:
            print("\n  ❌ No bearer token found in localStorage")
            print("  📋 Available localStorage keys:")
            for key in local_storage.keys():
                print(f"     - {key}")
            return None
            
    except Exception as e:
        print(f"  ❌ Error extracting token: {e}")
        import traceback
        traceback.print_exc()
        return None

def extract_cookies(driver):
    print("\n🍪 Extracting cookies...")
    
    all_cookies = {}
    
    try:
        for cookie in driver.get_cookies():
            all_cookies[cookie['name']] = cookie['value']
        
        print(f"  ✓ Extracted {len(all_cookies)} cookies")
        
    except Exception as e:
        print(f"  ⚠️  Error extracting cookies: {e}")
    
    return all_cookies

def save_session(bearer_token, cookies):
    if not bearer_token:
        print("\n❌ Cannot save session - no bearer token found")
        return None
    
    config = {
        "access_token": bearer_token,
        "headers": {
            "Authorization": f"Bearer {bearer_token}"
        },
        "cookies": cookies,
        "extracted_at": datetime.now().isoformat(),
        "expires_estimate": (datetime.now() + timedelta(hours=24)).isoformat(),
        "method": "automated_browser"
    }
    
    config_file = Path('config.json')
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n✅ Session saved to: {config_file.absolute()}")
    print(f"📅 Estimated expiry: {config['expires_estimate']}")
    
    print(f"\n📊 Session Summary:")
    print(f"   Bearer token: ✅ Yes ({len(bearer_token)} chars)")
    print(f"   Cookies: {len(cookies)}")
    print(f"   Preview: {bearer_token[:30]}...{bearer_token[-15:]}")
    
    return config_file

def automated_login(browser='auto', headless=False):
    if not SELENIUM_AVAILABLE:
        print("❌ Selenium not installed!")
        print("Install: pip3 install selenium webdriver-manager")
        return False
    
    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║        Automated Browser Login - Tel-U Service Desk       ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    driver = None
    
    try:
        print(f"\n🚀 Starting browser...")
        driver = get_driver(browser, headless)
        
        login_url = 'https://satu.telkomuniversity.ac.id/'
        print(f"🌐 Navigating to: {login_url}")
        driver.get(login_url)
        
        if not wait_for_login(driver):
            print("\n⚠️  Login not completed")
            return False
        
        bearer_token = extract_bearer_token(driver)
        
        if not bearer_token:
            print("\n❌ Failed to extract bearer token!")
            print("\nPlease check:")
            print("  1. You completed login successfully")
            print("  2. You're on SATU dashboard (https://satu.telkomuniversity.ac.id/home)")
            print("  3. The page fully loaded")
            return False
        
        cookies = extract_cookies(driver)
        
        if save_session(bearer_token, cookies):
            print("\n" + "="*60)
            print("✅ SUCCESS! Token extracted and saved")
            print("="*60)
            print("\nYou can now use:")
            print("  ./cli.py status")
            print("  ./cli.py my-tickets --username {your_username}")
            print("  ./cli.py closed-tickets --username {your_username}")
            print("="*60)
            return True
        else:
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        if driver:
            print("\n🔒 Closing browser...")
            driver.quit()

def check_requirements():
    issues = []
    warnings = []
    
    if not SELENIUM_AVAILABLE:
        issues.append("selenium")
    
    if not WEBDRIVER_MANAGER_AVAILABLE:
        warnings.append("webdriver-manager (recommended)")
    
    if issues:
        print("❌ Missing required packages:")
        for issue in issues:
            print(f"  - {issue}")
        print("\nInstall: pip3 install selenium webdriver-manager")
        return False
    
    if warnings:
        print("⚠️  Recommended:")
        for warning in warnings:
            print(f"  - {warning}")
        print()
    
    return True

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Automated browser login for Tel-U')
    parser.add_argument('--browser', choices=['auto', 'chrome', 'firefox', 'edge'], default='auto')
    parser.add_argument('--headless', action='store_true')
    
    args = parser.parse_args()
    
    if check_requirements():
        automated_login(browser=args.browser, headless=args.headless)
