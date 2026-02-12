#!/bin/bash
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 <query>"
  exit 1
fi

QUERY="$*"

# Prefer real SERP-style results via ddgs CLI (powerful)
if command -v ddgs >/dev/null 2>&1; then
  ddgs text -k "$QUERY" -m 8
  exit 0
fi

# Fallback: DuckDuckGo Instant Answer API (limited)
ENCODED_QUERY=$(python3 -c 'import sys, urllib.parse; print(urllib.parse.quote_plus(sys.argv[1]))' "$QUERY")
API_URL="https://api.duckduckgo.com/?q=${ENCODED_QUERY}&format=json&nohtml=1&skip_disambig=1"
response=$(curl -s "$API_URL")

abstract_text=$(echo "$response" | jq -r '.AbstractText // empty')
abstract_url=$(echo "$response" | jq -r '.AbstractURL // empty')
redirect_url=$(echo "$response" | jq -r '.Redirect // empty')

if [ -n "$abstract_text" ]; then
  echo -e "$abstract_text\nURL: $abstract_url"
elif [ -n "$redirect_url" ]; then
  echo "Redirect: $redirect_url"
else
  echo "No direct answer found (and ddgs not installed)."
fi

