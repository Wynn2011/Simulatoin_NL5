"""Step verification: NL5_Continue

Objective:
  Continue simulation and extend the simulation window duration to 0.2s.

Command template from doc:
  http://localhost/?NL5_Continue,screen=0.2

This script sends the NL5 HTTP command to your Hermes-reachable host.
No hard assertions; prints response.
"""

from __future__ import annotations

import time, requests

BASE = "http://172.30.48.1"
TIMEOUT = 60
THROTTLE_SEC = 0.2


def http_get(path_query: str) -> tuple[int, str, str]:
    url = BASE + '/' + path_query.lstrip('/')
    r = requests.get(url, timeout=TIMEOUT)
    return r.status_code, r.text.strip(), url


def main() -> None:
    time.sleep(THROTTLE_SEC)
    sc, body, url = http_get('?'+"NL5_Continue,screen=0.2".lstrip('?'))
    print("NL5_Continue:")
    print("  url:", url)
    print("  status:", sc)
    print("  body:", body)


if __name__ == '__main__':
    main()
