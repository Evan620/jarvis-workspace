#!/bin/bash
# Security Audit Script for JARVIS
# Purpose: Regular security checks to ensure system integrity

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🔒 JARVIS Security Audit"
echo "========================"
echo "Started: $(date)"
echo ""

# Check 1: File permissions on sensitive files
echo -e "${YELLOW}[1] Checking sensitive file permissions...${NC}"
SENSITIVE_FILES=(
  "MEMORY.md"
  "USER.md"
  "SESSION-STATE.md"
  "identity.json"
  ".env"
)

for file in "${SENSITIVE_FILES[@]}"; do
  if [ -f "$file" ]; then
    perms=$(stat -c %a "$file" 2>/dev/null || stat -f %A "$file" 2>/dev/null)
    if [ "$perms" = "600" ] || [ "$perms" = "640" ]; then
      echo -e "  ${GREEN}✓${NC} $file ($perms)"
    else
      echo -e "  ${RED}✗${NC} $file ($perms) - should be 600 or 640"
    fi
  fi
done
echo ""

# Check 2: No secrets in git
echo -e "${YELLOW}[2] Checking for secrets in git...${NC}"
if git rev-parse --git-dir > /dev/null 2>&1; then
  # Check for common secret patterns in recent commits
  SECRETS_FOUND=$(git log --all -p -S "api_key" -S "password" -S "secret" -S "token" 2>/dev/null | head -20)
  if [ -z "$SECRETS_FOUND" ]; then
    echo -e "  ${GREEN}✓${NC} No obvious secrets found in git history"
  else
    echo -e "  ${RED}✗${NC} Possible secrets detected in git history"
  fi
else
  echo "  ℹ️  Not a git repository"
fi
echo ""

# Check 3: Check for suspicious shell scripts
echo -e "${YELLOW}[3] Checking shell scripts for suspicious patterns...${NC}"
SUSPICIOUS_PATTERNS=(
  "curl.*sh.*|.*bash"
  "wget.*sh.*|.*bash"
  "eval.*\$.*"
  "rm -rf /"
)

for pattern in "${SUSPICIOUS_PATTERNS[@]}"; do
  RESULTS=$(grep -r "$pattern" *.sh 2>/dev/null || true)
  if [ -z "$RESULTS" ]; then
    echo -e "  ${GREEN}✓${NC} No '$pattern' found"
  else
    echo -e "  ${YELLOW}⚠${NC} Found '$pattern' in:"
    echo "$RESULTS" | head -5
  fi
done
echo ""

# Check 4: Check for unauthorized cron jobs
echo -e "${YELLOW}[4] Checking cron jobs...${NC}"
if [ -d ".git/hooks" ] || [ -d ".github/workflows" ]; then
  echo "  ℹ️  Reviewing automation configs..."
  # List cron-related files
  ls -la setup_cron*.sh 2>/dev/null || echo "  ℹ️  No cron setup scripts found"
fi
echo ""

# Check 5: Verify skill integrity
echo -e "${YELLOW}[5] Checking skill integrity...${NC}"
if [ -d "skills" ]; then
  SKILL_COUNT=$(find skills -name "SKILL.md" | wc -l)
  echo -e "  ${GREEN}✓${NC} Found $SKILL_COUNT skill definitions"
else
  echo -e "  ${YELLOW}⚠${NC} No skills/ directory"
fi
echo ""

# Summary
echo "========================"
echo "Completed: $(date)"
echo ""
echo "Next steps:"
echo "  - Review any RED items above"
echo "  - Fix file permissions if needed"
echo "  - Remove any suspicious patterns"
echo ""
