#!/bin/bash
# Browser.cash Verification Script
# Test that your API key works

SKILL_DIR="/home/evan/clawd/skills/browser-cash"

echo "🔍 Browser.cash API Key Verification"
echo "==============================="
echo ""

# Check if key is configured
BROWSER_CASH_KEY=$(clawdbot config get skills.entries.browser-cash.apiKey 2>/dev/null)

if [ -z "$BROWSER_CASH_KEY" ]; then
  echo "❌ API key not configured"
  echo ""
  echo "To configure:"
  echo "  1. Go to https://dash.browser.cash"
  echo "  2. Create account or sign in"
  echo "  3. Generate API token"
  echo "  4. Run: clawdbot config set skills.entries.browser-cash.apiKey 'your_key_here'"
  echo ""
  echo "After configuring, run this script again to verify."
  exit 1
fi

echo "✅ API key found (first 20 chars: ${BROWSER_CASH_KEY:0:20}...)"
echo ""

# Create test session
echo "Creating test session..."
SESSION=$(curl -s -X POST "https://api.browser.cash/v1/browser/session" \
  -H "Authorization: Bearer $BROWSER_CASH_KEY" \
  -H "Content-Type: application/json" \
  -d '{"country": "US", "windowSize": "1920x1080"}')

echo "Session response:"
echo "$SESSION" | jq '.' 2>/dev/null || echo "$SESSION"
echo ""

# Extract session info
SESSION_ID=$(echo "$SESSION" | jq -r '.sessionId' 2>/dev/null)
STATUS=$(echo "$SESSION" | jq -r '.status' 2>/dev/null)
CDP_URL=$(echo "$SESSION" | jq -r '.cdpUrl' 2>/dev/null)

if [ -z "$SESSION_ID" ]; then
  echo "❌ Failed to create session"
  exit 1
fi

echo "✅ Session created successfully!"
echo "  Session ID: $SESSION_ID"
echo "  Status: $STATUS"
echo "  CDP URL: $CDP_URL"
echo ""

# Clean up - stop test session
echo "Cleaning up test session..."
DELETE_RESULT=$(curl -s -w "%{http_code}" -X DELETE "https://api.browser.cash/v1/browser/session?sessionId=$SESSION_ID" \
  -H "Authorization: Bearer $BROWSER_CASH_KEY")

echo "Delete response code: $DELETE_RESULT"
echo ""

echo "✅ Verification complete!"
echo ""
echo "Your Browser.cash API key is working."
echo "You can now use Browser.cash for unblocked browser sessions."
