# 2026-06-27 Home Lab Restoration & Expansion

## what happened

the docker image resize failed and wiped all containers. rebuilt everything from scratch.

## docker recovery

- original 20GB image was 83% full with 3.4GB free
- attempted btrfs resize to 40GB -- failed, loopback device didnt pick up new size
- attempted directory mode -- unraid doesnt create docker storage that way
- solution: unraid gui Settings -> Docker -> disable -> delete vdisk -> re-enable, set 35GB
- reinstalled all 13 containers from templates + docker run commands + compose files

## what changed

- **cloudreve removed** -- wrong tool for browsing syncthing files. replaced with **FileBrowser** (port 8083)
- **homepage dashboard added** (port 3000) -- all services listed with icons, SearXNG as search widget
- **searxng installed** (port 8082) -- private metasearch engine for all devices
- **tailscale installed** via docker, needs OAuth at login.tailscale.com/a/1ff883870177b5
- docker image size: 35GB, clean

## what stayed the same

- all 13 containers restored successfully
- home assistant automations loaded from appdata
- immich with RTX 3060 CUDA ML working
- penthouse from audit/backend-trim-performance, api healthy
- syncthing syncing m5Pro documents + downloads, ~33GB transferred
- qbittorrent incomplete in RAM (64GB tmpfs), completed on downloads pool

## parity check

- still running as of 2026-06-27 evening
- ~59% complete, slows array writes significantly
- syncthing running at low kbps until parity check finishes

## pi-hole

- at 192.168.0.145
- unbound was configured during a previous session
- ssh password auth might be disabled -- needs hdmi cord to check

## brave / arc search engine

- brave docs say "index other search engines" setting exists under brave://settings/search
- user reports it doesnt appear in their version
- arc browser doesnt support custom search engines at all
- workaround: set searxng as browser homepage or use keyword search

## remaining todo

- [ ] lsi bios staggered spin-up for sas drives
- [ ] parity check finish then full-speed syncthing
- [ ] pi-hole ssh fix (hdmi cord)
- [ ] deploy m80q (uptime kuma + penthouse fallback)
- [ ] deploy rpi b+ (ntp + ping watchdog)
- [ ] off-box backups (m80q or mac rsync)
- [ ] tailscale auth & phone install
- [ ] syncthing auto-accept config for bigrig and m4air
- [ ] time machine test from mac
- [ ] searxng theming (settings.yml)
