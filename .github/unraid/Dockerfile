FROM ghcr.io/astral-sh/uv:python3.12-bookworm

RUN apt-get update \
    && apt-get install -y --no-install-recommends git openssh-client \
    && rm -rf /var/lib/apt/lists/*

RUN uv pip install --system pyyaml

RUN git config --system safe.directory '*'

WORKDIR /vault/published
ENTRYPOINT ["python", "/vault/published/.github/scripts/compose.py"]
