---
created: 2026-02-13T10:37:00.000000
modified: 2026-02-13T10:37:00.000000
privacy_scan: not_scanned
published_to_garden: false
tags: [penthouse, deployment, android, truenas, caddy, session-log, troubleshooting, security, reliability, checklist]
title: The Penthouse - Session Notes 2026-02-13
visibility: private
---

# The Penthouse - Session Notes 2026-02-13

## Session Overview
Marathon session covering push notification fixes, on-prem TrueNAS deployment, Caddy HTTPS setup, Android APK build troubleshooting, and initial mobile testing. First successful APK build and install on a real Android device.

---

## Key Accomplishments

### 1. Push Notification Fixes 🔔

**Problem:** Notifications showed raw `userId` instead of sender's display name.

**Fix:**
- Updated `server/src/websocket.js` to fetch `displayName` from the database before sending push
- Added logic to skip push notifications for users actively in the chat (via Socket.IO rooms)
- Verified end-to-end push flow

### 2. TrueNAS On-Prem Deployment 🖥️

**Docker Configuration:**
- Fixed volume path mismatch in `docker-compose.yml` (`./data:/app/data`)
- Updated `Dockerfile.production` for consistent data directory structure
- Created `.env.example` with all production environment variables
- Server deployed at `192.168.0.120:3000`

**Data Persistence:**
- SQLite database stored at `/app/data/penthouse.db` (persisted via Docker volume)
- Uploads stored at `/app/data/uploads/`
- APK downloads at `/app/data/downloads/`

**Created `DEPLOYMENT.md`** — full TrueNAS setup guide including:
- Docker installation, SSH access, git clone
- Environment variable configuration
- Container management commands
- Backup procedures

### 3. Caddy HTTPS Configuration 🔒

**Setup:**
- Added Caddy as a reverse proxy service in `docker-compose.yml`
- Created `Caddyfile` for `penthouse.blog` → `penthouse-app:3000`
- Mapped ports: `9080:80` and `9443:443` (TrueNAS uses 80/443 for its own UI)

**Router Port Forwarding (TP-Link):**
- External `443` → Internal `9443` (SSL)
- External `80` → Internal `9080` (HTTP)

**Current Issue:** Caddy can't obtain SSL certificates because `penthouse.blog` DNS is proxied through **Cloudflare** (resolves to Cloudflare IPs `104.21.9.162`, `172.67.160.73`). Let's Encrypt ACME challenges fail with HTTP 530.

**Fix Needed:** Disable Cloudflare proxy (orange cloud → gray/DNS only) OR use Cloudflare's origin certificates.

### 4. Android APK Build 📱

**Build Failures Debugged:**

| Attempt | Error | Root Cause |
|---------|-------|------------|
| 1-2 | `Build request failed` | EAS server-side rejection |
| 3 | Gradle: `ANDROID_HOME not set` | Local build without Android SDK |
| 4-5 | `AAPT: file failed to compile` | **JPEG images with .png extensions** |
| 6 (Final) | ✅ Success | Fixed image formats |

**The AAPT Fix (Key Learning):**
- `penthouse-bg.png` and `lounge-bg.png` were JPEG files renamed to `.png`
- Android's AAPT resource compiler is strict — extension must match actual format
- Used `sips -s format png` on macOS to convert to real PNGs
- `file <filename>` command reveals actual format regardless of extension

**Build Details:**
- Platform: EAS Build (cloud)
- Profile: `preview` (generates `.apk` not `.aab`)
- Build time: ~15-20 minutes in free tier queue
- SDK: Expo SDK 54, React Native

### 5. APK Deployment Script 📤

**`scripts/deploy_apk.sh`:**
- SCPs the APK to TrueNAS at `/mnt/Storage_Pool/penthouse/app/data/downloads/the-penthouse.apk`
- Handles missing `sshpass` gracefully (falls back to interactive password)
- Creates remote directory if it doesn't exist (`mkdir -p` via SSH)
- Server credentials: `root@192.168.0.120`

### 6. Mobile API Configuration 📡

**`mobile/src/services/api.ts` URL Logic:**
```typescript
const origin = Constants.expoConfig?.hostUri?.split(':')[0];
const BASE_URL = origin ? `http://${origin}:3000` : 'https://penthouse.blog';
```
- In dev (Expo Go): Uses local machine IP (e.g., `http://192.168.0.x:3000`)
- In production (APK): Falls back to `https://penthouse.blog`

---

## Current State

### What's Working ✅
- Server running on TrueNAS at `192.168.0.120:3000`
- Docker containers healthy (penthouse-app + caddy)
- APK built, downloaded, and installed on Android device
- Deploy script works for uploading APK to server
- Router port forwarding configured correctly

### What's Broken ❌
- **Auth on Android:** Can't register or login from the APK
  - Root cause: `penthouse.blog` DNS goes through Cloudflare, not directly to home IP
  - Caddy can't get SSL cert (ACME fails with 530)
  - App tries `https://penthouse.blog` which doesn't route to the server
- **No deployment automation:** Every update requires manual: build APK → download → SCP → SSH → git pull → docker rebuild

### What's Needed 🔲
- Fix DNS (disable Cloudflare proxy OR use Cloudflare origin certs)
- Automate the deployment pipeline (push → build → deploy)
- Test auth flow end-to-end once DNS is fixed
- Consider NAT hairpinning (testing from same LAN as server may not work)

---

## Technical Architecture

```
┌─────────────┐     ┌───────────────┐     ┌──────────────┐
│ Android APK │────▶│ penthouse.blog│────▶│  Router      │
│ (Expo/RN)   │     │ (DNS)         │     │  (TP-Link)   │
└─────────────┘     └───────────────┘     └──────┬───────┘
                                                  │
                                    Port 443→9443 │ Port 80→9080
                                                  │
                                          ┌───────▼───────┐
                                          │  TrueNAS      │
                                          │  192.168.0.120│
                                          └───────┬───────┘
                                                  │
                                    ┌─────────────┼─────────────┐
                                    │             │             │
                              ┌─────▼─────┐ ┌────▼────┐  ┌────▼────┐
                              │   Caddy   │ │ Node.js │  │ SQLite  │
                              │ :80/:443  │▶│  :3000  │──│  .db    │
                              │ (HTTPS)   │ │ (API)   │  │ (data)  │
                              └───────────┘ └─────────┘  └─────────┘
```

---

## Files Modified This Session

| File | Change |
|------|--------|
| `server/src/websocket.js` | Push notification displayName fix |
| `docker-compose.yml` | Added Caddy service, port mappings |
| `Caddyfile` | **NEW** — reverse proxy config |
| `Dockerfile.production` | Data directory consistency |
| `.env.example` | Production env vars |
| `DEPLOYMENT.md` | **NEW** — full deployment guide |
| `mobile/src/services/api.ts` | Production URL logic |
| `mobile/assets/penthouse-bg.png` | Converted JPEG→PNG |
| `mobile/assets/lounge-bg.png` | Converted JPEG→PNG |
| `scripts/deploy_apk.sh` | Directory creation + sshpass fallback |
| `mobile/eas.json` | Build profile config |

---

## Action Items

### Pending (Blocking)
- [ ] Fix `penthouse.blog` DNS — disable Cloudflare proxy (orange → gray cloud)
- [ ] Verify Caddy obtains SSL cert after DNS fix
- [ ] Test auth on Android after HTTPS is working

### Pending (Automation)
- [ ] Create automated deployment pipeline (GitHub Actions or shell script)
- [ ] Automate: code push → server pull → docker rebuild → APK build → APK deploy

### Future
- [ ] Handle NAT hairpinning for local network testing
- [ ] Add configurable server URL in app settings (for self-hosted flexibility)
- [ ] Set up Expo Updates (OTA) for JS-only changes without full APK rebuild

---

## Quotes Worth Remembering

> "Android's AAPT is strict — if the extension says .png, it better actually be a PNG."

The build failed 5 times before we caught that `penthouse-bg.png` was secretly a JPEG. The `file` command is your friend.

> "NAT hairpinning: your router may not route traffic from your own network back to itself."

When testing from the same WiFi as the server, requests to your public IP might fail. Test from mobile data instead (This is for Aim🎩)

---

## Related Notes
- [[DEPLOYMENT.md]] — Full TrueNAS deployment guide
- [[THE_PENTHOUSE_NATIVE_SPECIFICATION.md]] — App specification
