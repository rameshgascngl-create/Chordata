#!/usr/bin/env python3
"""Strict CHORDATA Play version input validation with typo-safe normalisation.

Accept one accidental trailing period in a numeric semver name, but retain
strict Android versionCode and versionName contracts. Never touch signing keys.
"""
import os
from pathlib import Path
import re


def validate(code: str, name: str) -> tuple[str, str, bool]:
    code = str(code).strip()
    name = str(name).strip()
    if not re.fullmatch(r"[0-9]+", code):
        raise ValueError("version_code must be a whole number (e.g. 2), not 1.0.0")
    number = int(code)
    if number < 1 or number > 2100000000:
        raise ValueError("version_code must be between 1 and 2100000000")
    corrected = name.endswith(".")
    if corrected:
        name = name[:-1]
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", name):
        raise ValueError("version_name must be numeric major.minor.patch, e.g. 1.0.0")
    return str(number), name, corrected


def main() -> None:
    try:
        code, name, corrected = validate(
            os.environ["RELEASE_CODE"], os.environ["RELEASE_NAME"]
        )
        env_file = Path(os.environ["GITHUB_ENV"])
    except (KeyError, ValueError) as exc:
        raise SystemExit("::error::Invalid Play release metadata: " + str(exc))
    if corrected:
        print("::notice::Removed a single accidental trailing '.' from version_name")
    with env_file.open("a", encoding="utf-8") as f:
        f.write("CHORDATA_RELEASE_VERSION_CODE=" + code + "\n")
        f.write("CHORDATA_RELEASE_VERSION_NAME=" + name + "\n")
    print("PASS: validated release versionCode=" + code + ", versionName=" + name)


if __name__ == "__main__":
    main()
