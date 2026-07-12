"""NL5 HTTP command helpers for Hermes.

This module provides:
- NL5_URL builder for your Hermes-reachable host (default confirmed: 172.30.48.1)
- A single generic `nl5_cmd()` that sends one NL5 HTTP command (sequential, no concurrency)
- Convenience wrappers for the most common no-arg commands (NL5_GetInfo, NL5_New, ...)

For commands that need parameters, use `nl5_cmd('<COMMAND>', 'arg1', 'arg2', ...)`.

Command URL format (from NL5 HTTP examples):
  http://<HOST>/?<COMMAND>[,<arg1>[,<arg2>...]]
"""

from __future__ import annotations

import time
from typing import Optional

import requests


BASE = "http://172.30.48.1"  # Hermes-reachable address (confirmed working)
DEFAULT_TIMEOUT_SEC = 30
DEFAULT_THROTTLE_SEC = 0.2


def build_url(command: str, *params: str) -> str:
    # command must look like NL5_GetInfo / NL5_New / etc.
    if params:
        query = command + "," + ",".join(str(p) for p in params)
    else:
        query = command
    return f"{BASE}/?{query}"


def nl5_cmd(command: str, *params: str, timeout_sec: int = DEFAULT_TIMEOUT_SEC) -> str:
    """Send one NL5 HTTP command and return response text."""
    url = build_url(command, *params)
    r = requests.get(url, timeout=timeout_sec)
    # NOTE: keep this sequential; caller should manage ordering.
    return r.text


def nl5_getinfo() -> str:
    return nl5_cmd("NL5_GetInfo")


def nl5_new() -> str:
    return nl5_cmd("NL5_New")


def nl5_isrunning() -> str:
    return nl5_cmd("NL5_IsRunning")


def nl5_start(*, step: Optional[str] = None) -> str:
    # Example from docs: NL5_Start,step=1u
    if step is None:
        return nl5_cmd("NL5_Start")
    return nl5_cmd("NL5_Start", f"step={step}")


def nl5_pause() -> str:
    return nl5_cmd("NL5_Pause")


def nl5_continue(*, screen: Optional[str] = None) -> str:
    # Example: NL5_Continue,screen=0.2
    if screen is None:
        return nl5_cmd("NL5_Continue")
    return nl5_cmd("NL5_Continue", f"screen={screen}")


def nl5_wait_between_requests(throttle_sec: float = DEFAULT_THROTTLE_SEC) -> None:
    time.sleep(throttle_sec)
