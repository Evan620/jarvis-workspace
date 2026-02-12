#!/bin/bash

# JARVIS Self-Maintenance Script
# Runs weekly (Sundays 22:00) via cron
# Purpose: Review system health, clean up, suggest improvements

set -e

# Configuration
WORKSPACE="/home/evan/clawd"
LOG_DIR="$WORKSPACE/session-logs"
MEMORY_DIR="$WORKSPACE/memory"
TODAY=$(date +%Y-%m-%d)
LOG_FILE="$LOG_DIR/maintenance-$(date +%Y%m%d).log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

warn() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1" | tee -a "$LOG_FILE"
}

info() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

# Start maintenance
log "═══════════════════════════════════════════════════════════"
log "Starting JARVIS Self-Maintenance"
log "═══════════════════════════════════════════════════════════"

# Task 1: Review session logs
info "Task 1: Reviewing session logs..."
SESSION_COUNT=$(ls -1 "$LOG_DIR"/*.md 2>/dev/null | wc -l)
log "Found $SESSION_COUNT session log files"

# Check for empty or incomplete session logs
for file in "$LOG_DIR"/*.md; do
    if [ -f "$file" ]; then
        # Check if file has content (more than header)
        if [ $(wc -l < "$file") -lt 5 ]; then
            warn "Session log appears incomplete: $(basename $file)"
        fi
    fi
done

# Task 2: Archive old session logs (older than 30 days)
info "Task 2: Archiving old session logs..."
ARCHIVE_DIR="$LOG_DIR/archive"
mkdir -p "$ARCHIVE_DIR"

find "$LOG_DIR" -name "session-*.md" -mtime +30 -type f -exec mv {} "$ARCHIVE_DIR/" \; 2>/dev/null
ARCHIVED=$(ls -1 "$ARCHIVE_DIR"/*.md 2>/dev/null | wc -l)
log "Archived $ARCHIVED old session logs"

# Task 3: Review MEMORY.md health
info "Task 3: Checking MEMORY.md health..."
if [ -f "$WORKSPACE/MEMORY.md" ]; then
    MEMORY_SIZE=$(du -h "$WORKSPACE/MEMORY.md" | cut -f1)
    MEMORY_LINES=$(wc -l < "$WORKSPACE/MEMORY.md")
    log "MEMORY.md: $MEMORY_SIZE ($MEMORY_LINES lines)"

    # Check if MEMORY.md is too large (suggested limit: 5000 lines)
    if [ $MEMORY_LINES -gt 5000 ]; then
        warn "MEMORY.md is large ($MEMORY_LINES lines). Consider archiving old content."
    fi
else
    warn "MEMORY.md not found - will be created on next main session"
fi

# Task 4: Review NEXT-ACTIONS.md
info "Task 4: Reviewing NEXT-ACTIONS.md..."
if [ -f "$WORKSPACE/NEXT-ACTIONS.md" ]; then
    # Count active vs completed tasks
    ACTIVE_TASKS=$(grep -c "High Priority\|Medium Priority\|Low Priority" "$WORKSPACE/NEXT-ACTIONS.md" 2>/dev/null || echo "0")
    COMPLETED_TASKS=$(grep -c "✅ Completed" "$WORKSPACE/NEXT-ACTIONS.md" 2>/dev/null || echo "0")
    log "Active tasks: $ACTIVE_TASKS | Completed tasks: $COMPLETED_TASKS"

    # Check for overdue tasks
    if grep -q "due:.*$(date +%Y-%m-%d)" "$WORKSPACE/NEXT-ACTIONS.md" 2>/dev/null; then
        warn "Some tasks may be overdue - check NEXT-ACTIONS.md"
    fi
else
    warn "NEXT-ACTIONS.md not found"
fi

# Task 5: Check SKILL file consistency
info "Task 5: Checking SKILL files..."
SKILL_COUNT=$(find "$WORKSPACE/skills" -name "SKILL.md" 2>/dev/null | wc -l)
log "Found $SKILL_COUNT skill files"

# Check for SKILL files without proper structure
for skill_dir in "$WORKSPACE/skills"/*/; do
    if [ -d "$skill_dir" ]; then
        SKILL_FILE="$skill_dir/SKILL.md"
        if [ -f "$SKILL_FILE" ]; then
            # Check for key sections
            if ! grep -q "## Description" "$SKILL_FILE" 2>/dev/null; then
                warn "SKILL file missing description: $(basename $skill_dir)"
            fi
        else
            warn "Skill directory without SKILL.md: $(basename $skill_dir)"
        fi
    fi
done

# Task 6: Generate weekly summary
info "Task 6: Generating weekly summary..."
WEEKLY_SUMMARY="$LOG_DIR/weekly-summary-$(date +%Y%m%d).md"

cat > "$WEEKLY_SUMMARY" << EOF
# Weekly Summary - $(date +%Y-%m-%d)

## System Health
- Session logs: $SESSION_COUNT files
- Active tasks: $ACTIVE_TASKS
- Completed tasks: $COMPLETED_TASKS
- SKILL files: $SKILL_COUNT

## This Week's Activity
$(ls -1 "$LOG_DIR"/*.md 2>/dev/null | tail -7 | while read file; do
    echo "- $(basename $file)"
done)

## Items Requiring Attention
$(grep -r "⚠️\|⚡\|🔥" "$WORKSPACE"/*.md "$WORKSPACE/memory"/*.md 2>/dev/null | head -5 || echo "No urgent items found")

## Suggestions for Improvement
1. Review archived session logs for patterns
2. Consider consolidating related memory items
3. Update outdated skill documentation
4. Archive completed tasks from NEXT-ACTIONS.md

## Next Maintenance
- Scheduled: Next Sunday at 22:00
- Focus areas: System optimization, skill updates

---
Generated: $(date '+%Y-%m-%d %H:%M:%S')
EOF

log "Weekly summary created: $WEEKLY_SUMMARY"

# Task 7: Backup critical files
info "Task 7: Backing up critical files..."
BACKUP_DIR="$WORKSPACE/backups/$(date +%Y%m%d)"
mkdir -p "$BACKUP_DIR"

CRITICAL_FILES=(
    "$WORKSPACE/SOUL.md"
    "$WORKSPACE/AGENTS.md"
    "$WORKSPACE/USER.md"
    "$WORKSPACE/NEXT-ACTIONS.md"
    "$WORKSPACE/MEMORY-TAGGING.md"
    "$WORKSPACE/FIX-WORKFLOW.md"
)

BACKUP_COUNT=0
for file in "${CRITICAL_FILES[@]}"; do
    if [ -f "$file" ]; then
        cp "$file" "$BACKUP_DIR/"
        ((BACKUP_COUNT++))
    fi
done

log "Backed up $BACKUP_COUNT critical files to $BACKUP_DIR"

# Cleanup old backups (keep last 7 days)
find "$WORKSPACE/backups" -type d -mtime +7 -exec rm -rf {} + 2>/dev/null
log "Cleaned up old backups (keeping last 7 days)"

# Task 8: Check disk usage
info "Task 8: Checking disk usage..."
DISK_USAGE=$(df -h "$WORKSPACE" | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    warn "Disk usage is at ${DISK_USAGE}% - consider cleaning up"
else
    log "Disk usage: ${DISK_USAGE}% - healthy"
fi

# Task 9: Generate improvement suggestions
info "Task 9: Generating improvement suggestions..."
IMPROVEMENTS_FILE="$WORKSPACE/IMPROVEMENT-SUGGESTIONS.md"

cat > "$IMPROVEMENTS_FILE" << EOF
# JARVIS Improvement Suggestions
# Last Updated: $(date '+%Y-%m-%d %H:%M:%S')

## System-Level Improvements

### High Priority
EOF

# Add specific suggestions based on analysis
if [ $ACTIVE_TASKS -gt 20 ]; then
    echo "- [ ] Task queue has $ACTIVE_TASKS active items - consider archiving old tasks" >> "$IMPROVEMENTS_FILE"
fi

if [ $MEMORY_LINES -gt 5000 ]; then
    echo "- [ ] MEMORY.md is large - consider splitting into topic-specific files" >> "$IMPROVEMENTS_FILE"
fi

if [ $SESSION_COUNT -gt 50 ]; then
    echo "- [ ] Many session logs - consider consolidating patterns into SKILL files" >> "$IMPROVEMENTS_FILE"
fi

cat >> "$IMPROVEMENTS_FILE" << EOF

### Medium Priority
- [ ] Review and update SKILL files based on recent usage patterns
- [ ] Add new tags to MEMORY-TAGGING.md based on emerging categories
- [ ] Consider adding automated tests for critical workflows

### Low Priority
- [ ] Document common "Fix" scenarios in FIX-WORKFLOW.md
- [ ] Create templates for common task types
- [ ] Build visual dashboard for system metrics

## Skills to Review
$(find "$WORKSPACE/skills" -name "SKILL.md" -exec sh -c 'echo "- [ ] $(basename $(dirname {}))"' \;)

## Metrics to Track
- Session completion rate: Tasks started vs completed
- Memory retrieval speed: Average time to find information
- Fix frequency: How often corrections are needed
- Proactive suggestions: New ideas JARVIS proposes

---
Auto-generated by self-maintenance.sh
EOF

log "Improvement suggestions created: $IMPROVEMENTS_FILE"

# Final summary
log "═══════════════════════════════════════════════════════════"
log "Self-Maintenance Complete"
log "═══════════════════════════════════════════════════════════"
log "Session logs reviewed: $SESSION_COUNT"
log "Files archived: $ARCHIVED"
log "Active tasks: $ACTIVE_TASKS"
log "Backups created: $BACKUP_COUNT"
log "Disk usage: ${DISK_USAGE}%"
log "═══════════════════════════════════════════════════════════"
log "Next maintenance: Next Sunday at 22:00"
log "═══════════════════════════════════════════════════════════"

exit 0
