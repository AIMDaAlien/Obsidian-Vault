---
type: documentation
topic: Browser Debloat & Benchmark 2026-09-19
category: Omarchy & Desktop
tags: [browsers, debloat, benchmark]
publish: true
created: 2026-09-23
machine: bigrig
title: "Browser Debloat & Benchmark — 2026-09-19"
---
# Browser Debloat & Benchmark — 2026-09-19

**Category:** [[Omarchy & Desktop]] · **Vault:** [[Vault Map]]

Goal: cut RAM/resource usage from the browsers on MASSIVE-RIG and compare the three installed
ones. Big honest finding first: **you cannot debloat stock browser binaries** — Chromium/Firefox
ship prebuilt with millions of lines C++; the "bloat" lives inside the binary and can't be
stripped without rebuilding from source. Real RAM levers are config: killing renderer processes,
disabling background networking, and the profiling stack. Swap the package, don't strip the code.

## Installed browsers (Sep 2026)
- chromium 152 — `/usr/bin/chromium` (plain ELF, NOT a wrapper script)
- helium-browser 0.17.0.1 — Chromium 153 fork at `/opt/helium-browser-bin/` (ships its own chrome +
  chromedriver)
- zen-browser 1.22.1b — Firefox fork at `/opt/zen-browser-bin/zen-bin`

## DeepSeek harness — no browser needed
LiveCodeBench's `deepseek_runner.py` is pure HTTP (openai client → `api.deepseek.com`). Zero
playwright/selenium/chromium imports anywhere in the harness. Never depended on Chrome.

## Omarchy-specific gotcha (page this again)
`/usr/bin/chromium` is an ELF, so the flags it honors live in **`~/.config/chromium-flags.conf`**
(written by the omarchy install script at `~/.config/chromium-flags.conf`, NOT the stock
`~/.config/chromium/chrome-flags.conf`). Omarchy also injects wayland ozone + its own extensions
via this same file. Helium reads `~/.config/helium-browser-flags.conf`. My first flag drop in the
wrong path silently did nothing — verify the live process argv (`tr '\0' ' ' < /proc/PID/cmdline`)
rather than trusting the path.

## Chromium debloat (applied + verified)
`~/.config/chromium-flags.conf` (base = omarchy wayland/extensions, appended):
```
--disable-component-update
--disable-component-extensions-with-background-pages
--disable-background-networking
--disable-sync
--no-pings
--no-first-run
--disable-features=Translate,MediaRouter,ReadLater,Coupons,PrivacySandboxSettings4
--renderer-process-limit=4   <- the real RAM lever: caps renderer procs
```
Managed policy `~/.config/chromium/policies/managed/debloat.json`: kill translate, media router,
promotions, metrics reporting, sync, autofill (address+credit card), search suggestions; harden
DoH=automatic. Verified: valid JSON, per-user path, all keys present in the binary; flags confirmed
in live `cmdline`. Launch tested clean (exit 0, no crash). NOTE: window `--user-data-dir` relocates
config dir so policies aren't read there — test against the real `~/.config/chromium/`.

Tradeoffs: SyncDisabled blocks sign-in/sync; SearchSuggestEnabled:false kills URL-bar suggestions.

## Zen (Firefox) resource tuning
`~/.config/zen/jk7sr7hf.Default (release)/user.js` (applies every startup, remove file to revert):
- `dom.ipc.processCount=3`, extension=1, `processPrelaunch.enabled=false` (big lever — default
  scaled to 13 renderer procs)
- lazy tab restore on demand; `browser.tabs.unloadOnLowMemory=true` (discard bg tabs under pressure)
- session history 25 entries/tab; session backup 2min; mem cache 32MB cap, disk 256MB
- all speculative networking off: prefetch-next, dns.disablePrefetch, predictor, speculative-
  parallel-limit 0, urlbar.speculativeConnect
- media autoplay blocked; media cache 512KB; built-in screenshot off
- prefs validated against real omni.ja source (TabUnloader/UrlbarPrefs.sys.mjs), not just binary strings

## Benchmark results (real binaries, headless, Selenium WebDriver, 3 pages: Wikipedia+GitHub+HN)
```
        peak RSS    final RSS    processes
chromium  2027 MB     2027 MB      13
helium    2070 MB     2070 MB      13
zen       1973 MB     1973 MB      15
```
All three within 5% ≈ 2GB for 3 real pages (same two engines). Caveats: headless+fresh profile
(no extensions/history/cache); real many-tab sessions run higher and the renderer cap's win shows
under many tabs, not 3; renderer cap = mild sandbox tradeoff (bad site shares its process with
neighbors).

## Verdict: Helium is redundant
Helium = Chromium 153 fork with a privacy/anti-tracking wrapper. No functional gain over the
installed Chromium 152, and it's a step behind on automation tooling (Playwright/Puppeteer target
upstream Chromium first). Recommendation: drop Helium, keep Zen (daily) + Chromium (agent work).

## Tooling notes (for future benches)
- Playwright's driver can't talk to real Zen (its Firefox driver needs juggler, real builds don't
  have it). Use **Selenium WebDriver** for real-binary benchmarks: geckodriver for Firefox/Zen,
  chromedriver for Chromium (Helium ships its own).
- Installed: `/tmp/benchvenv` (selenium 4.49, playwright), geckodriver 0.37.1 → `~/.local/bin/geckodriver`.
- Scripts: `/tmp/bench_browsers.py` (playwright, broken — Browser.process removed), `/tmp/bench_selenium.py` (working).
- Full-tree RSS measured via `/proc/PID/status` VmRSS summed down `pgrep -P` children.

## Open items
- [ ] uninstall helium-browser-bin (redundant)
- [ ] optional: many-tab soak to show renderer cap reducing process count
- [ ] Zen changes apply on restart (old process farm lingers until then)

## Related

- Same OS discipline: [[Omarchy Trim Debloat & Idle Policy]] · [[Omarchy Plugins & Shell Widgets]]
- Why browsers matter here: agents drive Chromium headless — see [[Agents & Tooling]]
