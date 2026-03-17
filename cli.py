#!/usr/bin/env python3

import click
import json
from colorama import Fore, Style, init as colorama_init
from auth import TelUAuth
from api import TelUServiceDesk
from formatter import format_ticket_summary, format_ticket_list, format_pagination_info

colorama_init(autoreset=True)

@click.group()
def cli():
    pass

@cli.command()
@click.option('--browser', type=click.Choice(['auto', 'chrome', 'firefox', 'edge']), default='auto')
def login(browser):
    click.echo(f"{Fore.CYAN}🚀 Automated browser login{Style.RESET_ALL}")
    click.echo()
    click.echo("This will:")
    if browser == 'auto':
        click.echo(f"  {Fore.GREEN}✓{Style.RESET_ALL} Auto-detect available browser")
    else:
        click.echo(f"  {Fore.GREEN}✓{Style.RESET_ALL} Use {browser.title()}")
    click.echo(f"  {Fore.GREEN}✓{Style.RESET_ALL} Open SATU login page")
    click.echo(f"  {Fore.YELLOW}⏸{Style.RESET_ALL}  Wait for you to complete SSO + OTP")
    click.echo(f"  {Fore.GREEN}✓{Style.RESET_ALL} Extract bearer token from SATU dashboard")
    click.echo(f"  {Fore.GREEN}✓{Style.RESET_ALL} Save to config.json")
    click.echo()
    
    if not click.confirm("Continue?", default=True):
        return
    
    try:
        import subprocess
        import sys
        
        result = subprocess.run(
            [sys.executable, 'browser_login.py', '--browser', browser],
            cwd='.'
        )
        
        if result.returncode == 0:
            click.echo()
            click.echo(f"{Fore.GREEN}✅ Login successful!{Style.RESET_ALL}")
            click.echo(f"\nRun: {Fore.CYAN}./cli.py status{Style.RESET_ALL} to verify")
        else:
            click.echo()
            click.echo(f"{Fore.RED}✗ Login failed{Style.RESET_ALL}")
            
    except FileNotFoundError:
        click.echo(f"{Fore.RED}✗ browser_login.py not found{Style.RESET_ALL}")
    except Exception as e:
        click.echo(f"{Fore.RED}✗ Error: {e}{Style.RESET_ALL}")

@cli.command()
def status():
    auth = TelUAuth()
    
    if not auth.token_data:
        click.echo(f"{Fore.RED}✗ Not authenticated{Style.RESET_ALL}")
        click.echo(f"Run: {Fore.CYAN}./cli.py login{Style.RESET_ALL}")
        return
    
    if 'access_token' not in auth.token_data:
        click.echo(f"{Fore.RED}✗ No bearer token found in config.json{Style.RESET_ALL}")
        click.echo(f"Run: {Fore.CYAN}./cli.py login{Style.RESET_ALL}")
        return
    
    if auth.is_authenticated():
        click.echo(f"{Fore.GREEN}✓ Authenticated{Style.RESET_ALL}")
        click.echo(f"\nToken info:")
        token = auth.token_data['access_token']
        click.echo(f"  Bearer token: {token[:30]}...{token[-15:]}")
        click.echo(f"  Length: {len(token)} chars")
        
        if 'extracted_at' in auth.token_data:
            click.echo(f"  Extracted: {auth.token_data['extracted_at']}")
        if 'expires_estimate' in auth.token_data:
            click.echo(f"  Expires: {auth.token_data['expires_estimate']}")
    else:
        click.echo(f"{Fore.RED}✗ Token expired{Style.RESET_ALL}")
        click.echo(f"Run: {Fore.CYAN}./cli.py login{Style.RESET_ALL}")

@cli.command('my-tickets')
@click.option('--username', prompt='Enter username', help='Tel-U username')
@click.option('--format', 'output_format', type=click.Choice(['json', 'pretty']), default='pretty')
def my_tickets(username, output_format):
    auth = TelUAuth()
    if not auth.is_authenticated():
        click.echo(f"{Fore.RED}✗ Not authenticated. Run: ./cli.py login{Style.RESET_ALL}")
        raise click.Abort()
    
    api = TelUServiceDesk(auth)
    click.echo(f"{Fore.CYAN}🎫 Fetching my tickets for: {username}...{Style.RESET_ALL}")
    
    try:
        data = api.get_my_tickets(username)
        
        if output_format == 'json':
            click.echo(json.dumps(data, indent=2))
        else:
            if isinstance(data, dict):
                if data.get('status') == 'success' and data.get('message') == 'No Data Found':
                    click.echo(f"\n{Fore.YELLOW}No tickets found for user: {username}{Style.RESET_ALL}")
                elif 'data' in data:
                    tickets = data['data']
                    click.echo(format_ticket_list(tickets))
                    click.echo(format_pagination_info(data))
                else:
                    click.echo(f"\n{Fore.YELLOW}Response: {json.dumps(data, indent=2)}{Style.RESET_ALL}")
            elif isinstance(data, list):
                click.echo(format_ticket_list(data))
            else:
                click.echo(f"\n{Fore.YELLOW}Unexpected response format{Style.RESET_ALL}")
            
    except Exception as e:
        click.echo(f"{Fore.RED}✗ Error: {e}{Style.RESET_ALL}")

@cli.command('closed-tickets')
@click.option('--username', prompt='Enter username', help='Tel-U username')
@click.option('--page', default=1, help='Page number')
@click.option('--format', 'output_format', type=click.Choice(['json', 'list', 'detail']), default='list')
def closed_tickets(username, page, output_format):
    auth = TelUAuth()
    if not auth.is_authenticated():
        click.echo(f"{Fore.RED}✗ Not authenticated. Run: ./cli.py login{Style.RESET_ALL}")
        raise click.Abort()
    
    api = TelUServiceDesk(auth)
    click.echo(f"{Fore.CYAN}✅ Fetching closed tickets for: {username} (page {page})...{Style.RESET_ALL}")
    
    try:
        data = api.get_closed_tickets(username, page)
        
        if output_format == 'json':
            click.echo(json.dumps(data, indent=2))
        elif output_format == 'list':
            if 'data' in data:
                tickets = data['data']
                click.echo(format_ticket_list(tickets))
                click.echo(format_pagination_info(data))
            else:
                click.echo(f"{Fore.YELLOW}No tickets found.{Style.RESET_ALL}")
        elif output_format == 'detail':
            if 'data' in data:
                tickets = data['data']
                for ticket in tickets:
                    click.echo(format_ticket_summary(ticket))
                click.echo(format_pagination_info(data))
            else:
                click.echo(f"{Fore.YELLOW}No tickets found.{Style.RESET_ALL}")
            
    except Exception as e:
        click.echo(f"{Fore.RED}✗ Error: {e}{Style.RESET_ALL}")

if __name__ == '__main__':
    cli()
