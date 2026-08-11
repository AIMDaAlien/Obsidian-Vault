---
project: Holo Companion
updated: 2026-08-10
---

# Models, Research, and Privacy

## Current Runtime

- Fast/default model: `prism-ml/bonsai-27b` as LM Studio alias `holo-fast`.
- Context: 16K.
- MTP load flag: enabled where accepted by LM Studio.
- Embedding model: Nomic Embed Text v1.5 as `holo-embed`, 2K context.
- Deliberate lane: optional through `HOLO_DELIBERATE_MODEL`; not selected until benchmark approval.
- API bind: `127.0.0.1:1234`.

The old Holo-tuned Qwen3.6-35B-A3B MXFP4 path is documented but the local weights are currently absent.

## Model Selection Candidates

- Qwen3.6-35B-A3B Q2 MLX plus compatible MTP drafter.
- Holo-tuned Qwen3.6-35B-A3B MXFP4.
- Qwen3.6-35B-A3B OptiQ 4-bit MTP.
- Bonsai 27B 2-bit.
- Official Qwen3.6-27B 4-bit.

Selection requires measured warm first-token latency, decode speed, structured-output reliability, memory pressure, prompt-copying resistance, long-form coherence, coaching quality, creative constraint-following, and source faithfulness.

References:

- [Qwen3.6-35B-A3B model card](https://huggingface.co/Qwen/Qwen3.6-35B-A3B/blob/main/README.md)
- [MLX MTP drafter](https://huggingface.co/mlx-community/Qwen3.6-35B-A3B-MTP-bf16/blob/main/README.md)
- [LM Studio Responses API](https://lmstudio.ai/docs/developer/openai-compat/responses)
- [LM Studio structured output](https://beta.lmstudio.ai/docs/developer/openai-compat/structured-output)

## Qualitative Research Agent

Research is not a single search-summary call. The implemented harness performs:

1. A sanitized initial query.
2. SearXNG search and public-page retrieval.
3. An evidence ledger with source title, URL, snippet, and bounded excerpt.
4. A local-model gap evaluation covering credibility, missing evidence, and disagreement.
5. Up to two follow-up rounds.
6. A cited local synthesis with a deterministic source appendix.

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
- HTML search works, so Holo now falls back to native SearXNG HTML parsing.

## Outbound Privacy Boundary

Allowed to leave the LAN during research:

- Minimal search queries.
- Requested public URLs, normal HTTP headers, and the public IP seen by those websites.

Never intentionally sent to search engines or fetched websites:

- Holo memories or raw transcript history.
- Screenshots or OCR dumps.
- Local filesystem paths.
- LAN addresses.
- Unrelated personal context.

Search-query sanitization removes local paths and LAN addresses. A result fetch also rejects private network targets to prevent SearXNG results from becoming an SSRF path.

