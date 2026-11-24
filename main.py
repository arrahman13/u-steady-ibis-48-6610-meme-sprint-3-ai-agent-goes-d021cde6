#!/usr/bin/env python3
"""Entrypoint for the Meme Sprint 3 entry.

Copies the committed entry.png into the output directory and verifies the
copy against the committed SHA-256. Standard library only. This program
never renders anything: the image was produced at build time by
build_image.py and is committed beside this file as entry.png.
"""

import hashlib
import os
import shutil
import sys

EXPECTED_SHA256 = "9ca6b92b546112147e6ee0134d52f2a33ae97957ca5548887db52880263c424f"


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print(f"entry.png not found beside main.py (looked in {here})",
              file=sys.stderr)
        return 1
    digest = sha256_of(src)
    if digest != EXPECTED_SHA256:
        print(f"entry.png hash mismatch: {digest} != {EXPECTED_SHA256}",
              file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)

    if sha256_of(dst) != EXPECTED_SHA256:
        print("copied entry.png failed verification", file=sys.stderr)
        return 1
    print(f"wrote {dst} ({os.path.getsize(dst)} bytes, sha256 verified)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
