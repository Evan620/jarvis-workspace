# Message Monitor Setup

This project contains a Go script `message_monitor.go` that monitors and summarizes unread Gmail and WhatsApp messages.

## Files

- `message_monitor.go`: The main monitoring script.
- `setup_cron_30min.sh`: Shell script to build the Go program and set up the cron job for running every 30 minutes.

## Setup Instructions

1. Build the Go program and set up the cron job by running:

   ```bash
   bash setup_cron_30min.sh
   ```

2. The program will run every 30 minutes and append logs to `message_monitor.log`.

3. Modify `message_monitor.go` to integrate your actual Gmail and WhatsApp fetching and notification sending implementations.

---

If you want a different schedule, edit the cron expression in `setup_cron_30min.sh` accordingly.
