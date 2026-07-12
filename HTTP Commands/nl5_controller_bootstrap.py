"""NL5 HTTP bootstrap + first command runner.

What it does:
1) Launch NL5.exe with the -http switch (opens default blank document).
2) Poll readiness by calling NL5_GetInfo every 20 seconds until it returns 0,Version...
3) Send the first control command NL5_New (no additional args).

You can import this module or run it directly.

Note about networking:
Your NL5 HTTP server is reachable from Hermes via:
  http://172.30.48.1/?NL5_GetInfo
(not necessarily WSL localhost).
"""

from __future__ import annotations

import subprocess
import time
from typing import Optional

import requests


NL5_EXE = r"C:\Users\wynnl\Mains\Personal\AI_projects\Hermes_Projects\Project_NL5_auto\NL5-V4.3\NL5.exe"

# Hermes-reachable address (confirmed working in your environment)
BASE = "http://172.30.48.1"
GETINFO_URL = f"{BASE}/?NL5_GetInfo"

# First command you requested
NEW_URL = f"{BASE}/?NL5_New"

# Polling cadence
POLL_INTERVAL_SEC = 20


def launch_nl5_with_http(exe_path: str = NL5_EXE) -> subprocess.Popen:
    # Launch in the NL5-V4.3 working directory to reduce any temp/config surprises.
    workdir = r"C:\Users\wynnl\Mains\Personal\AI_projects\Hermes_Projects\Project_NL5_auto\NL5-V4.3"
    print("[NL5] Launching:", exe_path, "with -http")
    p = subprocess.Popen([exe_path, "-http"], cwd=workdir)
    print("[NL5] Launch subprocess pid:", p.pid)
    return p


def wait_until_ready(url: str = GETINFO_URL, max_attempts: Optional[int] = None) -> str:
    """Poll GetInfo until response starts with '0,' and contains 'Version'."""
    attempt = 0
    while True:
        attempt += 1
        try:
            r = requests.get(url, timeout=10)
            text = r.text.strip()
            print(f"[NL5] NL5_GetInfo attempt {attempt}: status={r.status_code} text={text}")
            if text.startswith("0,") and ("Version" in text or "Version" in text):
                return text
        except Exception as e:
            print(f"[NL5] NL5_GetInfo attempt {attempt} failed:", repr(e))

        if max_attempts is not None and attempt >= max_attempts:
            raise TimeoutError(f"NL5 HTTP not ready after {max_attempts} attempts")

        print(f"[NL5] Not ready. Sleeping {POLL_INTERVAL_SEC}s...")
        time.sleep(POLL_INTERVAL_SEC)


def send_command(url: str, timeout_sec: int = 30) -> str:
    print("[NL5] Sending command:", url)
    r = requests.get(url, timeout=timeout_sec)
    print("[NL5] Command status_code:", r.status_code)
    print("[NL5] Command response_text:")
    print(r.text)
    return r.text


def main() -> None:
    # Reuse an existing NL5 instance when possible (avoid multiple servers on port 80).
    # Strategy: try to wait for readiness first; if it times out, then launch.
    try:
        wait_until_ready(GETINFO_URL, max_attempts=2)
        print('[NL5] Reusing existing NL5 instance (HTTP already ready).')
    except Exception:
        launch_nl5_with_http()
        wait_until_ready(GETINFO_URL)

    send_command(NEW_URL)


if __name__ == "__main__":
    main()
