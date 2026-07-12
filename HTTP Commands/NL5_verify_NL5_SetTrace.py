"""Step 18 verification: NL5_SetTrace

Objective:
  Set the color of the trace at index 0 to red.

Command template from doc:
  http://localhost/?NL5_SetTrace,0,color=red

This script sends the NL5 HTTP command to your Hermes-reachable host.
No hard assertions; prints response.
"""

from __future__ import annotations

import time, requests

BASE = "http://172.30.48.1"
TIMEOUT = 60
THROTTLE_SEC = 0.2

def http_get(path_query: str) -> tuple[int, str, str]:
    # path_query example: '/?NL5_GetInfo' or '?NL5_GetInfo'
    if path_query.startswith('http'):
        url = path_query
    else:
        url = BASE + '/' + path_query.lstrip('/')
    r = requests.get(url, timeout=TIMEOUT)
    return r.status_code, r.text.strip(), url

def main() -> None:
    # Optional: show sim status if available
    try:
        sc, body, url = http_get('?NL5_IsRunning')
        print('NL5_IsRunning: status=', sc, 'body=', body)
    except Exception as e:
        print('[info] NL5_IsRunning check failed:', e)

    time.sleep(THROTTLE_SEC)

    # Send command
    cmd = "http://localhost/?NL5_SetTrace,0,color=red"
    # cmd is like 'http://localhost/?NL5_Foo,...'
    path_query = cmd.split('?',1)[1] if '?' in cmd else cmd
    full_path_query='?' + path_query
    sc, body, url = http_get(full_path_query)
    print('NL5_SetTrace:')
    print('  url:', url)
    print('  status:', sc)
    print('  body:', body)

if __name__ == '__main__':
    main()
