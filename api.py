import requests
from auth import TelUAuth

class TelUServiceDesk:
    BASE_URL = "https://service-satu.telkomuniversity.ac.id/servicedesk"
    
    def __init__(self, auth: TelUAuth):
        self.auth = auth
        self.session = requests.Session()
        
    def _request(self, method, url, **kwargs):
        headers = self.auth.get_headers()
        
        if 'headers' in kwargs:
            headers.update(kwargs.pop('headers'))
        
        headers['Accept'] = 'application/json'
        
        response = self.session.request(
            method, url, headers=headers, **kwargs
        )
        response.raise_for_status()
        return response.json()
    
    def get_my_tickets(self, username):
        url = f"{self.BASE_URL}/558d90eacf725ed8c451a4c824df6364/0/{username}/"
        return self._request('GET', url)
    
    def get_closed_tickets(self, username, page=1):
        url = f"{self.BASE_URL}/f2e3d7e81dc9acf98d615ac257af7805/{username}/5/1/0/0/0/0/0/0/0/0/0/10/?page={page}"
        return self._request('GET', url)
