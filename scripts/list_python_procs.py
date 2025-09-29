import psutil
for p in psutil.process_iter(['pid','name','exe']):
    try:
        print(p.info['pid'], p.info['name'], p.info['exe'])
    except Exception:
        pass
