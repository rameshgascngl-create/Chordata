#!/usr/bin/env python3
"""Source-level low-memory check for the native image gallery.

This predicts ARGB_8888 pixel-buffer sizes using the same power-of-two
sampling logic as FigureGallery.decodePlateBitmap. It is not a device heap
measurement and cannot replace an Android instrumentation run.
"""
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'app/src/main/assets'
GALLERY = ROOT / 'app/src/main/java/in/gasc/zoology/chordata/ui/FigureGallery.kt'
TESTS = ROOT / 'app/src/androidTest/java/in/gasc/zoology/chordata/ReaderNavigationTest.kt'
LIMIT_PX = 1200
MAX_PREVIEW_BYTES = 5 * 1024 * 1024


def dimensions(p):
    with p.open('rb') as stream:
        head = stream.read(24)
    assert head[:8] == b'\x89PNG\r\n\x1a\n', f'Invalid PNG: {p}'
    return struct.unpack('>II', head[16:24])


def expected_preview(width, height):
    sample = 1
    while ((width // sample > LIMIT_PX or height // sample > LIMIT_PX)
           and sample < 32):
        sample *= 2
    return sample, 4 * (width // sample) * (height // sample)


def main():
    gallery = GALLERY.read_text(encoding='utf-8')
    tests = TESTS.read_text(encoding='utf-8')
    assert 'internal fun decodePlateBitmap(' in gallery
    assert 'options.inJustDecodeBounds = true' in gallery
    assert 'options.inSampleSize = sample' in gallery
    assert 'maxLongestEdgePx = 1200' in gallery
    assert 'decodePlateBitmap(context, plate.assetDirectory, plate.filename)' in gallery
    assert 'fun lessonPreviewIsBoundedAndZoomAssetIsFullResolution()' in tests

    manifest = json.loads((ASSETS / 'pencil_plates/manifest.json').read_text(encoding='utf-8'))
    paths = {item['path'].split('/')[-1] for item in manifest['figures']}
    sizes = []
    for filename in sorted(paths):
        width, height = dimensions(ASSETS / 'pencil_plates' / filename)
        sample, preview_bytes = expected_preview(width, height)
        original_bytes = 4 * width * height
        assert preview_bytes <= MAX_PREVIEW_BYTES, (
            f'Preview exceeds 5 MiB ARGB_8888 estimate: {filename} ({preview_bytes} bytes)')
        assert preview_bytes <= original_bytes
        sizes.append((filename, width, height, sample, preview_bytes, original_bytes))
    assert len(sizes) == 67
    worst = max(sizes, key=lambda x: x[4])
    biggest = max(sizes, key=lambda x: x[5])
    print(f'PASS: {len(sizes)} distinct PNGs; gallery uses bounded decode and full-resolution zoom')
    print(f'PASS: estimated maximum preview allocation {worst[4]/(1024*1024):.2f} MiB ({worst[0]})')
    print(f'NOTE: largest full-resolution source estimates {biggest[5]/(1024*1024):.2f} MiB ({biggest[0]})')
    print('NOTE: these are pixel-buffer estimates; emulator/device heap validation remains pending')

if __name__ == '__main__':
    main()
