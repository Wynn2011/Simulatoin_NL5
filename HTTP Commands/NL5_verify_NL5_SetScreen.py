"""Step verification: NL5_SetScreen

Objective:
  Set waveform window horizontal start time and display span; also supports separate vertical axes.

Command templates from doc:
  http://localhost/?NL5_SetScreen,start=0.1,screen=0.01
  http://localhost/?NL5_SetScreen,separate=on

This script sends both variants sequentially.
No hard assertions; prints response.
"""

from __future__ import annotations

import time
import requests

BASE = "http://172.30.48.1"
TIMEOUT = 60
THROTTLE_SEC = 0.2


def http_get(path_query: str) -> tuple[int, str, str]:
    # path_query should start with '?' like '?NL5_SetScreen,...'
    url = BASE + '/' + path_query.lstrip('/')
    r = requests.get(url, timeout=TIMEOUT)
    return r.status_code, r.text.strip(), url


def main() -> None:
    time.sleep(THROTTLE_SEC)

    tests = [
        '?NL5_SetScreen,start=0.1,screen=0.01',
        '?NL5_SetScreen,separate=on',
    ]

    for t in tests:
        func_url = http_get(t)
        sc, body, url = func_url
        print('NL5_SetScreen:')
        print('  url:', url)
        print('  status:', sc)
        print('  body:', body)
        time.sleep(THROTTLE_SEC)


if __name__ == '__main__':
    main()
