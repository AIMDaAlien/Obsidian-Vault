"""Compose one published vault from several source vaults."""


class ComposeError(Exception):
    """A compose run must stop; the message says why."""
