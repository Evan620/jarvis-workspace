---
name: linkedin
description: LinkedIn CLI for searching people, companies, jobs, viewing profiles, and messaging.
homepage: https://github.com/tomquirk/linkedin-api
metadata: {"clawdbot":{"emoji":"💼","requires":{"bins":["linkedin-cli"]}}}
---

# LinkedIn CLI

Search people, companies, and jobs on LinkedIn. View profiles and send messages.

## Setup (Required First)

Configure credentials (interactive):
```bash
linkedin-cli configure
```

Or with arguments:
```bash
linkedin-cli configure --email "your@email.com" --password "yourpassword"
```

Check status:
```bash
linkedin-cli check
```

## Commands

### Search People
```bash
linkedin-cli search "software engineer" -n 10
linkedin-cli search "data scientist Kenya" --json
```

### Search Companies
```bash
linkedin-cli companies "fintech startup"
linkedin-cli companies "climate tech" -n 5
```

### Search Jobs
```bash
linkedin-cli jobs "python developer"
linkedin-cli jobs "AI engineer" -l "Nairobi" -n 20
linkedin-cli jobs "remote software" --remote
```

### View Profile
```bash
linkedin-cli profile billy-g
linkedin-cli profile lazarus-magwaro-0067b333a --json
```

### Get Contact Info
```bash
linkedin-cli contact username
```

### Get Connections (1st degree)
```bash
linkedin-cli connections username -n 50
```

### Send Message
```bash
linkedin-cli message username "Hello! I'd like to connect."
```

### Who Am I
```bash
linkedin-cli whoami
```

## Output Formats

Add `--json` to most commands for JSON output:
```bash
linkedin-cli search "CEO" --json | jq '.[] | .name'
```

## Notes

- Uses unofficial LinkedIn API (no official API key needed)
- Requires valid LinkedIn account credentials
- Rate limits apply - don't spam
- May violate LinkedIn ToS - use responsibly
- Credentials stored in `~/.config/linkedin/credentials.json`

## CLI Location

`/home/evan/clawd/skills/linkedin/linkedin-cli`
