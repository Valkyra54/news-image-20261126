#!/usr/bin/env python3
"""Entry point for THE THURSDAY GAZETTE (news-image-20261126).

Stdlib only: validates the pre-rendered entry.png and copies it to
$MAKEFUN_OUTPUT_DIR (default /output). The grader has no Pillow, so this
file must never import it. Never deletes the output directory itself.
"""
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
PNG_SIG = b"\x89PNG\r\n\x1a\n"


def fail(msg):
    sys.stderr.write("error: %s\n" % msg)
    return 1


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        with open(SRC, "rb") as f:
            data = f.read()
    except OSError as e:
        return fail("cannot read entry.png: %s" % e)
    if len(data) > 1024 * 1024:
        return fail("entry.png exceeds 1 MiB (%d bytes)" % len(data))
    if not data.startswith(PNG_SIG):
        return fail("entry.png is not a PNG")
    if len(data) < 33 or data[12:16] != b"IHDR":
        return fail("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if width > 1024 or height > 1024:
        return fail("entry.png is %dx%d, over the 1024x1024 cap" % (width, height))
    if data[24] != 8:
        return fail("entry.png bit depth is %d, expected 8" % data[24])
    if not data.endswith(b"IEND\xaeB`\x82"):
        return fail("entry.png has no IEND tail")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SRC, os.path.join(out_dir, "entry.png"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
