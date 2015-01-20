import os
import shutil
import sys
import time

# Simple script to rename files that are just named with unix timestamps, e.g. 1234567890.jpg

FAILED_DIR = "failed"

def main():
    for fn in sys.argv[1:]:
        root, ext = os.path.splitext(os.path.basename(fn))
        t = time.gmtime(int(root) / 1000.0)
        new_root = time.strftime("%Y-%m-%d %H.%M.%S", t)

        new_fn = new_root + ext
        print fn, new_fn
        if os.path.exists(new_fn):
            raise Exception("TODO: deal with this")
        shutil.copy2(fn, new_fn)

if __name__ == "__main__":
    main()
