#!/usr/bin/env python3
"""Regression tests for GitHub Play candidate input handling."""
from validate_play_release_inputs import validate


def reject(code: str, name: str) -> None:
    try:
        validate(code, name)
    except ValueError:
        return
    raise AssertionError(f"Unsafe input accepted: {code!r}, {name!r}")


def main() -> None:
    assert validate("2", "1.0.0") == ("2", "1.0.0", False)
    assert validate("2", "1.0.0.") == ("2", "1.0.0", True)
    assert validate(" 2 ", " 1.0.0. ") == ("2", "1.0.0", True)
    assert validate("0002", "1.0.0") == ("2", "1.0.0", False)
    for code, name in [
        ("1.0.0", "1.0.0"), ("0", "1.0.0"), ("-2", "1.0.0"),
        ("2100000001", "1.0.0"), ("2", "1.0.0.."), ("2", "1.0.0-beta"),
        ("2", "1.0"), ("2", "1.0.0.1"), ("2", "1.0.0;echo nope"),
        ("2", ""), ("2", "qa-1.0.0"),
    ]:
        reject(code, name)
    print("PASS: safe trailing dot correction, integer version code and strict semver rejection")


if __name__ == "__main__":
    main()
