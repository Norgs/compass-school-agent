---
name: compass-school-agent
description: Use when building, deploying, or maintaining the Compass school notification agent.
version: 1.2.0
author: User
license: MIT
metadata:
  hermes:
    tags: [school, compass, gmail, notification, agent, dashboard]
    related_skills: [google-workspace]
---
# Compass School Notification Agent

## When to Use
Use when building, deploying, or maintaining an automated agent that ingests school portal notification emails (such as Compass), categorizes events, updates structured task stores, and serves local HTML web dashboards or Telegram digests.

## Overview
Automated pipeline to ingest Compass school notification emails via Gmail, structure them with LLM extraction, categorize by urgency/child/action, and serve both a Telegram digest and a live local HTML web dashboard on OC01.

## Workflow
1. **Gmail Ingestion:** Connect via Google Workspace OAuth (`google_token.json`) and search emails with query terms like `compass`.
2. **Parsing & Extraction:** Extract fields (date, sender, subject, body snippet) and classify urgency (`Excursion`, `Payment Needed`, `Action Required`, `Informational`) and child.
3. **Child Baseline Mapping:** Always map school/sender keywords to the correct family baseline (e.g. Melbourne Girls' College -> Brae; Kew High School -> Jy & Quade; Deepdene -> Ivy).
4. **State Storage:** Persist structured items as JSON to `~/.hermes/data/compass_todo.json`.
5. **Local Dashboard & LAN Access:** 
   - Serve a live, auto-refreshing UI with high-contrast badge styles and clear category separation (e.g., Red for Action, Amber for Payment, Indigo for Excursions, Green for Info).
   - Containerize the frontend with `nginx:alpine` using custom `nginx.conf` and Docker Compose (`restart: unless-stopped`) to ensure availability across the LAN on reboot.
   - For LAN HTTPS on private IP/local domains, generate 10-year self-signed certificates with `openssl` mounted into `/etc/nginx/certs/` rather than Let's Encrypt (which requires public FQDNs).
   - Mount persistent JSON data (`~/.hermes/data/compass_todo.json`) into the container as read-only (`ro`) so the native host scraper can continue updating without altering storage locations.
6. **Cron Automation:** Schedule twice-daily background runs via Hermes cron (`cronjob_manage`).

## Pitfalls & Troubleshooting
- **Google OAuth Expiration:** Tokens created in "Testing" publishing status expire after 7 days; move the Google Cloud project's publishing status to "In Production" to keep tokens active indefinitely for personal use.
- **API Enablement:** Ensure the Gmail API is explicitly enabled in the Google Cloud Console project before authorizing tokens, otherwise API calls fail with `accessNotConfigured`.
- **Card Readability:** Keep event summaries visually distinct by separating badges, child names, and dates into clear header rows above card titles and body snippets.
- **Process Termination:** When replacing local Python servers, terminate existing processes completely (`pkill -f` or PID kill) before starting container bindings on port 8085 to prevent port binding collisions.
- **Git Backup:** Maintain and backup configuration and container files (Docker Compose, Nginx config, static HTML, self-signed certs) in a local Git repository and push to GitHub as a disaster recovery reference.
