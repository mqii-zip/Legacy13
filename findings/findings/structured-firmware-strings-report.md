# Structured Findings Report: Extracted Firmware Strings

## 1) Scope
- **Project:** Legacy13 (`n61-ios13-research`)
- **Analyzed context:** iPhone 6s (`n71ap`) iOS 13 beta firmware notes and extracted identifiers
- **Primary source notes used:**
  - `findings/all_flash-analysis.md`
  - `findings/a8-reference-buildmanifest.md`

---

## 2) Extracted Strings and Identifiers

| String / Identifier | Type | Source Context | Confidence |
|---|---|---|---|
| `DeviceTree.n71ap.im4p` | File artifact | `Firmware/all_flash/` listing | High |
| `DeviceTree.n71map.im4p` | File artifact | `Firmware/all_flash/` listing | High |
| `iBoot.n71.RELEASE.im4p` | File artifact | `Firmware/all_flash/` listing | High |
| `LLB.n71.RELEASE.im4p` | File artifact | `Firmware/all_flash/` listing | High |
| `n71ap` | Hardware/platform identifier | DeviceTree naming + repo notes | High |
| `n71m` / `n71map` | Variant identifier | DeviceTree naming variant | Medium |
| `ApChipID = 0x8000` | BuildManifest key/value | iOS 13 beta BuildManifest finding | High |
| `0x8000` → Apple A8 | SoC mapping claim (from notes) | A8 reference analysis note | Medium |

---

## 3) Normalized Interpretation

### Bootchain-related artifacts present
The `all_flash` listing contains expected early-boot artifacts (`LLB`, `iBoot`, `DeviceTree`) packaged as `IM4P`, which is consistent with Apple bootchain image handling in IPSW firmware bundles.

### Platform targeting signal
`n71`/`n71ap` naming strongly indicates iPhone 6s platform targeting in the analyzed iOS 13 beta firmware set, while `n71m` likely indicates a board or hardware variant.

### Legacy compatibility signal
The BuildManifest note reports `ApChipID = 0x8000`, recorded in this repository as an A8-associated identifier. If validated against raw manifests and additional firmware components, this may indicate retained legacy references or shared support pathways relevant to A8 research.

---

## 4) Key Findings

1. **Core bootchain components are present in `all_flash`.**
   - Confirms availability of `LLB`, `iBoot`, and multiple `DeviceTree` images for targeted reverse-engineering.

2. **At least two closely related platform variants appear in naming (`n71ap`, `n71map`).**
   - Suggests variant-specific configuration differences that may affect compatibility experiments.

3. **An explicit `ApChipID` value associated with A8 was documented in BuildManifest notes.**
   - This is a high-value lead for investigating whether iOS 13-era assets still embed A8-related logic, metadata, or fallback pathways.

---

## 5) Risk / Confidence Assessment

- **High confidence:** File-name-based observations from listed `all_flash` artifacts.
- **Medium confidence:** Semantic interpretation of `n71m` as revision/variant without direct Apple internal mapping docs in-repo.
- **Medium confidence:** A8 implication from `ApChipID = 0x8000` pending independent re-validation from raw BuildManifest extraction in this repo.

---

## 6) Recommended Next Validation Steps

1. Re-extract and parse raw BuildManifest XML/PLIST from the same IPSW and confirm every `ApChipID` occurrence with surrounding device class metadata.
2. Perform string extraction (`strings`) and symbol/section triage for `iBoot.n71.RELEASE.im4p` and `LLB.n71.RELEASE.im4p` to identify cross-platform references (`n61`, `n71`, `s8000`, etc.).
3. Diff `DeviceTree.n71ap.im4p` vs `DeviceTree.n71map.im4p` for:
   - Memory map differences
   - SoC/peripheral node deltas
   - Display/GPU configuration changes
4. Build a structured indicator table (identifier → component → offset/source) to support reproducible follow-up analysis.

---

## 7) Analyst Notes

This report is intentionally constrained to **already captured extracted strings and markdown findings** in the current repository state. It does **not** claim binary-level proof beyond those notes; it is a structured synthesis for next-stage validation.
