#!/usr/bin/env python3
"""Recursively scan firmware files and extract Apple SoC and device identifier references."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Set

# Common firmware / text-like extensions worth scanning.
DEFAULT_EXTENSIONS = {
    ".im4p",
    ".img4",
    ".ipsw",
    ".plist",
    ".xml",
    ".txt",
    ".bin",
    ".dmg",
    ".dtb",
    ".devicetree",
    ".kernelcache",
}

# Patterns for Apple SoC and Apple device identifiers.
PATTERNS = {
    "soc_a_series": re.compile(r"\bA(?:[4-9]|[1-2][0-9])\b", re.IGNORECASE),
    "soc_t_series": re.compile(r"\bT[0-9]{1,2}\b", re.IGNORECASE),
    "soc_s_series": re.compile(r"\bS[0-9]{1,2}\b", re.IGNORECASE),
    "board_config": re.compile(r"\bn[0-9]{2,4}[a-z]{0,3}p\b", re.IGNORECASE),
    "iphone_identifier": re.compile(r"\biPhone[0-9]{1,2},[0-9]{1,2}\b"),
    "ipad_identifier": re.compile(r"\biPad[0-9]{1,2},[0-9]{1,2}\b"),
    "ipod_identifier": re.compile(r"\biPod[0-9]{1,2},[0-9]{1,2}\b"),
    "watch_identifier": re.compile(r"\bWatch[0-9]{1,2},[0-9]{1,2}\b"),
    "appletv_identifier": re.compile(r"\bAppleTV[0-9]{1,2},[0-9]{1,2}\b"),
}


def iter_files(root: Path, exts: Set[str]) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if exts and path.suffix.lower() not in exts:
            continue
        yield path


def scan_file(path: Path, max_bytes: int) -> Dict[str, List[str]]:
    try:
        raw = path.read_bytes()
    except OSError:
        return {}

    if max_bytes > 0 and len(raw) > max_bytes:
        raw = raw[:max_bytes]

    text = raw.decode("latin-1", errors="ignore")
    matches: Dict[str, List[str]] = {}
    for key, pattern in PATTERNS.items():
        found = sorted({m.group(0) for m in pattern.finditer(text)}, key=str.casefold)
        if found:
            matches[key] = found
    return matches


def build_report(root: Path, exts: Set[str], max_bytes: int) -> dict:
    files_report = []
    aggregate: Dict[str, Set[str]] = defaultdict(set)

    for file_path in iter_files(root, exts):
        rel = file_path.relative_to(root)
        found = scan_file(file_path, max_bytes=max_bytes)
        if not found:
            continue

        files_report.append({"file": str(rel), "matches": found})
        for key, values in found.items():
            aggregate[key].update(values)

    aggregate_sorted = {k: sorted(v, key=str.casefold) for k, v in sorted(aggregate.items())}
    return {
        "root": str(root),
        "scanned_extensions": sorted(exts),
        "files_with_matches": len(files_report),
        "aggregate": aggregate_sorted,
        "files": sorted(files_report, key=lambda x: x["file"]),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Recursively scan firmware files and extract Apple SoC/device references."
    )
    parser.add_argument("root", nargs="?", default=".", help="Root directory to scan (default: current dir)")
    parser.add_argument(
        "--ext",
        action="append",
        default=None,
        help="Extension to include (can be passed multiple times). Example: --ext .plist",
    )
    parser.add_argument(
        "--max-bytes",
        type=int,
        default=15_000_000,
        help="Read at most this many bytes from each file (default: 15000000). 0 = no limit.",
    )
    parser.add_argument("--output", help="Write JSON report to this path (default: print to stdout)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.root).resolve()
    exts = {e.lower() if e.startswith(".") else f".{e.lower()}" for e in (args.ext or DEFAULT_EXTENSIONS)}

    report = build_report(root=root, exts=exts, max_bytes=args.max_bytes)
    output = json.dumps(report, indent=2)

    if args.output:
        out_path = Path(args.output)
        out_path.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    main()
