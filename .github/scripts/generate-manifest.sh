#!/usr/bin/env bash
# generate-manifest.sh
# Delegates to Python for robust JSON generation
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
python3 "$REPO_ROOT/.github/scripts/generate-manifest.py" "$REPO_ROOT"
