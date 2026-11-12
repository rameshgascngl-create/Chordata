#!/usr/bin/env python3
"""Verify native .so ELF load segments and APK 16 KiB ZIP alignment.

AABs are repackaged into split APKs by Play; inspect the native ELF payloads
here. On a final APK, also verify uncompressed .so local ZIP data offsets.
Pure Kotlin does not exempt transitive SDK-provided .so libraries from checks.
"""
from pathlib import Path
from zipfile import ZipFile, ZIP_STORED
import struct
import sys

PAGE = 16384
def elf_load_alignment(data: bytes, name: str):
    assert data[:4] == b"\\x7fELF", f"Invalid ELF file: {name}"
    assert data[5] == 1, f"Unsupported big-endian ELF: {name}"
    cls = data[4]
    if cls == 2:
        phoff = struct.unpack_from("<Q", data, 32)[0]
        entsize, count = struct.unpack_from("<HH", data, 54)
        alignoff, posoff, vaddroff = 48, 8, 16
        unpack = "<Q"
    elif cls == 1:
        phoff = struct.unpack_from("<I", data, 28)[0]
        entsize, count = struct.unpack_from("<HH", data, 42)
        alignoff, posoff, vaddroff = 28, 4, 8
        unpack = "<I"
    else:
        raise AssertionError(f"Unknown ELF class: {name}")
    assert 0 < count < 1024 and entsize >= alignoff + (8 if cls == 2 else 4), name
    found = 0
    for i in range(count):
        start = phoff + i * entsize
        assert start + entsize <= len(data), f"Truncated program headers: {name}"
        if struct.unpack_from("<I", data, start)[0] != 1:
            continue
        found += 1
        off = struct.unpack_from(unpack, data, start + posoff)[0]
        virt = struct.unpack_from(unpack, data, start + vaddroff)[0]
        alignment = struct.unpack_from(unpack, data, start + alignoff)[0]
        assert alignment >= PAGE, f"ELF LOAD alignment below 16KiB: {name}, {alignment}"
        assert (virt - off) % PAGE == 0, f"ELF LOAD offsets incompatible with 16KiB: {name}"
    assert found, f"ELF has no PT_LOAD segments: {name}"
    return found

def check_archive(path: Path):
    assert path.is_file(), path
    is_apk = path.suffix.lower() == ".apk"
    with ZipFile(path) as archive, path.open("rb") as disk:
        members = [i for i in archive.infolist() if i.filename.endswith(".so")]
        for item in members:
            elf_load_alignment(archive.read(item), item.filename)
            if is_apk and item.compress_type == ZIP_STORED:
                disk.seek(item.header_offset)
                header = disk.read(30)
                assert header[:4] == b"PK\\x03\\x04", item.filename
                name_len, extra_len = struct.unpack_from("<HH", header, 26)
                offset = item.header_offset + 30 + name_len + extra_len
                assert offset % PAGE == 0, f"APK .so local ZIP offset not 16KiB aligned: {item.filename} ({offset})"
    print(f"PASS: {path.name}: {len(members)} native libraries; 16KiB ELF"
          + (" and ZIP placement" if is_apk else " segment checks"))
if __name__ == "__main__":
    assert len(sys.argv) == 2, "Usage: audit_native_16kb.py APK-or-AAB"
    check_archive(Path(sys.argv[1]))
