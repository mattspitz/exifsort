import os
import shutil
import sys

# Simple script to rename files like: PANO_20120526_152013.jpg

FAILED_DIR = "."

def main():
    for fn in sys.argv[1:]:
        root, ext = os.path.splitext(os.path.basename(fn))

        _, date, time_of_day = root.split("_")

        assert len(date) == 8
        year, month, day = int(date[:4]), int(date[4:6]), int(date[6:])

        assert len(time_of_day) == 6
        hour, minute, second = int(time_of_day[:2]), int(time_of_day[2:4]), int(time_of_day[4:])

        new_root = "{:04d}-{:02d}-{:02d} {:02d}.{:02d}.{:02d}".format(
            year, month, day, hour, minute, second)

        new_fn = os.path.join(FAILED_DIR, new_root + ext)
        print fn, new_fn
        if os.path.exists(new_fn):
            raise Exception("TODO: deal with this")
        shutil.copy2(fn, new_fn)

if __name__ == "__main__":
    main()
