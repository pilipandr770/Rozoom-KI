import ast, traceback, sys
fn = r"c:\Users\ПК\Rozoom-KI\app\commands\seed_blog.py"
try:
    with open(fn, 'r', encoding='utf-8') as f:
        src = f.read()
    ast.parse(src, filename=fn)
    print('PARSE_OK')
except Exception:
    traceback.print_exc()
    # print snippet around error
    try:
        import linecache
        tb = sys.exc_info()[2]
        # get last frame lineno if present
        import traceback as tbmod
        for frame in tbmod.extract_tb(tb):
            lineno = frame.lineno
        if lineno:
            start = max(1, lineno-5)
            for i in range(start, lineno+6):
                print(f"{i:4}: {linecache.getline(fn, i).rstrip()}")
    except Exception:
        pass
