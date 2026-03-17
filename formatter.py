from colorama import Fore, Style
from datetime import datetime

def format_ticket_summary(ticket):
    lines = []
    
    lines.append(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    lines.append(f"{Fore.YELLOW}Ticket #{ticket.get('id')}{Style.RESET_ALL}")
    lines.append(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    
    lines.append(f"\n{Fore.GREEN}📋 Basic Info:{Style.RESET_ALL}")
    lines.append(f"  Status       : {ticket.get('name_status', 'N/A')}")
    lines.append(f"  Priority     : {ticket.get('priority', 'N/A')}")
    lines.append(f"  Classification: {ticket.get('classification', 'N/A')}")
    lines.append(f"  Purpose      : {ticket.get('purpose', 'N/A')}")
    lines.append(f"  Service      : {ticket.get('service_name', 'N/A')} → {ticket.get('sub_service_name', 'N/A')}")
    
    lines.append(f"\n{Fore.GREEN}👤 User Info:{Style.RESET_ALL}")
    lines.append(f"  Name         : {ticket.get('name', 'N/A')}")
    lines.append(f"  Username     : {ticket.get('username_user', 'N/A')}")
    lines.append(f"  Tel-U ID     : {ticket.get('telu_id', 'N/A')}")
    lines.append(f"  Email        : {ticket.get('email', 'N/A')}")
    lines.append(f"  Phone        : {ticket.get('phone_number', 'N/A')}")
    lines.append(f"  Other Number : {ticket.get('cell_number', 'N/A')}")
    lines.append(f"  Position     : {ticket.get('position', 'N/A')}")
    
    lines.append(f"\n{Fore.GREEN}📅 Dates:{Style.RESET_ALL}")
    lines.append(f"  Created      : {ticket.get('created_at', 'N/A')}")
    lines.append(f"  Updated      : {ticket.get('updated_at', 'N/A')}")
    if ticket.get('end_date'):
        lines.append(f"  Closed       : {ticket.get('end_date')}")
    lines.append(f"  SLA          : {ticket.get('sla', 'N/A')} hours")
    
    lines.append(f"\n{Fore.GREEN}📝 Description:{Style.RESET_ALL}")
    desc = ticket.get('description_user', 'N/A')
    lines.append(f"  {desc}")
    
    if ticket.get('url'):
        lines.append(f"\n{Fore.GREEN}📎 Attachment:{Style.RESET_ALL}")
        lines.append(f"  {ticket.get('url')}")
    
    if ticket.get('rating'):
        lines.append(f"\n{Fore.GREEN}⭐ Rating:{Style.RESET_ALL}")
        lines.append(f"  Score        : {ticket.get('rating')}/5")
        if ticket.get('feedback_user') and ticket.get('feedback_user') != '-':
            lines.append(f"  Feedback     : {ticket.get('feedback_user')}")
    
    tasks = ticket.get('tasks', [])
    if tasks:
        lines.append(f"\n{Fore.GREEN}📋 Tasks ({len(tasks)}):{Style.RESET_ALL}")
        for i, task in enumerate(tasks, 1):
            lines.append(f"  {i}. {task.get('task_description', 'N/A')}")
            lines.append(f"     Created: {task.get('created_at', 'N/A')} by {task.get('created_by', 'N/A')}")
            assignees = task.get('assignees', [])
            if assignees:
                done_count = sum(1 for a in assignees if a.get('is_done'))
                lines.append(f"     Assignees: {len(assignees)} ({done_count} done)")
    
    keywords = ticket.get('keywords', [])
    if keywords:
        kw_list = [kw.get('keyword_name', '') for kw in keywords]
        lines.append(f"\n{Fore.GREEN}🏷️  Keywords:{Style.RESET_ALL}")
        lines.append(f"  {', '.join(kw_list)}")
    
    assignees = ticket.get('assignees', [])
    if assignees:
        lines.append(f"\n{Fore.GREEN}👥 Assignees:{Style.RESET_ALL}")
        usernames = [a.get('username_assignee', 'N/A') for a in assignees]
        lines.append(f"  {', '.join(usernames)}")
    
    return '\n'.join(lines)

def format_ticket_list(tickets):
    lines = []
    
    lines.append(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    lines.append(f"{Fore.YELLOW}Total: {len(tickets)} ticket(s){Style.RESET_ALL}")
    lines.append(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
    
    if not tickets:
        lines.append(f"{Fore.YELLOW}No tickets found.{Style.RESET_ALL}")
        return '\n'.join(lines)
    
    for ticket in tickets:
        id_str = f"#{ticket.get('id', 'N/A')}"
        status = ticket.get('name_status', 'N/A')
        priority = ticket.get('priority', 'N/A')
        purpose = ticket.get('purpose', 'N/A')
        created = ticket.get('created_at', 'N/A')
        
        desc = ticket.get('description_user', '')
        if desc:
            desc = desc.replace('<p>', '').replace('</p>', '').replace('<br>', ' ')
        
        lines.append(f"{Fore.YELLOW}{id_str:<8}{Style.RESET_ALL} {status:<12} {priority:<10} {purpose:<15}")
        lines.append(f"         {created}")
        lines.append(f"         {desc}")
        lines.append("")
    
    return '\n'.join(lines)

def format_pagination_info(data):
    if not isinstance(data, dict):
        return ""
    
    current = data.get('current_page', 1)
    last = data.get('last_page', 1)
    total = data.get('total', 0)
    
    return f"\n{Fore.CYAN}Page {current} of {last} | Total: {total} records{Style.RESET_ALL}"
