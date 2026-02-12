#!/bin/bash

# Gmail Classification Script
# Categorizes emails based on patterns

INPUT_FILE="/tmp/gmail_inbox_scan.json"
OUTPUT_FILE="/tmp/gmail_categorized.json"

# Create output structure
cat > "$OUTPUT_FILE" << 'EOF'
{
  "auto_archive": [],
  "needs_attention": [],
  "important": [],
  "promotions": [],
  "updates": [],
  "social": [],
  "forums": [],
  "other": []
}
EOF

# Read and classify emails
python3 << 'PYTHON_SCRIPT'
import json

with open('/tmp/gmail_inbox_scan.json', 'r') as f:
    data = json.load(f)

categories = {
    "auto_archive": [],
    "needs_attention": [],
    "important": [],
    "promotions": [],
    "updates": [],
    "social": [],
    "forums": [],
    "other": []
}

for thread in data.get('threads', []):
    email = {
        "id": thread['id'],
        "date": thread['date'],
        "from": thread['from'],
        "subject": thread['subject'],
        "labels": thread['labels']
    }

    # Skip archived
    if 'INBOX' not in thread['labels']:
        categories['auto_archive'].append(email)
        continue

    # High priority / needs attention
    keywords_urgent = ['urgent', 'asap', 'critical', 'important', 'deadline', 'invoice', 'payment']
    subject_lower = thread['subject'].lower()
    from_lower = thread['from'].lower()

    if any(kw in subject_lower or kw in from_lower for kw in keywords_urgent):
        categories['needs_attention'].append(email)
        continue

    # Already marked important by user
    if 'IMPORTANT' in thread['labels']:
        categories['important'].append(email)
        continue

    # Promotions (newsletter, offers, marketing)
    if 'CATEGORY_PROMOTIONS' in thread['labels']:
        categories['promotions'].append(email)
        continue

    # Updates (notifications, confirmations, system alerts)
    if 'CATEGORY_UPDATES' in thread['labels']:
        categories['updates'].append(email)
        continue

    # Social (social media, personal)
    if 'CATEGORY_SOCIAL' in thread['labels']:
        categories['social'].append(email)
        continue

    # Forums
    if 'CATEGORY_FORUMS' in thread['labels']:
        categories['forums'].append(email)
        continue

    # Default to other
    categories['other'].append(email)

# Save categorized results
with open('/tmp/gmail_categorized.json', 'w') as f:
    json.dump(categories, f, indent=2)

# Print summary
for cat_name, emails in categories.items():
    print(f"{cat_name.replace('_', ' ').title()}: {len(emails)} emails")
PYTHON_SCRIPT

echo ""
echo "✅ Classification complete!"
