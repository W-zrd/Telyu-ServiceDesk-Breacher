from colorama import Fore, Style

def format_ticket_summary(ticket, comments=None):
    lines = []
    
    lines.append(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    lines.append(f"{Fore.YELLOW}Ticket #{ticket.get('id', 'N/A')}{Style.RESET_ALL}")
    lines.append(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    
    lines.append(f"\n{Fore.GREEN}📋 Basic Info:{Style.RESET_ALL}")
    
    status_display = ticket.get('name_status') or 'N/A'
    if 'status_name' in ticket:
        status_display = f"{status_display} ({ticket['status_name']})"
    lines.append(f"  Status       : {status_display}")
    
    lines.append(f"  Priority     : {ticket.get('priority') or 'N/A'}")
    lines.append(f"  Classification: {ticket.get('classification') or 'N/A'}")
    lines.append(f"  Purpose      : {ticket.get('purpose') or 'N/A'}")
    lines.append(f"  Service      : {ticket.get('service_name') or 'N/A'} → {ticket.get('sub_service_name') or 'N/A'}")
    
    lines.append(f"\n{Fore.GREEN}👤 User Info:{Style.RESET_ALL}")
    lines.append(f"  Name         : {ticket.get('name') or 'N/A'}")
    lines.append(f"  Username     : {ticket.get('username_user') or 'N/A'}")
    lines.append(f"  Tel-U ID     : {ticket.get('telu_id') or 'N/A'}")
    lines.append(f"  Email        : {ticket.get('email') or 'N/A'}")
    lines.append(f"  Phone        : {ticket.get('phone_number') or 'N/A'}")
    lines.append(f"  Other Number : {ticket.get('cell_number') or 'N/A'}")
    lines.append(f"  Position     : {ticket.get('position') or 'N/A'}")
    
    lines.append(f"\n{Fore.GREEN}📅 Dates:{Style.RESET_ALL}")
    lines.append(f"  Created      : {ticket.get('created_at') or 'N/A'}")
    lines.append(f"  Updated      : {ticket.get('updated_at') or 'N/A'}")
    if ticket.get('end_date'):
        lines.append(f"  Closed       : {ticket.get('end_date')}")
    lines.append(f"  SLA          : {ticket.get('sla') or 'N/A'} hours")
    
    lines.append(f"\n{Fore.GREEN}📝 Description:{Style.RESET_ALL}")
    desc = ticket.get('description_user') or ''
    if desc:
        desc = str(desc).replace('<p>', '').replace('</p>', '').replace('<br>', ' ').replace('\r\n', ' ')
    lines.append(f"  {desc or 'N/A'}")
    
    if ticket.get('url'):
        lines.append(f"\n{Fore.GREEN}📎 Attachment:{Style.RESET_ALL}")
        lines.append(f"  {ticket.get('url')}")
    
    if ticket.get('rating'):
        lines.append(f"\n{Fore.GREEN}⭐ Rating:{Style.RESET_ALL}")
        lines.append(f"  Score        : {ticket.get('rating')}/5")
        feedback = ticket.get('feedback_user')
        if feedback and str(feedback) != '-':
            lines.append(f"  Feedback     : {feedback}")
    
    tasks = ticket.get('tasks', [])
    if tasks:
        lines.append(f"\n{Fore.GREEN}📋 Tasks ({len(tasks)}):{Style.RESET_ALL}")
        for i, task in enumerate(tasks, 1):
            lines.append(f"  {i}. {task.get('task_description') or 'N/A'}")
            lines.append(f"     Created: {task.get('created_at') or 'N/A'} by {task.get('created_by') or 'N/A'}")
            assignees = task.get('assignees', [])
            if assignees:
                done_count = sum(1 for a in assignees if a.get('is_done'))
                lines.append(f"     Assignees: {len(assignees)} ({done_count} done)")
    
    keywords = ticket.get('keywords', [])
    if keywords:
        kw_list = [kw.get('keyword_name', '') for kw in keywords if kw.get('keyword_name')]
        if kw_list:
            lines.append(f"\n{Fore.GREEN}🏷️  Keywords:{Style.RESET_ALL}")
            lines.append(f"  {', '.join(kw_list)}")
    
    assignees = ticket.get('assignees', [])
    if assignees:
        lines.append(f"\n{Fore.GREEN}👥 Assignees:{Style.RESET_ALL}")
        usernames = [a.get('username_assignee') or 'N/A' for a in assignees]
        lines.append(f"  {', '.join(usernames)}")
    
    if comments:
        if isinstance(comments, dict) and 'data' in comments:
            comments_list = comments['data']
        elif isinstance(comments, list):
            comments_list = comments
        else:
            comments_list = []
        
        if comments_list:
            lines.append(f"\n{Fore.GREEN}💬 Comments ({len(comments_list)}):{Style.RESET_ALL}")
            for i, comment in enumerate(comments_list, 1):
                username = comment.get('username') or comment.get('created_by') or 'Unknown'
                created_at = comment.get('created_at') or 'N/A'
                comment_text = comment.get('messages') or comment.get('message') or comment.get('comment') or comment.get('description') or ''
                attachment_url = comment.get('url') or ''
                
                if comment_text:
                    comment_text = str(comment_text).replace('<p>', '').replace('</p>', '\n     ').replace('<br>', '\n     ').replace('\r\n', '\n     ').strip()
                
                lines.append(f"  {i}. {Fore.CYAN}{username}{Style.RESET_ALL} - {created_at}")
                if comment_text:
                    lines.append(f"     {comment_text}")
                if attachment_url:
                    lines.append(f"     📎 {attachment_url}")
    
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
        
        status_display = ticket.get('name_status') or 'N/A'
        if 'status_name' in ticket:
            status_label = ticket['status_name'].upper()
            status_display = f"[{status_label}] {status_display}"
        
        priority = ticket.get('priority') or 'N/A'
        purpose = ticket.get('purpose') or 'N/A'
        created = ticket.get('created_at') or 'N/A'
        
        desc = ticket.get('description_user') or ''
        if desc:
            desc = str(desc).replace('<p>', '').replace('</p>', '').replace('<br>', ' ').replace('\r\n', ' ')
        else:
            desc = 'N/A'
        
        lines.append(f"{Fore.YELLOW}{id_str:<10}{Style.RESET_ALL} {Fore.CYAN}{status_display:<30}{Style.RESET_ALL} {priority:<10}")
        lines.append(f"           {created}")
        lines.append(f"           {desc}")
        lines.append("")
    
    return '\n'.join(lines)

def format_pagination_info(data):
    if not isinstance(data, dict):
        return ""
    
    current = data.get('current_page', 1)
    last = data.get('last_page', 1)
    total = data.get('total', 0)
    
    return f"\n{Fore.CYAN}Page {current} of {last} | Total: {total} records{Style.RESET_ALL}"
