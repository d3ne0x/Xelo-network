# XELO Network — development entry point

This repository is a fork of [ZeroTierOne](https://github.com/zerotier/ZeroTierOne).
The upstream networking engine and its notices are preserved; XELO-specific work
must be tracked separately. This is a **development fork**, not a released product.

## Read before changing anything

- [Phase 0 engineering plan](docs/xelo/PHASE0.md)
- [Licensing boundaries and unresolved items](docs/xelo/LICENSING.md)
- [Proposed architecture](docs/xelo/ARCHITECTURE.md)
- [Original ZeroTier README](README.md)
- [Original build guide](build.md)

## Initial Linux free build

Prerequisites: CMake, C/C++ build tools, Rust, Git, Ninja, Python 3,
OpenSSL development headers and nlohmann-json development headers.

```sh
bash scripts/bootstrap-deps.sh
python3 -m unittest discover -s tests/xelo_phase0 -v
cmake --preset linux-free-release -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
python3 scripts/xelo_verify_free_build.py \
  --cache build-linux-free-release/CMakeCache.txt \
  --compile-commands build-linux-free-release/compile_commands.json
cmake --build --preset linux-free-release --parallel 2
./build-linux-free-release/zerotier-selftest
```

## Initial Windows x64 free build

Prerequisites: VS 2022 C++ tools, CMake, Python 3, Rust and vcpkg with
`VCPKG_ROOT` configured.

```powershell
.\scripts\bootstrap-deps.ps1 -Arch x64
python -m unittest discover -s tests/xelo_phase0 -v
cmake --preset windows-x64-free
python scripts/xelo_verify_free_build.py --cache build-windows-x64-free/CMakeCache.txt
cmake --build --preset windows-x64-free-release --parallel 2
```

Do not install this build over an existing ZeroTier service. Test in an isolated
VM first. Network operations require access to a controller you are authorized
to use; turning the bundled controller off does not create an independent
XELO control plane.

**No binary redistribution, monetization or production release is approved by
this document.** License and dependency review are open work items.
