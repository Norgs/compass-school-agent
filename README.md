# Compass School Dashboard Container

A lightweight, containerized web dashboard to display school notifications and action items scraped from Compass emails across your home LAN.

## Project Structure
- `docker-compose.yml`: Defines the `nginx:alpine` container service with auto-restart (`unless-stopped`) on port `8085`.
- `nginx.conf`: Nginx configuration enforcing HTTPS via self-signed certificates and serving the static frontend and JSON data endpoint (`/data`).
- `index.html`: Clean, responsive single-page frontend that fetches and displays color-coded school to-do items.
- `certs/`: Contains the 10-year self-signed TLS certificate (`server.crt`) and private key (`server.key`).

## Volume Mounts & Data Storage
The scraped data is maintained natively on the host at `~/.hermes/data/compass_todo.json` and mounted read-only into the Nginx container (`/usr/share/nginx/html/compass_todo.json`). The Hermes background cron job (`compass-sync-agent`) handles syncing emails twice daily.

## LAN Access
Accessible over HTTPS across your home network at:
`https://<OC01-LAN-IP>:8085`
