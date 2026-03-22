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

**Available Options:**
- `--username`: Tel-U SSO username to query (required)
- `--status`: Ticket status filter (optional, fetches all if omitted)
- `--page`: Page number (only used with --status)
- `--format`: Output format (`list`, `detail`, or `json`)

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
--status {status_name}
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

## 3. Create New Ticket as Another User

The `create-ticket` command allows you to create a new service desk ticket as any specified user. 

```bash
./cli.py create-ticket
```

You'll be prompted for Target username and Ticket description

- `username`: Target SSO username. Specify which user the ticket will be created as
- `description`: The ticket description/message

## 4. Replying/Commenting to Someone's Ticket

The `comment` command allows you to send a comment or reply to an existing ticket as any specified user based on ticket ID. So the first thing you need to do for using this command is to find the ticket ID first. You can use `./cli.py tickets --username {sso_username}` to do so.

```bash
./cli.py comment
```

**Example:**
```bash
./cli.py comment
# Ticket ID: 24043
# Comment message: baik, dimengerti
# Sender SSO username (Who will you submit this ticket AS?): target_username
# Receiver SSO username (Who will you send this ticket TO?) [default is `admin`]: admin
```

Typically, you'd send the comment AS your target victim (*or yourself*) -> TO the `admin`. But if you want to do the opposite (from admin to target_victim), you need to specify the admin username.

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