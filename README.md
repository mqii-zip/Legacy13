# Legacy13

Legacy13 is an experimental low-level research and reverse engineering project focused on exploring the possibility of bringing iOS 13 compatibility to the iPhone 6 (A8), a device officially unsupported beyond iOS 12.5.x.

This repository documents research related to Apple's bootchain, firmware structure, kernel behavior, DeviceTree analysis, and hybrid firmware experimentation using components from both iOS 12 and iOS 13.

> This project is currently in the research stage.

---

# Goals

- Study the internal structure of IPSW firmware files
- Analyze iOS bootchain behavior on A8 devices
- Compare DeviceTree structures between iPhone 6 and iPhone 6s
- Research potential A8 compatibility inside iOS 13 builds
- Experiment with hybrid firmware approaches
- Document kernelcache behavior and boot process
- Attempt partial userspace booting on unsupported hardware

---

# Current Research Areas

## IPSW Analysis
Studying firmware packaging, IMG4 components, BuildManifest structure, and root filesystem organization.

## Bootchain Research
Analyzing SecureROM, iBoot, kernel loading, boot arguments, and low-level boot process behavior.

## DeviceTree Comparison
Comparing hardware descriptions between:
- iPhone 6 (`n61ap`)
- iPhone 6s (`n71ap`)

Current focus:
- memory regions
- hardware identifiers
- SoC differences
- display and GPU references

## Kernelcache Research
Investigating:
- A8 references
- legacy support remnants
- driver compatibility
- kernel patching possibilities
- panic causes

---

# Devices

| Device | Identifier | Chip |
|---|---|---|
| iPhone 6 | iPhone7,2 | A8 |
| iPhone 6s | iPhone8,1 | A9 |

---

# Current Status

- [x] Initial IPSW collection
- [x] Repository structure created
- [ ] BuildManifest comparison
- [ ] DeviceTree analysis
- [ ] Kernelcache inspection
- [ ] IMG4 extraction tests
- [ ] Custom ramdisk experiments
- [ ] Partial userspace# n61-ios13-research