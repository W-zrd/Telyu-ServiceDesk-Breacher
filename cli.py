#!/usr/bin/env python3

import click
import json
from colorama import Fore, Style, init as colorama_init
from telyu_cli import TelUAuth, TelUServiceDesk, format_ticket_summary, format_ticket_list, format_pagination_info

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
                
        except Exception as e:
            click.echo(f"{Fore.RED}✗ Error: {e}{Style.RESET_ALL}")

if __name__ == '__main__':
    cli()
