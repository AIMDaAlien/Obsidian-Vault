---
tags: [self-hosting, mobile, updates, versioning, expo]
created: 2026-02-21
published_to_garden: true
visibility: public
---

# Mobile Update and Versioning Protocol (Expo + Self-Hosted APK)

## Goal

A clear update model so users always know when an update's available, what changed, and whether it's optional or forced — with deploys automated from GitHub pushes.

## What I implemented

### 1. APK build and deploy pipeline

On push to `main`, the workflow:
- Builds the Android APK with EAS
- Generates release notes from the commit range
- Publishes the APK to `data/downloads/the-penthouse.apk`
- Writes `data/downloads/app-update.json` with:
  - `latestVersion`
  - `notes`
  - `mandatory`
  - `minSupportedVersion`
  - `checksumSha256`

### 2. OTA pipeline for JS and asset changes

A separate workflow fires on push to `main` when changes touch `mobile/**`. It publishes an OTA update to the EAS `preview` branch using the generated release notes as the OTA message.

### 3. In-app update prompting

The app checks two things on launch:
- The binary update feed at `/api/app/update`
- OTA availability via `expo-updates`

It shows a changelog modal with an "Update now" action, a "Later" option for non-mandatory updates, and a forced update flow when `mandatory=true` or the current version is below `minSupportedVersion`.

## Can you skip the APK reinstall?

Short answer: not fully for binary or native updates.

- Android requires the package installer for new binaries.
- You can update in place (no uninstall, user data preserved) but the user still has to confirm the install.
- OTA updates are the bypass path only for JavaScript and asset changes within the same runtime binary.

## Versioning rules (SemVer)

- `PATCH` (1.2.3 → 1.2.4): bug fixes
- `MINOR` (1.2.3 → 1.3.0): new features, backwards-compatible behavior
- `MAJOR` (1.2.3 → 2.0.0): breaking changes to behavior, protocol, or API

Operational rules:
- Use OTA for JS and asset-only changes that don't need a native rebuild.
- Publish a new APK when native dependencies, config, or runtime compatibility changes.
- Use `mandatory` and `minSupportedVersion` for forced upgrades.

## Expo constraint worth knowing

The config uses `runtimeVersion.policy = appVersion`. This means OTA updates only apply to clients on the exact same app binary version. If you push a new APK, previous OTAs don't transfer.

## Note on the v1 APK path

The v1 era used this Expo-based native APK distribution. The current version of the app has since migrated to a PWA — see [[../The Penthouse/15 - PWA Rebuild]] for why and what changed. The versioning and OTA principles here are still useful reference for any Expo-based project.
