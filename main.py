#!/usr/bin/env python3
"""news-image-20261119 entry: place the finished front-page image at the
grader's output path. Standard library only, fully deterministic.

The image is drawn ahead of time by make_image.py and shipped as entry.png
beside this file; this program only copies those exact bytes, so every run
writes an identical file.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DST = os.path.join(OUT_DIR, "entry.png")


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if not os.path.isfile(SRC):
        print("entry.png missing beside main.py", file=sys.stderr)
        return 1
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, DST)
    if digest(SRC) != digest(DST):
        print("copy verification failed", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
