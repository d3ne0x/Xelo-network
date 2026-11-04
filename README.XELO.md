# XELO Network — development entry point

This repository forks [ZeroTierOne](https://github.com/zerotier/ZeroTierOne).
Upstream engine and notices are preserved. This is a **development fork**,
not a released or commercially approved product.

## Read first

- [Phase 0 engineering plan](docs/xelo/PHASE0.md)
- [Low-cost CI and lab builds](docs/xelo/BUILD_STRATEGY.md)
- [Licensing boundaries](docs/xelo/LICENSING.md)
- [Proposed architecture](docs/xelo/ARCHITECTURE.md)
- [Original upstream README](README.md) and [build instructions](build.md)

## No-compilation checks (recommended first)

On Linux / SAIA Raspberry Pi:

```bash
bash scripts/xelo_phase0_local.sh check
```

On Windows PowerShell:

```powershell
.\scripts\xelo_phase0_local.ps1
```

Both commands check the build guard and the intended free CMake presets.

## Full builds (isolated test machines only)

Linux **x86_64** prerequisites: CMake, C/C++ toolchain, Rust, Git, Ninja,
Python 3, OpenSSL development headers and nlohmann-json development headers.

```bash
bash scripts/xelo_phase0_local.sh build
```

Windows x64 prerequisites: VS 2022 C++ tools, CMake, Git, Python 3, Rust and
vcpkg with `VCPKG_ROOT` configured.

```powershell
.\scripts\xelo_phase0_local.ps1 -FullBuild
```

Full GitHub-hosted builds are **manual**, not triggered by every PR. See
[BUILD_STRATEGY.md](docs/xelo/BUILD_STRATEGY.md).

Do not install test binaries over an existing ZeroTier service. Network
integration requires a test controller you are authorized to use; disabling
the bundled controller does **not** create an independent XELO control plane.

No binary redistribution, production rollout or monetization is approved
until dependency licensing, third-party source, patent and security reviews
are complete.
