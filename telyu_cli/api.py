import requests
from .auth import TelUAuth

class AuthenticationError(Exception):
    """Raised when authentication fails or token is expired"""
    pass

class TelUServiceDesk:
    BASE_URL = "https://service-satu.telkomuniversity.ac.id/servicedesk"
    
    STATUS_CODES = {
        'new': 1,
        'assigned': 2,
        'in-progress': 3,
        'resolve': 4,
        'closed': 5,
        'on-hold': 6,
        'confirmation': 8
    }
    
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
        
        # Check for authentication errors
        if response.status_code in [401, 403]:
            raise AuthenticationError(
                "Authentication failed - your bearer token has expired or is invalid. "
                "Please run: ./cli.py login"
            )
        
        response.raise_for_status()
        return response.json()
    
    def get_tickets(self, username, status_code, page=1):
        url = f"{self.BASE_URL}/f2e3d7e81dc9acf98d615ac257af7805/{username}/{status_code}/1/0/0/0/0/0/0/0/0/0/10/?page={page}"
        return self._request('GET', url)
    
    def get_all_tickets(self, username):
        all_tickets = []
        
        for status_name, status_code in self.STATUS_CODES.items():
            try:
                data = self.get_tickets(username, status_code, page=1)
                
                if 'data' in data and data['data']:
                    tickets = data['data']
                    for ticket in tickets:
                        ticket['status_name'] = status_name
                    all_tickets.extend(tickets)
                    
                    total_pages = data.get('last_page', 1)
                    
                    for page in range(2, total_pages + 1):
                        data = self.get_tickets(username, status_code, page)
                        if 'data' in data and data['data']:
                            tickets = data['data']
                            for ticket in tickets:
                                ticket['status_name'] = status_name
                            all_tickets.extend(tickets)
            
            except AuthenticationError:
                # Re-raise authentication errors immediately
                raise
            except Exception:
                # Silently skip other errors (e.g., network issues for specific status codes)
                continue
        
        all_tickets.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return all_tickets
