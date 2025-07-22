"""ReasonBot Utility Functions

Includes helpers for caching, rate-limiting, text cleaning, environment handling,
and error resilience. Shared tools across all modules.
"""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Set

__all__ = [
    "get_env_var",
    "is_rate_limited",
    "load_processed_ids",
    "save_processed_id",
]


def get_env_var(name: str, default: str | None = None) -> str | None:
    """Return an environment variable with a fallback.

    Parameters
    ----------
    name:
        Name of the environment variable.
    default:
        Value returned if the variable is not set.

    Returns
    -------
    str | None
        The environment variable or ``default`` if missing.
    """

    value = os.getenv(name)
    return value if value is not None else default


def is_rate_limited(lock_file: Path, cooldown: int) -> bool:
    """Simple file-based rate limiter.

    The function stores the timestamp of the last successful action in a lock
    file. If the next call occurs before ``cooldown`` seconds have passed, it
    returns ``True`` without updating the timestamp.

    Parameters
    ----------
    lock_file:
        File path used to store the timestamp.
    cooldown:
        Number of seconds that must elapse between calls.

    Returns
    -------
    bool
        ``True`` if the caller must wait, ``False`` otherwise.
    """

    now = time.time()
    try:
        if lock_file.exists():
            last = float(lock_file.read_text())
            if now - last < cooldown:
                return True
    except Exception:
        # Corrupted or unreadable file -> ignore and regenerate
        pass

    try:
        lock_file.write_text(str(now))
    except Exception:
        # Don't crash if the timestamp cannot be written
        pass
    return False


def load_processed_ids(path: Path) -> Set[str]:
    """Load a set of processed tweet IDs from ``path``."""

    if not path.exists():
        return set()
    try:
        return {line.strip() for line in path.read_text().splitlines() if line.strip()}
    except Exception:
        return set()


def save_processed_id(path: Path, tweet_id: str) -> None:
    """Append ``tweet_id`` to the cache file at ``path``."""

    try:
        with path.open("a", encoding="utf-8") as fh:
            fh.write(f"{tweet_id}\n")
    except Exception:
        pass
