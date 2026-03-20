import requests
from .auth import TelUAuth

class AuthenticationError(Exception):
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
                raise
            except Exception:
                continue
        
        all_tickets.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return all_tickets
    
    def get_ticket_owner(self, ticket_id):
        url = f"{self.BASE_URL}/e5161778a026afc58c32ecaac665080d/{ticket_id}"
        data = self._request('GET', url)
        
        if isinstance(data, list):
            for entry in data:
                if entry.get('type_id') == 1:
                    return entry.get('created_by')
        
        raise ValueError(f"Could not find owner for ticket #{ticket_id}")
    
    def get_ticket_detail(self, ticket_id):
        username = self.get_ticket_owner(ticket_id)
        
        for status_code in [1, 2, 3, 4, 5, 6]:
            try:
                url = f"{self.BASE_URL}/f2e3d7e81dc9acf98d615ac257af7805/{username}/{status_code}/1/{ticket_id}/0/0/0/0/0/0/0/0/"
                data = self._request('GET', url)
                
                if 'data' in data and data['data']:
                    return data['data']
            except Exception:
                continue
        
        raise ValueError(f"Could not retrieve ticket #{ticket_id} for user {username}")
    
    def get_ticket_comments(self, ticket_id):
        url = f"{self.BASE_URL}/84bb4e380f70e9a912fb06fe686593f2/{ticket_id}/1/0/0/0"
        try:
            data = self._request('GET', url)
            return data if data else []
        except Exception:
            return []
    
    def create_ticket(self, username, description, user_id=None, service_detail_id=1213):
        url = f"{self.BASE_URL}/67fe01881afdcb8956f2dbf67b4b7596"
        if not description.strip().startswith('<p>'):
            description = f"<p>{description}</p>"
        
        data = {
            'service_detail_id': str(service_detail_id),
            'description': description,
            'requester': username,
            'username': username,
            'reporter': username,
            'created_by': username,
            'user_id': str(user_id) if user_id else '',
            'media': '0'
        }

        response = self.session.post(
            url,
            headers=self.auth.get_headers(),
            data=data
        )

        if response.status_code in [401, 403]:
            raise AuthenticationError(
                "Authentication failed - your bearer token has expired or is invalid. "
                "Please run: ./cli.py login"
            )
        
        response.raise_for_status()
        return response.json()
