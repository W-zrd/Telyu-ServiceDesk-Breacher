# Tel-U Service Desk Breacher

If you ever tired of being student, feeling burnout, lack of motivations, or depressed during study, wouldn't it be better if you take a revenge to have some fun, or shall we make PuTI a little bit busy tonight?

![](/img/cover.jpeg)

## Overview

A tool to satisfy your frustation that can be used for viewing ticket belonging to another users or creating a new ticket pretending as another users. It's not just a ticket, sometimes user add sensitive data or attachments in it, that's why it might satisfy your frustation 😈. Only works on users who have sent a ticket to the PuTI service desk. ***Under development, tested on Linux***.

**Key Features:**
- Automated SSO authentication (Chrome/Firefox/Edge)
- Session persistence in `config.json`
- Breach ticket list and its detail from another user
- Breach attachments from another user's ticket
- Send reply to hijack another user's ticket which didn't belong to you (*todo*)
- Create a new ticket by pretending to be created by some user (*todo*)

![](/img/overview.png)

## Requirements

### System Requirements
- Python 3.7+
- Chrome, Firefox, or Edge browser
- Linux or Windows (Tested on Linux)

**Required packages:**
- `click` - CLI framework
- `requests` - HTTP client
- `colorama` - Colored terminal output
- `selenium` - Browser automation
- `webdriver-manager` - Automatic driver management

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

### 1. Login (First Time)

Run the login first:
```bash
./cli.py login
```

**What happens:**
1. Browser opens automatically
2. Navigate to SATU SSO page
3. **You** complete the login:
   - Enter Tel-U email
   - Enter password
   - Complete Microsoft OTP
   - Wait for dashboard to load
4. Script automatically extracts bearer token
5. Browser closes
6. Session saved to `config.json`

**Browser Selection (optional):**
```bash
./cli.py login --browser chrome # default
./cli.py login --browser firefox
./cli.py login --browser auto
```

### 2. View All Tickets

The simplest way to use the tool is fetch ALL tickets for a user:

```bash
./cli.py tickets --username {sso_username}
```

**What it does:**
- Fetches all ticket list from a given username
- Sorts by creation time (newest first)
- Shows status label for each ticket

**Examples:**
```bash
./cli.py tickets --username king.wzrd
./cli.py tickets --username king.wzrd --format detail
./cli.py tickets --username king.wzrd --format json
```

### 3. Filter by Specific Status

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

## Troubleshooting

### "Not authenticated"
Run login first:
```bash
./cli.py login
```

### "Session expired"
Tokens expire after ~24 hours. Re-authenticate:
```bash
./cli.py login
```

### "Selenium not installed"
```bash
pip3 install selenium webdriver-manager
```

## Usage Patterns

### Quick User Audit
Get all tickets for a user to see their full history:
```bash
./cli.py tickets --username king.wzrd
```

### Check Active Work
Filter only in-progress tickets:
```bash
./cli.py tickets --username king.wzrd --status in-progress
```

### Export for Analysis
Get all tickets in JSON format:
```bash
./cli.py tickets --username king.wzrd --format json > king_wzrd_tickets.json
```

### Detailed Investigation
View full details of all tickets:
```bash
./cli.py tickets --username king.wzrd --format detail
```

## Project Structure

```
Telyu-CLI/
├── cli.py                    # CLI entry point
├── telyu_cli/                # Source code package
│   ├── __init__.py
│   ├── api.py                # Service Desk API wrapper
│   ├── auth.py               # Authentication & token management
│   ├── formatter.py          # Output formatting utilities
│   └── browser_login.py      # Automated browser login
├── docs/                     # Documentation
│   └── CHANGELOG.md
├── img/                      # Images
│   ├── cover.jpeg
│   └── overview.png
├── config.json               # Session data (created after login)
├── config.json.example       # Example configuration
├── requirements.txt          # Python dependencies
├── setup.sh                  # Quick setup script
├── LICENSE
├── .gitignore
└── README.md                 # This file
```