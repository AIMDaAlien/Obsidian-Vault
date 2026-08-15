---
project: Veyra Companion
updated: 2026-08-15
---

# Models, Research, and Privacy

## Current Runtime

- Fast/default model: `mlx-community/Qwen3.5-4B-MLX-4bit` on `127.0.0.1:8112`.
- Deliberate lane: `qwen3.8-27b-4bit` on `127.0.0.1:8110`.
- Embedding model: Nomic Embed Text v1.5 as `veyra-embed` on LM Studio `127.0.0.1:1234`.
- Bonsai is removed from the runtime.
- Conversation model allowlisting permits only the intended Qwen3.5-4B and Qwen3.8-27B runtime IDs; Heretic and legacy Qwen remain blocked.
- `VEYRA_FAST_MODEL` and `VEYRA_DELIBERATE_MODEL` are honored only when they pass the allowlist.

## Routing Rules

| Mode | Model | Endpoint | Context |
|---|---|---|---|
| Brief, normal, proactive | Qwen3.5-4B | `127.0.0.1:8112` | 16K |
| Deep, creative, research | Qwen3.8-27B | `127.0.0.1:8110` | 32K |
| Embeddings | `veyra-embed` | `127.0.0.1:1234` | 2K |

Visual awareness is a separate Qwen3.5-4B call: a downscaled local frame becomes a concise factual text description in `awarenessContext`. Qwen3.8 never receives the image.

## Small-Model Replacement Shortlist

Qwen3.5-4B is the interim fast model until a replacement passes live multilingual conversation testing.

Known MLX candidates under roughly 4 GB:

| Candidate | Resident size | Notes |
|---|---|---|
| `mlx-community/Qwen3.5-4B-MLX-4bit` | ~2.9 GB | Multimodal; current interim; verified for brief/normal and visual description |
| `mlx-community/Ministral-3-3B-Instruct-2512-4bit` | ~2.6 GB | Next multilingual short-reply candidate |
| `mlx-community/LFM2.5-1.2B-Instruct-4bit` | small | Public MLX-community candidate; reports English, Arabic, Japanese, and other language support |
| `mlx-community/granite-4.1-3b-4bit` | ~2.0 GB | Lower confidence for Arabic and Japanese naturalness |

Recommended ranking:

1. Qwen3.5-4B first because it is multimodal and already verified.
2. Ministral or LFM2.5 as the next audition candidates.
3. Granite lower priority until Arabic/Japanese short-reply quality is shown.

Rank by multilingual naturalness, resident size, MLX support, and time-to-first-token. Keep Qwen3.5-4B as interim until a replacement passes live conversation testing.

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

Screen frames remain in memory and are only read locally by Qwen3.5-4B. They are never persisted by Veyra and never sent to the external Qwen3.8 service or to the internet.

Search-query sanitization removes local paths and LAN addresses. A result fetch also rejects private network targets to prevent SearXNG results from becoming an SSRF path.
