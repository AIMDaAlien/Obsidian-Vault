---
tags: [self-hosting, ssh, truenas, security, hardening]
created: 2026-02-18
published_to_garden: true
visibility: public
---

# SSH Hardening on TrueNAS SCALE

## Goal

Key-only login for a non-root admin account. Root SSH and password auth both disabled.

## Why this matters

On a public internet host, SSH is the top brute-force target. The two most impactful changes are disabling password auth and disabling root login. Everything else is secondary.

## Safe procedure (don't lock yourself out)

Do this in order. Don't skip to the hardening step before you've confirmed the new account works.

1. Create a new admin user and add your SSH public key to it.
2. Open a **new** SSH session as that user and confirm it connects successfully.
3. Only then disable root login and password auth.

## Option A — TrueNAS UI (recommended)

1. Credentials → Local Users: add an admin user, enable sudo/admin as appropriate, paste your SSH public key.
2. System Settings → Services → SSH: disable "Log in as Root" and disable "Password Authentication."
3. Restart the SSH service.

## Option B — Script (dry-run by default)

The repo includes `scripts/truenas_ssh_hardening.sh` for scripted setup.

```bash
# Dry run (no changes made)
./scripts/truenas_ssh_hardening.sh --admin-user adminuser --pubkey-file /root/adminuser.pub

# Apply user creation and key update only
./scripts/truenas_ssh_hardening.sh --admin-user adminuser --pubkey-file /root/adminuser.pub --apply

# After confirming the admin login works, harden sshd
./scripts/truenas_ssh_hardening.sh --admin-user adminuser --pubkey-file /root/adminuser.pub --apply --disable-root --disable-password
```

## Important note on TrueNAS config persistence

TrueNAS stores persistent SSH config in its middleware layer. Editing `/etc/ssh/sshd_config` directly works until the next reboot or system update, then it'll get overwritten. Use the TrueNAS UI or a script that goes through the middleware if you want changes to survive reboots.
