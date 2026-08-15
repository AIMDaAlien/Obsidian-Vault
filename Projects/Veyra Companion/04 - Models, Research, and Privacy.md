---
project: Veyra Companion
updated: 2026-08-15
---

# Models, Research, and Privacy

## Current Runtime

- Fast/default model: `LiquidAI/LFM2.5-VL-3B-MLX-4bit` on `127.0.0.1:8112`.
- Deliberate lane: `qwen3.8-27b-4bit` on `127.0.0.1:8110`.
- Embedding model: Nomic Embed Text v1.5 as `veyra-embed` on LM Studio `127.0.0.1:1234`.
- Qwen3.5-4B and Bonsai are removed from the runtime.
- Conversation model allowlisting is split by lane: fast permits only `lfm2.5-vl-3b` and deliberate permits only `qwen3.8-27b`; Heretic and legacy Qwen remain blocked.
- `VEYRA_FAST_MODEL` and `VEYRA_DELIBERATE_MODEL` are honored only when they pass their lane-specific allowlists.

## Routing Rules

| Mode | Model | Endpoint | Context |
|---|---|---|---|
| Brief, normal, proactive | LFM2.5-VL-3B | `127.0.0.1:8112` | 32K |
| Deep, creative, research | Qwen3.8-27B | `127.0.0.1:8110` | 32K |
| Embeddings | `veyra-embed` | `127.0.0.1:1234` | 2K |

Visual awareness is a separate LFM2.5-VL-3B call: a downscaled local frame becomes a concise factual text description in `awarenessContext`. Qwen3.8 never receives the image.

## Small-Model Replacement Resolved

LFM2.5-VL-3B is the new fast/vision model, not an interim placeholder. It replaced Qwen3.5-4B after passing the multilingual short-reply and screenshot audition.

The prior shortlist is closed. Qwen3.5-4B remains cached on disk for rollback only and is no longer a valid runtime conversation model.

## Qualitative Research Agent

Research is not a single search-summary call. The implemented harness performs:

1. A sanitized initial query.
2. SearXNG search and public-page retrieval.
3. An evidence ledger with source title, URL, snippet, and bounded excerpt.
4. A Qwen3.8 gap evaluation covering credibility, missing evidence, and disagreement.
5. Up to two follow-up rounds.
6. A cited local synthesis with a deterministic source appendix.

Before research begins, Veyra shows a non-blocking warning: “Close heavy apps before research.”

Limits:

- At most three rounds.
- At most three queries per round.
- At most eight sources total.
- Five-megabyte fetch ceiling per page.
- Public HTTP/HTTPS only; loopback, LAN, link-local, and `.local` result URLs are rejected.
- JavaScript-only and inaccessible pages may provide only their SearXNG snippet.

## SearXNG

Order:

1. `http://127.0.0.1:8082`
2. `http://192.168.0.120:8082`

Observed on 2026-08-10:

- Local endpoint unavailable.
- Unraid endpoint returns HTTP 200.
- Unraid JSON search returns HTTP 403 because JSON output is disabled.
- HTML search works, so Veyra now falls back to native SearXNG HTML parsing.

## Outbound Privacy Boundary

Allowed to leave the LAN during research:

- Minimal search queries.
- Requested public URLs, normal HTTP headers, and the public IP seen by those websites.

Never intentionally sent to search engines or fetched websites:

- Veyra memories or raw transcript history.
- Raw screen frames or local visual descriptions.
- Local filesystem paths.
- LAN addresses.
- Unrelated personal context.

Screen frames remain in memory and are only read locally by LFM2.5-VL-3B. They are never persisted by Veyra and never sent to the external Qwen3.8 service or to the internet.

Search-query sanitization removes local paths and LAN addresses. A result fetch also rejects private network targets to prevent SearXNG results from becoming an SSRF path.
