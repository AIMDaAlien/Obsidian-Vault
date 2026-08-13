# 2026-08-12 Session Continuation

> Short handoff note. Too many compactions this session, this is where we left off.

## What we did today

- Docker vdisk on Unraid: 35G → 56G (was 92% full, now 58%). Trick: loop device had a hard sizelimit, needed losetup --set-capacity + umount stale /var/lib/docker + offline btrfs resize.
- DDR4 OC: not possible outside BIOS. Intel MCH locks clocks at POST. Sticks are JEDEC 3200, no XMP. Dead end, dont revisit.
- Time Machine: root cause was shareVolsizelimit=3GB on the TimeMachine share (SMB reported disk full). Removed. Corrupt 992GB sparsebundle deleted (empty APFS inside, orphaned bands). Share re-exported with fruit support. New bundle created but TM destination is half-broken - NEEDS sudo:
  - sudo tmutil removedestination 7FC40668-1426-4DAC-99F5-E3775B001B28
  - sudo tmutil setdestination -a "smb://guest@192.168.0.120/TimeMachine"
- Mac storage: freed ~42GB (83GB free now). Deleted Draw Things container 41G, Windows 11 Parallels VM 37G, Android SDK 10G, strays. 12 TM exclusions added (HF cache, LM Studio, flux2, caches, Downloads, etc - all re-downloadable).
- tm-prune.sh written (~/.hermes/scripts/) but NOT wired to cron yet - does age (5wk) + size (1.2TB) pruning.

## Nemotron 3.5 Lightning 30B A3B - deployed, benched, REMOVED

- Deployed on Unraid port 18006 via rebuilt laguna image from UPSTREAM llama.cpp master (poolside laguna branch was stale, "wrong number of tensors 417 vs 408"). RTX 3060, Q4_K_M 25.5GB + MTP drafter.
- Bench results vs Qwen: 130-question easy battery ~tied, 17-question hard agentic tied 16/17 (both fell for chmod 100 vs 700 trap + tool-selection preference for run_command over read_file).
- User verdict: no clear differences -> REMOVED. 26GB freed. Roster + compose clean. Rebuilt laguna image stays (Qwen runs on it).
- Runtime quirk: intermittent HTTP 500 "peg-native format" - harness needs retry (added).

## Benchmark suite - the real deliverable

- fingerprint-bench.py + bank_1..8.py = 317 questions, 28 domains, deterministic grading, retry-capable.
- Domains: history, geography, science, recent, math, ling, pop, sports, food, medicine, tech, biz, lang (30 langs), niche, trap, obscure, esoteric, rare, region, food2, geo2, tech2, homelab, security, islam, math2, multihop.
- Qwen baseline: 305/317 raw (96.2%), ~311/317 effective (98%). Perfect on obscure science, esoteric history, rare trivia, islam, homelab, math2, multihop, security.
- Qwen outputs native script (감사합니다, Вода) - grader artifact, actually stronger multilingual.
- Genuine Qwen misses: Unraid version (says 6.14), Seven Sisters (Conoco), HTTP idempotent (PUT - arguable).
- Usage: python3 fingerprint-bench.py <qwen|nemotron|...> - run any future model against this battery.

## Pending / next

1. TM sudo re-register (user's hands, needs password)
2. tm-prune.sh -> weekly cron
3. Dotslash cache 258M needs sudo (SIP-locked)
4. Mac-local roster: Gemma 4 26B A4B QAT still the flagship (hgemma-local :8110, 262144 ctx, TurboQuant v4 + int4 KV, ~61 tps). LFM2.5-8B for interactive loops. Bonsai/Maple/LFM2.6B verdicts lost to compaction - dont re-litigate, they're not in use.
5. Unraid roster: nanbeige + qwen36-terminal only (nemotron gone)
6. Deepwen-3.6 dir on Unraid still uninspected (carried from before)
7. Qwen UD-Q6_K 29GB + DFlash 421MB stale on Unraid disk - awaiting user OK to delete
8. Next benchmark candidate if user wants: Mistral Small 3.2 24B (13.3GB 4bit) or Gemma 4 E2B - both fit Mac, fingerprint-bench.py ready
