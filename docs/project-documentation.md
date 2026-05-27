# N61 iOS 13 Reverse Engineering Documentation

## Executive Summary

This repository investigates whether portions of iOS 13-era firmware and userspace can be understood, adapted, or partially booted on **iPhone 6 (N61AP, A8)** hardware, which is officially capped at iOS 12.5.x.

The current evidence indicates that iOS 13 beta artifacts for iPhone 6s-class targets still include metadata and boot artifacts that may preserve historical compatibility traces relevant to A8-era platforms.

---

## Findings

### 1) `all_flash` contains expected boot-critical images

From analyzed iPhone 6s iOS 13 beta IPSW material, `Firmware/all_flash/` includes:

- `LLB.n71.RELEASE.im4p`
- `iBoot.n71.RELEASE.im4p`
- `DeviceTree.n71ap.im4p`
- `DeviceTree.n71map.im4p`

**Interpretation:** these components align with the classical Apple secure boot flow where LLB, iBoot, and DeviceTree are staged as signed IMG4/IM4P payloads.

### 2) BuildManifest includes `ApChipID = 0x8000`

Research notes identify an iOS 13 beta BuildManifest entry with:

- `ApChipID = 0x8000`

`0x8000` is associated with **Apple A8**, used by iPhone 6 / 6 Plus.

**Interpretation:** this does not prove runtime support for iPhone 6 on iOS 13, but it suggests residual or shared configuration paths that are relevant for reverse engineering and compatibility analysis.

### 3) Hardware variant identifiers appear in boot artifacts

Observed naming (`n71`, `n71m`, `n71ap`) indicates multiple hardware/board variants inside the same artifact set.

**Interpretation:** variant mapping and board config partitioning should be tracked carefully when testing cross-device component reuse.

---

## Architecture Notes

### Target and Reference Platforms

- **Primary target:** iPhone 6 (`iPhone7,2`, `n61ap`, A8)
- **Reference platform:** iPhone 6s (`iPhone8,1`, `n71ap`, A9)

### Research Strategy

The project follows a comparative reverse engineering approach:

1. Extract and catalog IPSW components (boot images, manifests, rootfs payloads).
2. Compare bootchain artifacts between known-supported and unsupported hardware generations.
3. Identify compatibility-relevant metadata (chip IDs, board IDs, variant tables).
4. Validate whether assumptions hold through controlled boot-stage experiments.

### Key Technical Axes

- **Bootchain sequencing:** LLB → iBoot → kernel handoff.
- **DeviceTree compatibility:** board-specific hardware description differences.
- **Kernelcache behavior:** legacy symbol/driver expectations for A8-class hardware.
- **Manifest-driven policy:** trust/selection logic encoded in BuildManifest fields.

---

## Firmware Structure

### IPSW (high-level)

A typical IPSW used in this research can be treated as a signed firmware bundle containing:

- Bootloader-stage images (LLB, iBoot) under firmware paths such as `Firmware/all_flash/`
- DeviceTree payloads (`*.im4p`) for hardware initialization description
- Build metadata (BuildManifest) used to map components to chip/board targets
- Kernel and userspace payloads (outside the scope of currently committed extraction notes)

### `all_flash` role in this project

`all_flash` is treated as the most direct entry point for bootchain reverse engineering because it bundles the earliest signed components required to reach kernel load decisions.

### Manifest role in this project

BuildManifest entries are treated as authoritative indexing metadata for:

- chip target declarations
- board-specific image selection
- cross-generation residue detection (e.g., unexpected SoC IDs)

---

## Bootchain Overview

> This section is an architecture-level reverse engineering model, not a claim of full iOS 13 bootability on iPhone 6.

1. **SecureROM (immutable, on-chip)**
   - Establishes root-of-trust and verifies first-stage signed boot material.
2. **LLB (`*.im4p`)**
   - Early loader stage that initializes minimal platform state and verifies next stage.
3. **iBoot (`*.im4p`)**
   - Performs broader initialization, policy checks, argument handling, and kernel image preparation.
4. **DeviceTree (`*.im4p`) integration**
   - Supplies board-specific hardware topology and configuration consumed during later boot initialization.
5. **Kernel handoff**
   - Control transfers to the kernel with selected boot arguments and hardware descriptors.
6. **Userspace transition**
   - Launch sequence continues toward rootfs/userspace (current project marks this as experimental/partial).

### Why this matters for N61/A8 research

Breakage on unsupported hardware can originate at any stage above due to:

- signature/policy mismatches
- incompatible board configuration assumptions
- missing/changed drivers in kernel or userspace
- altered memory/peripheral initialization expectations

---

## Suggested Next Steps

1. Complete BuildManifest comparison matrix for N61/N71 relevant entries.
2. Add structured DeviceTree diff notes (node-level and property-level deltas).
3. Expand kernelcache analysis with A8-relevant symbol/driver inventory.
4. Document reproducible boot experiment procedure and failure taxonomy.

---

## Scope and Status

- Project stage: **research and documentation**.
- No claim is made that iOS 13 fully boots on iPhone 6.
- Current repository evidence supports continued structured reverse engineering.
