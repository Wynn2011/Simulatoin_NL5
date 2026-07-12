"""Step 7 verification: NL5_Pause then NL5_Stop (ensure simulation stops)

Goal:
- NL5_Stop previously did not stop simulation (IsRunning remained 1).
- Retry with correct sequence: Pause -> Stop -> poll until IsRunning first field becomes 0.

Stability rule:
- Only assert on NL5_IsRunning first CSV field.

Polling:
- poll_interval_sec = 0.5
- max_wait_sec = 15
"""

from __future__ import annotations

import time
import requests

BASE = "http://172.30.48.1"
TIMEOUT = 30
THROTTLE_SEC = 0.2

POLL_INTERVAL_SEC = 0.5
MAX_WAIT_SEC = 15


def http_get(query: str) -> tuple[int, str, str]:
    url = f"{BASE}/{query.lstrip('/')}"
    r = requests.get(url, timeout=TIMEOUT)
    return r.status_code, r.text.strip(), url


def isrunning_first_field(body: str) -> str:
    # expected CSV like "1,xxx" or "0,yyy". We only take the first field.
    return (body.split(",", 1)[0] if body else "").strip()


def main() -> None:
    sc, body, url = http_get("?NL5_IsRunning")
    print("NL5_IsRunning (before Pause):", body)

    time.sleep(THROTTLE_SEC)

    sc, body, url = http_get("?NL5_Pause")
    print("NL5_Pause:", body)

    time.sleep(THROTTLE_SEC)

    sc, body, url = http_get("?NL5_Stop")
    print("NL5_Stop:", body)

    # Poll until first field becomes 0 or timeout.
    deadline = time.time() + MAX_WAIT_SEC
    last_body = None
    while time.time() < deadline:
        sc, body, url = http_get("?NL5_IsRunning")
        last_body = body
        first = isrunning_first_field(body)
        print("poll IsRunning:", body)
        if first == "0":
            print("Detected IsRunning=0 => simulation stopped")
            return
        time.sleep(POLL_INTERVAL_SEC)

    raise AssertionError(f"Timeout waiting for NL5_IsRunning first field to become 0. Last body: {last_body!r}")


if __name__ == "__main__":
    main()
