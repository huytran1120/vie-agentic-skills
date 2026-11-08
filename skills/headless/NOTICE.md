# Notices

`headless` is imported from [`kunchenguid/headless`](https://github.com/kunchenguid/headless) at revision `fe1a381c6f382ec3c9822da0e706484414bc63e0` (`skills/headless/SKILL.md`) under the MIT License (Copyright (c) 2026 Kun Chen); see `LICENSE`.

## Purpose & Bundled Payload

- Step-by-step setup, configuration, verification, and unattended restart verification of a headless macOS (Apple silicon), Linux (NixOS, Debian, Ubuntu, Fedora), or Windows (Windows 11, Windows Server 2025) machine over SSH.
- Secret isolation via `scripts/secret-run.sh`: the admin password stays in the user's secret store (Automic Vault, 1Password CLI, Bitwarden CLI, a custom command, or a mode-0600 env file) and is piped on file descriptor 3; the agent only ever handles the store entry reference.
- Standalone payload includes `SKILL.md`, `references/` (`mac.md`, `linux.md`, `windows.md`, `secrets.md`, `tailscale.md`), `scripts/` (`secret-run.sh`, `mac/`, `linux/`, `windows/`, `remote/`), `assets/` (`darwin/`, `nixos/`, `windows/`), and bundled copies of the upstream Nix modules in `modules/` (`darwin/headless.nix`, `nixos/headless.nix`).

## Prerequisites & Safe Operation

- Local machine prerequisites: `bash`, `ssh`, `tar` (and `nix` only when using `install-nixos.sh` with `nixos-anywhere`).
- Target machine prerequisites: reachable over SSH with an administrator/sudo account and password stored in the chosen secret store.
- Installation via `./vas install` or the no-clone Web Agent Prompt only links or copies static files and writes `.vas-manifest.json`. No script, SSH connection, secret store command, or Nix build is executed during installation.
