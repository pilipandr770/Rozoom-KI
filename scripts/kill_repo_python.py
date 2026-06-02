import os
from pathlib import Path

import psutil

repo = str(Path(__file__).resolve().parents[1])
for p in psutil.process_iter(['pid','name','exe']):
    try:
        exe = p.info['exe'] or ''
        if exe and repo.lower() in exe.lower():
            print('killing', p.info['pid'], exe)
            p.terminate()
    except Exception:
        pass
print('done')
