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

### Python Dependencies
```bash
pip3 install -r requirements.txt
```

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

Run the automated login:
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

**Browser Selection:**
```bash
./cli.py login --browser chrome
./cli.py login --browser firefox
./cli.py login --browser auto # Default, the same as using ./cli.py login
```

### 2. Check Authentication Status

```bash
./cli.py status
```

Shows whether you're authenticated, token info, and expiry time.

### 3. View My Tickets

Retrieve tickets from "My Tickets" endpoint:

```bash
./cli.py my-tickets --username {sso_username}
```

**Options:**
- `--username`: Tel-U SSO username to query (required)
- `--format`: Output format (`pretty` or `json`)

**Examples:**
```bash
./cli.py my-tickets --username king.wzrd
./cli.py my-tickets --username king.wzrd --format json
```

### 4. View Closed Tickets

Retrieve closed tickets with full details:

```bash
./cli.py closed-tickets --username king.wzrd
```

**Options:**
- `--username`: Tel-U username to query (required)
- `--page`: Page number (default: 1)
- `--format`: Output format (`list`, `detail`, or `json`)

**Examples:**
```bash
./cli.py closed-tickets --username king.wzrd
./cli.py closed-tickets --username king.wzrd --format detail
./cli.py closed-tickets --username king.wzrd --page 2
./cli.py closed-tickets --username king.wzrd --format json
```

**Output Formats:**
- `list`: Summary view with ticket IDs, status, and short description
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

### List Format

```

================================================================================
Total: 2 ticket(s)
================================================================================

#24340   Close        Medium     Information    
         2025-11-04 23:05:47
         Dear IT Service Desk PuTI, saya memerlukan bantuan untuk reset password SSO ...

#24043   Close        Medium     Information    
         2025-10-14 11:20:30
         Halo, butuh bantuan untuk setup Exam browser agar bisa mengerjakan UAS Alpro ...

Page 1 of 1 | Total: 2 records
```

### Detail Format
```
> ./cli.py closed-tickets --format detail
================================================================================
Ticket #24340
================================================================================

📋 Basic Info:
  Status       : Close
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
  2. [Extend] Permintaan reset password SSO oleh username victim_user
     Created: 2025-11-10 09:04:53 by admin_puti2
     Assignees: 2 (2 done)
  3. Reset password sudah berhasil dilakukan oleh victim_user.
     Created: 2025-11-14 11:11:54 by admin_puti3
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
./cli.py status
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

### "No browser found"
Install one of the supported browsers:
- Chrome: https://www.google.com/chrome/
- Firefox: https://www.mozilla.org/firefox/
- Edge: https://www.microsoft.com/edge

## Project Structure

```
telu-cli-v2/
├── cli.py              # Main CLI interface
├── auth.py             # Authentication & token management
├── api.py              # Service Desk API wrapper
├── formatter.py        # Output formatting utilities
├── browser_login.py    # Automated browser login
├── requirements.txt    # Python dependencies
├── setup.sh            # Quick setup script
├── config.json         # Session data (created after login)
└── README.md           # This file
```
