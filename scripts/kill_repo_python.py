import psutil,os
repo = r'C:\Users\\' + os.getlogin() + '\\Rozoom-KI'
for p in psutil.process_iter(['pid','name','exe']):
    try:
        exe = p.info['exe'] or ''
        if exe and repo.lower() in exe.lower():
            print('killing', p.info['pid'], exe)
            p.terminate()
    except Exception:
        pass
print('done')
