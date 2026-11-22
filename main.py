"""Entry point: write the 21 November 2026 news image to /output/entry.png.

The picture is rendered by draw.py from fixed data — no network, no clock,
no randomness — then checked against the competition's shape (PNG magic, at
most 1 MiB, at most 1024x1024) and written atomically, so two runs of this
program produce byte-identical files.
"""

import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw import build  # noqa: E402

MAX_BYTES = 1_048_576


def main():
    data = build()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise SystemExit("render did not produce a PNG")
    if len(data) > MAX_BYTES:
        raise SystemExit(f"image too large: {len(data)} bytes")
    width, height = struct.unpack(">II", data[16:24])
    if width > 1024 or height > 1024:
        raise SystemExit(f"image too big: {width}x{height}")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    tmp = target + ".tmp"
    with open(tmp, "wb") as fh:
        fh.write(data)
    os.replace(tmp, target)
    print(f"wrote {target}: {len(data)} bytes, {width}x{height}")


if __name__ == "__main__":
    main()
