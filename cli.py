#!/usr/bin/env python3

import click
import json
from colorama import Fore, Style, init as colorama_init
from telyu_cli import TelUAuth, TelUServiceDesk, format_ticket_summary, format_ticket_list, format_pagination_info
from telyu_cli.api import AuthenticationError

colorama_init(autoreset=True)

STATUS_CODES = {
    'new': 1,
    'assigned': 2,
    'in-progress': 3,
    'resolve': 4,
    'closed': 5,
    'on-hold': 6,
    'confirmation': 8
}

@click.group()
def cli():
    pass

@cli.command()
@click.option('--browser', type=click.Choice(['auto', 'chrome', 'firefox', 'edge']), default='auto')
@click.option('--manual', is_flag=True, help='Enter bearer token manually')
def login(browser, manual):
    if manual:
        click.echo(f"{Fore.CYAN}🔑 Manual bearer token entry{Style.RESET_ALL}")
        click.echo()
        click.echo(f"{Fore.YELLOW}Note: Paste your bearer token below{Style.RESET_ALL}")
        click.echo(f"{Fore.YELLOW}The token should be a long string from localStorage or network requests{Style.RESET_ALL}")
        click.echo()
        
        bearer_token = click.prompt('Bearer token', type=str, hide_input=True)
        
        if not bearer_token or len(bearer_token) < 20:
            click.echo(f"{Fore.RED}✗ Invalid token (too short){Style.RESET_ALL}")
            raise click.Abort()
        
        auth = TelUAuth()
        
        try:
            auth.set_manual_token(bearer_token)
            click.echo()
            click.echo(f"{Fore.GREEN}✅ Token saved successfully!{Style.RESET_ALL}")
            click.echo(f"  {Fore.GREEN}Method:{Style.RESET_ALL} Manual entry")
            click.echo(f"  {Fore.GREEN}Saved to:{Style.RESET_ALL} config.json")
            click.echo()
            click.echo(f"Run: {Fore.CYAN}./cli.py tickets --username {{username}}{Style.RESET_ALL} to test")
        except Exception as e:
            click.echo(f"{Fore.RED}✗ Error saving token: {e}{Style.RESET_ALL}")
            raise click.Abort()
    else:
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
        
        try:
            import subprocess
            import sys
            
            result = subprocess.run(
                [sys.executable, 'telyu_cli/browser_login.py', '--browser', browser],
                cwd='.'
            )
            
            if result.returncode == 0:
                click.echo()
                click.echo(f"{Fore.GREEN}✅ Login successful!{Style.RESET_ALL}")
                click.echo(f"\nRun: {Fore.CYAN}./cli.py tickets --username {{username}}{Style.RESET_ALL} to get started")
            else:
                click.echo()
                click.echo(f"{Fore.RED}✗ Login failed{Style.RESET_ALL}")
                
        except FileNotFoundError:
            click.echo(f"{Fore.RED}✗ telyu_cli/browser_login.py not found{Style.RESET_ALL}")
        except Exception as e:
            click.echo(f"{Fore.RED}✗ Error: {e}{Style.RESET_ALL}")

@cli.command()
@click.option('--username', prompt='Enter username', help='Tel-U username')
@click.option('--status', 'status_name', 
              type=click.Choice(['new', 'assigned', 'in-progress', 'resolve', 'closed', 'on-hold', 'confirmation']), 
              default=None,
              help='Ticket status to filter (default: all statuses)')
@click.option('--page', default=1, help='Page number (only used with --status)')
@click.option('--format', 'output_format', 
              type=click.Choice(['json', 'list', 'detail']), 
              default='list',
              help='Output format')
def tickets(username, status_name, page, output_format):
    auth = TelUAuth()
    if not auth.is_authenticated():
        click.echo(f"{Fore.RED}✗ Not authenticated. Run: ./cli.py login{Style.RESET_ALL}")
        raise click.Abort()
    
    api = TelUServiceDesk(auth)
    
    if status_name:
        status_code = STATUS_CODES[status_name]
        click.echo(f"{Fore.CYAN}🎫 Fetching {status_name} tickets for: {username} (page {page})...{Style.RESET_ALL}")
        
        try:
            data = api.get_tickets(username, status_code, page)
            
            if output_format == 'json':
                click.echo(json.dumps(data, indent=2))
            elif output_format == 'list':
                if 'data' in data:
                    tickets = data['data']
                    for ticket in tickets:
                        ticket['status_name'] = status_name
                    click.echo(format_ticket_list(tickets))
                    click.echo(format_pagination_info(data))
                else:
                    click.echo(f"{Fore.YELLOW}No tickets found.{Style.RESET_ALL}")
            elif output_format == 'detail':
                if 'data' in data:
                    tickets = data['data']
                    for ticket in tickets:
                        ticket['status_name'] = status_name
                        click.echo(format_ticket_summary(ticket))
                    click.echo(format_pagination_info(data))
                else:
                    click.echo(f"{Fore.YELLOW}No tickets found.{Style.RESET_ALL}")
                
        except AuthenticationError as e:
            click.echo(f"{Fore.RED}✗ {e}{Style.RESET_ALL}")
            raise click.Abort()
        except Exception as e:
            click.echo(f"{Fore.RED}✗ Error: {e}{Style.RESET_ALL}")
    else:
        click.echo(f"{Fore.CYAN}🎫 Fetching all tickets for: {username}...{Style.RESET_ALL}")
        
        try:
            tickets = api.get_all_tickets(username)
            
            if output_format == 'json':
                click.echo(json.dumps(tickets, indent=2))
            elif output_format == 'list':
                if tickets:
                    click.echo(format_ticket_list(tickets))
                    click.echo(f"\n{Fore.CYAN}Total: {len(tickets)} tickets across all statuses{Style.RESET_ALL}")
                else:
                    click.echo(f"{Fore.YELLOW}No tickets found.{Style.RESET_ALL}")
            elif output_format == 'detail':
                if tickets:
                    for ticket in tickets:
                        click.echo(format_ticket_summary(ticket))
                    click.echo(f"\n{Fore.CYAN}Total: {len(tickets)} tickets across all statuses{Style.RESET_ALL}")
                else:
                    click.echo(f"{Fore.YELLOW}No tickets found.{Style.RESET_ALL}")
                
        except AuthenticationError as e:
            click.echo(f"{Fore.RED}✗ {e}{Style.RESET_ALL}")
            raise click.Abort()
        except Exception as e:
            click.echo(f"{Fore.RED}✗ Error: {e}{Style.RESET_ALL}")

@cli.command()
@click.option('--username', prompt='Target username', help='Username to create ticket as (e.g., king.wzrd)')
@click.option('--user-id', default=None, help='User ID (optional, e.g., 1302210127)')
@click.option('--description', prompt='Ticket description', help='Description of the issue/request')
@click.option('--service-id', default=1213, help='Service detail ID (default: 1213)')
def create_ticket(username, user_id, description, service_id):
    auth = TelUAuth()
    if not auth.is_authenticated():
        click.echo(f"{Fore.RED}✗ Not authenticated. Run: ./cli.py login{Style.RESET_ALL}")
        raise click.Abort()
    
    api = TelUServiceDesk(auth)
    
    click.echo()
    click.echo(f"{Fore.CYAN}📝 Ticket Preview:{Style.RESET_ALL}")
    click.echo(f"  {Fore.GREEN}Username:{Style.RESET_ALL} {username}")
    if user_id:
        click.echo(f"  {Fore.GREEN}User ID:{Style.RESET_ALL} {user_id}")
    click.echo(f"  {Fore.GREEN}Service ID:{Style.RESET_ALL} {service_id}")
    click.echo(f"  {Fore.GREEN}Description:{Style.RESET_ALL}")
    
    preview_desc = description if description.strip().startswith('<p>') else f"<p>{description}</p>"
    click.echo(f"    {preview_desc}")
    click.echo()
    
    click.echo(f"{Fore.YELLOW}⚠️  WARNING: This will create a REAL ticket in Service Desk!{Style.RESET_ALL}")
    if not click.confirm(f"{Fore.RED}Are you sure you want to create this ticket as that specified user?{Style.RESET_ALL}", default=False):
        click.echo(f"{Fore.YELLOW}✗ Cancelled{Style.RESET_ALL}")
        return
    
    try:
        click.echo()
        click.echo(f"{Fore.CYAN}📤 Creating ticket...{Style.RESET_ALL}")
        
        result = api.create_ticket(
            username=username,
            description=description,
            user_id=user_id,
            service_detail_id=service_id
        )
        
        click.echo()
        click.echo(f"{Fore.GREEN}✅ Ticket created successfully!{Style.RESET_ALL}")
        click.echo()
        click.echo(f"  {Fore.GREEN}Ticket ID:{Style.RESET_ALL} {result.get('id', 'N/A')}")
        click.echo(f"  {Fore.GREEN}Status:{Style.RESET_ALL} {result.get('status', 'N/A')}")
        click.echo(f"  {Fore.GREEN}Message:{Style.RESET_ALL} {result.get('message', 'N/A')}")
        click.echo()
        
    except AuthenticationError as e:
        click.echo(f"{Fore.RED}✗ {e}{Style.RESET_ALL}")
        raise click.Abort()
    except Exception as e:
        click.echo(f"{Fore.RED}✗ Error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        raise click.Abort()

if __name__ == '__main__':
    cli()
