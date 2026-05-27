#!/usr/bin/env python3
"""Parse BuildManifest.plist and extract key firmware metadata.

Extracted fields per BuildIdentity:
- DeviceClass
- ApChipID
- kernelcache paths
- DeviceTree paths
- firmware identifiers
"""

from __future__ import annotations

import argparse
import json
import plistlib
from pathlib import Path
from typing import Any


def _normalize_chip_id(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, int):
        return hex(value)
    return str(value)


def _extract_component_path(component: dict[str, Any]) -> str | None:
    if not isinstance(component, dict):
        return None

    path = component.get("Path")
    if isinstance(path, str):
        return path

    info = component.get("Info")
    if isinstance(info, dict):
        info_path = info.get("Path")
        if isinstance(info_path, str):
            return info_path

    return None


def parse_build_manifest(data: dict[str, Any]) -> dict[str, Any]:
    identities = data.get("BuildIdentities", [])
    results = []

    for idx, identity in enumerate(identities):
        if not isinstance(identity, dict):
            continue

        info = identity.get("Info", {}) if isinstance(identity.get("Info"), dict) else {}
        manifest = identity.get("Manifest", {}) if isinstance(identity.get("Manifest"), dict) else {}

        device_class = info.get("DeviceClass") or identity.get("DeviceClass")
        ap_chip_id = _normalize_chip_id(identity.get("ApChipID") or info.get("ApChipID"))

        kernelcache_paths: list[str] = []
        devicetree_paths: list[str] = []
        firmware_identifiers: set[str] = set()

        for component_name, component in manifest.items():
            component_path = _extract_component_path(component)
            if not component_path:
                continue

            name_lower = str(component_name).lower()
            path_lower = component_path.lower()

            if "kernelcache" in name_lower or "kernelcache" in path_lower:
                kernelcache_paths.append(component_path)

            if "devicetree" in name_lower or "devicetree" in path_lower:
                devicetree_paths.append(component_path)

            if "firmware" in name_lower or "/firmware/" in path_lower:
                firmware_identifiers.add(str(component_name))

        results.append(
            {
                "build_identity_index": idx,
                "device_class": device_class,
                "ap_chip_id": ap_chip_id,
                "kernelcache_paths": sorted(set(kernelcache_paths)),
                "devicetree_paths": sorted(set(devicetree_paths)),
                "firmware_identifiers": sorted(firmware_identifiers),
            }
        )

    return {
        "build_identity_count": len(results),
        "identities": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse BuildManifest.plist")
    parser.add_argument("plist", type=Path, help="Path to BuildManifest.plist")
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output",
    )
    args = parser.parse_args()

    with args.plist.open("rb") as f:
        data = plistlib.load(f)

    result = parse_build_manifest(data)

    if args.pretty:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(json.dumps(result))


if __name__ == "__main__":
    main()
