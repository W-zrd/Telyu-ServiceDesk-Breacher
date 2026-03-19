import requests
import json
from pathlib import Path

class TelUAuth:
    def __init__(self, config_file='config.json'):
        self.config_file = Path(config_file)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        })
        self.token_data = None
        self.load_config()
    
    def load_config(self):
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.token_data = json.load(f)
                if 'cookies' in self.token_data:
                    self.session.cookies.update(self.token_data['cookies'])
                if 'headers' in self.token_data:
                    self.session.headers.update(self.token_data['headers'])
    
    def save_config(self):
        if self.token_data:
            with open(self.config_file, 'w') as f:
                json.dump(self.token_data, f, indent=2)
    
    def is_authenticated(self):
        if not self.token_data:
            return False
        
        if 'access_token' not in self.token_data:
            return False
        
        if 'expires_estimate' in self.token_data:
            from datetime import datetime
            try:
                expiry = datetime.fromisoformat(self.token_data['expires_estimate'])
                if datetime.now() > expiry:
                    print("⚠️  Session expired - please re-login")
                    return False
            except:
                pass
        
        return True
    
    def get_headers(self):
        headers = dict(self.session.headers)
        
        if self.token_data and 'access_token' in self.token_data:
            token = self.token_data['access_token']
            headers['Authorization'] = f"Bearer {token}"
        
        return headers
