# Estimated Boot Barriers: iPhone 6 (A8/n61) vs iOS 13 build for iPhone 6s (A9/n71)

## Scope
This estimate is based on repository findings:
- `Firmware/all_flash` for iPhone 6s iOS 13 beta contains only `n71*` bootchain artifacts.
- BuildManifest includes an `ApChipID = 0x8000` reference.

## Barrier 1 — Signed bootchain target mismatch (Very High)
**What is known:**
- `all_flash` contains `LLB.n71.RELEASE.im4p`, `iBoot.n71.RELEASE.im4p`, and `DeviceTree.n71*.im4p`.
- No explicit `n61` boot components are listed in findings.

**Why this blocks boot:**
- A8 iPhone 6 expects a bootchain and hardware description for `n61`.
- Even if restored, signed boot components are tightly bound to board/chip compatibility and secure boot policy.

**Estimated severity:** 10/10

## Barrier 2 — DeviceTree/platform description incompatibility (Very High)
**What is known:**
- Located DeviceTree files are `n71ap` and `n71map` (6s variants).

**Why this blocks boot:**
- DeviceTree drives early hardware init (memory map, peripherals, clocks, display paths, etc.).
- Using `n71` trees on `n61` will likely fail during early kernel bring-up or panic shortly after handoff.

**Estimated severity:** 9/10

## Barrier 3 — Kernelcache support gap for A8 platform (High)
**What is known:**
- `ApChipID = 0x8000` appears in BuildManifest, implying at least metadata-level A8 awareness.

**Why this is not sufficient:**
- Manifest references do not guarantee functional runtime support for `n61` board config, drivers, or initialization paths in iOS 13 kernel/userspace.
- If A8 code paths were removed or partially stubbed, kernel boot may fail after trust chain succeeds.

**Estimated severity:** 8/10

## Barrier 4 — Driver set and userspace hardware assumptions (High)
**What is likely:**
- iOS 13 for 6s may assume A9-era driver stack tuning and firmware expectations.

**Why this blocks practical boot:**
- Mismatches in GPU/display/SEP/baseband-related initialization or services can produce boot loops, panics, or stalls at/after launchd.

**Estimated severity:** 7/10

## Barrier 5 — Secure boot personalization/restore constraints (Very High)
**What is likely:**
- Restore/install pipelines enforce model/chip/build identity via signed IMG4 manifests and personalized tickets.

**Why this matters:**
- Even with hybrid images, producing a fully accepted boot path without exploiting the chain is a major blocker.

**Estimated severity:** 10/10

## Interpreting the `ApChipID=0x8000` finding
Most likely interpretations:
1. Shared manifest templates include legacy chip constants.
2. Some shared components remain multi-chip.
3. Residual support metadata exists without complete end-to-end boot support.

Therefore, this is a **promising clue** for research, but **not evidence** that stock iOS 13 6s firmware can boot on iPhone 6 without substantial bootchain/kernel adaptation.

## Overall estimate
- **Probability of straight boot (stock n71 iOS 13 image on n61):** near-zero.
- **Probability of partial boot with heavy hybridization/patching:** plausible only with significant low-level work across bootchain, DeviceTree, kernel, and trust/restore constraints.

## Recommended next validation steps
1. Enumerate BuildManifest identities to confirm whether any `n61`-compatible identities exist in the tested IPSW.
2. Inspect kernelcache symbols/strings for A8 + `n61` platform hooks.
3. Compare `n61` iOS 12 DeviceTree vs `n71` iOS 13 trees to map critical init diffs.
4. Attempt controlled hybrid boot experiments to identify exact fail stage (iBoot handoff vs early kernel vs userspace).
