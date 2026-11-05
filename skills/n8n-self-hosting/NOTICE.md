# Notices

`n8n-self-hosting` is imported from [czlonkowski/n8n-mcp](https://github.com/czlonkowski/n8n-mcp) at revision `1c755c5c8d99eb71faade17753a7f24138f4212c` under the MIT License (Copyright (c) 2024 Romuald Czlonkowski @ www.aiadvisors.pl/en); see `LICENSE`.

## Runtime & Infrastructure Prerequisites

- Deploying self-hosted n8n stacks requires Docker Engine and Docker Compose v2 on your target host, along with a domain name and DNS A/AAAA record if using automatic TLS via Caddy.
- All configuration templates (`assets/docker-compose.single.yml`, `assets/docker-compose.queue.yml`, `assets/.env.single.example`, `assets/.env.queue.example`, `assets/Caddyfile`, `assets/init-data.sh`) are shipped as static reference files inside `assets/` and never contain live secrets.

## Safe Operation

Installation via `./vas install` or the no-clone Web Agent Prompt only links or copies static files and writes `.vas-manifest.json`.
No scripts or containers are executed, no runtime or MCP server is installed, and no external services are connected during installation.
