#!/usr/bin/env python3
"""Fail closed if a proposed XELO build enables the source-available controller.

This is a CI build-configuration guard, NOT a legal compliance certification.
Run it after CMake configure, before building. On Makefile/Ninja generators,
provide compile_commands.json for a second check on directly compiled sources.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys


_CACHE_LINE = re.compile(r"^([A-Za-z_][A-Za-z_0-9]*):[^=]+=(.*)$")


def check_cache(cache_text: str) -> None:
    cache: dict[str, str] = {}
    for line in cache_text.splitlines():
        match = _CACHE_LINE.match(line)
        if match:
            cache[match.group(1)] = match.group(2).strip().upper()
    for name in ("ZT_NONFREE", "ZT1_CENTRAL_CONTROLLER"):
        value = cache.get(name)
        if value not in ("OFF", "FALSE", "NO", "0"):
            raise ValueError(f"{name} must be explicitly OFF (found {value!r})")


def check_compile_commands(commands_text: str) -> None:
    commands = json.loads(commands_text)
    if not isinstance(commands, list) or not commands:
        raise ValueError("compile_commands.json is empty or not a list")
    offenders = []
    for command in commands:
        if not isinstance(command, dict) or not isinstance(command.get("file"), str):
            raise ValueError("Invalid entry in compile_commands.json")
        source = "/" + command["file"].replace("\\", "/").lstrip("/")
        if "/nonfree/" in source.lower():
            offenders.append(command["file"])
    if offenders:
        raise ValueError("Nonfree source files appear in compilation: " + ", ".join(offenders[:10]))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, required=True, help="Configured CMakeCache.txt")
    parser.add_argument("--compile-commands", type=Path, help="Optional compile_commands.json")
    args = parser.parse_args()
    try:
        check_cache(args.cache.read_text(encoding="utf-8"))
        if args.compile_commands:
            check_compile_commands(args.compile_commands.read_text(encoding="utf-8"))
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"XELO FREE BUILD GUARD: FAIL: {exc}", file=sys.stderr)
        return 1
    print("XELO FREE BUILD GUARD: PASS (CMake flags and supplied compiled-source manifest)")
    print("This is not a complete license, dependency, binary, or patent audit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
