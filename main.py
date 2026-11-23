#!/usr/bin/env python3
"""Entry for news-image-20261122: place the front page into the output dir.

The image (entry.png, drawn by draw_image_20261122.py) sums up the world
news of Sunday 22 November 2026: COP31 collapses in Antalya, Iran strikes
US bases in Bahrain, a drone hits flats near Kyiv, West Bank settler
attacks, the AI sell-off, BepiColombo at Mercury, and the Cikande factory
fire. This program only copies that file, byte for byte, to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png). No network,
no randomness, no writes anywhere else.
"""
import hashlib
import os
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
SOURCE_NAME = "entry.png"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_source():
    source = HERE / SOURCE_NAME
    if not source.is_file():
        fail(f"{SOURCE_NAME} not found next to main.py")
    data = source.read_bytes()
    if not data.startswith(PNG_SIGNATURE):
        fail(f"{SOURCE_NAME} is not a PNG file")
    if len(data) > 1_048_576:
        fail(f"{SOURCE_NAME} is over the 1 MiB limit")
    return data


def write_output(data):
    out_dir = pathlib.Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / SOURCE_NAME
    target.write_bytes(data)
    written = target.read_bytes()
    if hashlib.sha256(written).hexdigest() != hashlib.sha256(data).hexdigest():
        fail("verification failed: written bytes differ from the source")
    return target


def main():
    data = read_source()
    target = write_output(data)
    print(f"wrote {target} ({len(data)} bytes, "
          f"sha256 {hashlib.sha256(data).hexdigest()[:16]}...)")


if __name__ == "__main__":
    main()
