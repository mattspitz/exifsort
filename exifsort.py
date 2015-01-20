import argparse
import datetime
import os
import shutil

import exiftool

# Initial script that renames files based on exif data.

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir")
    return parser.parse_args()

FAILED_DIR = "failed"
PROCESSED_DIR = "processed"

def handle_metadata(metadata):
    for m in metadata:
        fn = m["SourceFile"]
        if "EXIF:DateTimeOriginal" in m:
            date_str = m["EXIF:DateTimeOriginal"]
        elif "QuickTime:CreateDate" in m:
            date_str = m["QuickTime:CreateDate"]
        else:
            new_fn = os.path.join(FAILED_DIR, os.path.basename(fn))
            print fn, new_fn
            shutil.copy2(fn, new_fn)
            continue

        date = datetime.datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")

        _, ext = os.path.splitext(fn)
        new_root = date.strftime("%Y-%m-%d %H.%M.%S")
        inc = 0

        while True:
            inc_part = "" if inc < 1 else "_{}".format(inc)

            new_fn = os.path.join(PROCESSED_DIR, new_root + inc_part + ext)
            if not os.path.exists(new_fn):
                break
            inc += 1

        print fn, new_fn
        shutil.copy2(fn, new_fn)

def main():
    args = parse_args()

    for dirpath, _, filenames in os.walk(args.input_dir):
        BATCH_SIZE = 50
        for i in xrange(0, len(filenames), BATCH_SIZE):
            relative_filenames = [ os.path.join(dirpath, fn) for fn in filenames[i:i+BATCH_SIZE] ]

            with exiftool.ExifTool() as et:
                metadata = et.get_metadata_batch(relative_filenames)

            handle_metadata(metadata)

if __name__ == "__main__":
    main()
