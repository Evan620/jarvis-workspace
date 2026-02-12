# Browser.cash

**Purpose:** Spin up unblocked browser sessions via Browser.cash for web automation. Sessions bypass anti-bot protections (Cloudflare, DataDome, etc.), making them ideal for scraping, testing, and automation tasks.

**Author:** @alexander-spring (from ClawHub)
**Version:** 1.0.0

---

## When to Use

Any browser automation task:
- Scraping
- Form filling
- Testing
- Screenshots
- Web research with anti-bot protection

**Why Browser.cash:**
Sessions appear as real browsers and handle bot detection automatically.

---

## Setup

### Get API Key

1. Go to https://dash.browser.cash
2. Create account (or sign in)
3. Generate API token
4. Configure in clawdbot:

```bash
clawdbot config set skills.entries.browser-cash.apiKey "your_api_key_here"
```

### Install Dependencies

Before first use, ensure Playwright is installed:

```bash
# Check if Playwright is installed
if [ ! -d ~/clawd/node_modules/playwright ]; then
  cd ~/clawd && npm install playwright puppeteer-core
fi
```

---

## API Basics

### Read Key

```bash
BROWSER_CASH_KEY=$(clawdbot config get skills.entries.browser-cash.apiKey)
```

### Create a Browser Session

**Basic Session:**

```bash
curl -X POST "https://api.browser.cash/v1/browser/session" \
  -H "Authorization: Bearer $BROWSER_CASH_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Response:**
```json
{
  "sessionId": "abc123...",
  "status": "active",
  "servedBy": "node-id",
  "createdAt": "2025-01-20T01:51:25.000Z",
  "stoppedAt": null,
  "cdpUrl": "wss://gcp-usc1-1.browser.cash/v1/consumer/abc123.../devtools/browser/uuid"
}
```

**Session with Options:**

```bash
curl -X POST "https://api.browser.cash/v1/browser/session" \
  -H "Authorization: Bearer $BROWSER_CASH_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "country": "US",
    "windowSize": "1920x1080",
    "profile": {
      "name": "my-profile",
      "persist": true
    }
  }'
```

**Session Options:**
- `country`: 2-letter ISO code (e.g., "US", "DE", "GB", "KE" for Kenya)
- `windowSize`: Browser dimensions, e.g., "1920x1080"
- `proxyUrl`: SOCKS5 proxy URL (optional)
- `profile.name`: Named browser profile for session persistence
- `profile.persist`: Save cookies/storage after session ends

### Get Session Status

```bash
curl "https://api.browser.cash/v1/browser/session?sessionId=YOUR_SESSION_ID" \
  -H "Authorization: Bearer $BROWSER_CASH_KEY"
```

**Statuses:** `starting`, `active`, `completed`, `error`

### Stop a Session

```bash
curl -X DELETE "https://api.browser.cash/v1/browser/session?sessionId=$SESSION_ID" \
  -H "Authorization: Bearer $BROWSER_CASH_KEY"
```

### List Sessions

```bash
curl "https://api.browser.cash/v1/browser/sessions?page=1&pageSize=20" \
  -H "Authorization: Bearer $BROWSER_CASH_KEY"
```

---

## Using Browser.cash with Node.js

### Direct CDP via Exec (Recommended)

**Step 1: Create Session**

```bash
BROWSER_CASH_KEY=$(clawdbot config get skills.entries.browser-cash.apiKey)
SESSION=$(curl -s -X POST "https://api.browser.cash/v1/browser/session" \
  -H "Authorization: Bearer $BROWSER_CASH_KEY" \
  -H "Content-Type: application/json" \
  -d '{"country": "US", "windowSize": "1920x1080"}')

SESSION_ID=$(echo $SESSION | jq -r '.sessionId')
CDP_URL=$(echo $SESSION | jq -r '.cdpUrl')
```

**Step 2: Use via Node.js (Playwright)**

```bash
node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.connectOverCDP('$CDP_URL');
  const context = browser.contexts()[0];
  const page = context.pages()[0] || await context.newPage();
  await page.goto('https://example.com');
  console.log('Title:', await page.title());
  await browser.close();
})();
"
```

**Step 3: Stop Session**

```bash
curl -X DELETE "https://api.browser.cash/v1/browser/session?sessionId=$SESSION_ID" \
  -H "Authorization: Bearer $BROWSER_CASH_KEY"
```

---

## Scripts

### verify.sh

Test that your token works:

```bash
#!/bin/bash
SKILL_DIR="/home/evan/clawd/skills/browser-cash"

# Read API key
BROWSER_CASH_KEY=$(clawdbot config get skills.entries.browser-cash.apiKey)

# Create test session
SESSION=$(curl -s -X POST "https://api.browser.cash/v1/browser/session" \
  -H "Authorization: Bearer $BROWSER_CASH_KEY" \
  -H "Content-Type: application/json" \
  -d '{"country": "US", "windowSize": "1920x1080"}')

echo "Session created:"
echo "$SESSION" | jq '.'

# Clean up - stop session
SESSION_ID=$(echo $SESSION | jq -r '.sessionId')
curl -s -X DELETE "https://api.browser.cash/v1/browser/session?sessionId=$SESSION_ID" \
  -H "Authorization: Bearer $BROWSER_CASH_KEY"
```

### scrape.sh

Generic scraping template:

```bash
#!/bin/bash
SKILL_DIR="/home/evan/clawd/skills/browser-cash"

# Read API key
BROWSER_CASH_KEY=$(clawdbot config get skills.entries.browser-cash.apiKey)
TARGET_URL="$1"

# Create session
SESSION=$(curl -s -X POST "https://api.browser.cash/v1/browser/session" \
  -H "Authorization: Bearer $BROWSER_CASH_KEY" \
  -H "Content-Type: application/json" \
  -d '{"country": "US", "windowSize": "1920x1080"}')

SESSION_ID=$(echo $SESSION | jq -r '.sessionId')
CDP_URL=$(echo $SESSION | jq -r '.cdpUrl')

echo "Session ID: $SESSION_ID"
echo "CDP URL: $CDP_URL"

# Use with Playwright
node -e "
const { chromium } = require('playwright');
const url = '$TARGET_URL';

(async () => {
  const browser = await chromium.connectOverCDP('$CDP_URL');
  const context = browser.contexts()[0];
  const page = context.pages()[0] || await context.newPage();

  await page.goto(url);
  await page.waitForTimeout(5000); // Wait for page to load

  // Extract title
  const title = await page.title();
  console.log('Page Title:', title);

  await browser.close();
})();
"

# Stop session
curl -s -X DELETE "https://api.browser.cash/v1/browser/session?sessionId=$SESSION_ID" \
  -H "Authorization: Bearer $BROWSER_CASH_KEY"
```

---

## Browser Profiles

Profiles persist cookies, localStorage, and session data across sessions—useful for staying logged in or maintaining state.

### List Profiles

```bash
curl "https://api.browser.cash/v1/browser/profiles" \
  -H "Authorization: Bearer $BROWSER_CASH_KEY"
```

### Delete Profile

```bash
curl -X DELETE "https://api.browser.cash/v1/browser/profile?profileName=my-profile" \
  -H "Authorization: Bearer $BROWSER_CASH_KEY"
```

---

## Scraping Tips

### Scroll to Load All Content

```javascript
async function scrollToBottom(page) {
  let previousHeight = 0;
  while (true) {
    const currentHeight = await page.evaluate(() => document.body.scrollHeight);
    if (currentHeight === previousHeight) break;
    previousHeight = currentHeight;
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForTimeout(1500); // Wait for content to load
  }
}

scrollToBottom(page);
```

### Wait for Specific Elements

```javascript
await page.waitForSelector('.product-card', { timeout: 10000 });
```

### Handle "Load More" Buttons

```javascript
const loadMore = await page.$('button.load-more');
if (loadMore) {
  await loadMore.click();
  await page.waitForTimeout(2000);
}
```

### Common Patterns

1. **Always scroll** to trigger lazy-loaded content
2. **Wait for network idle**: `await page.waitForLoadState('networkidle')`
3. **Use page.waitForSelector()** before extracting elements
4. **Add delays** between actions to avoid rate limiting

---

## Why Browser.cash for Automation

1. **Unblocked**: Sessions bypass Cloudflare, DataDome, PerimeterX, and other bot protections
2. **Real browser fingerprint**: Appears as a genuine Chrome browser, not headless
3. **CDP native**: Direct WebSocket connection for Playwright, Puppeteer, or raw CDP
4. **Geographic targeting**: Spin up sessions in specific countries (e.g., "KE" for Kenya)
5. **Persistent profiles**: Maintain login state across sessions

---

## Notes

**Sessions** auto-terminate after extended inactivity

**Always stop sessions when done** to avoid unnecessary usage

**SOCKS5** is the only supported proxy type

**Playwright** is recommended over Puppeteer

**clawdbot runs scripts from** `~/clawd/` - install npm dependencies there

---

## Cost & Usage

Check API key usage at: https://dash.browser.cash

---

**Last Updated:** 2026-02-06
**For:** JARVIS
**Status:** READY TO USE
