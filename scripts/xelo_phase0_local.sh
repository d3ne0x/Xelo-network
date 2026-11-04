#!/usr/bin/env bash
# Run Phase 0 checks without consuming GitHub Actions resources.
# Usage: bash scripts/xelo_phase0_local.sh [check|build]
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
MODE="${1:-check}"
if [[ "$MODE" != "check" && "$MODE" != "build" ]]; then
  echo "Usage: bash scripts/xelo_phase0_local.sh [check|build]" >&2
  exit 2
fi

echo "==> XELO Phase 0: lightweight guard and preset tests"
python3 -m compileall -q scripts/xelo_verify_free_build.py tests/xelo_phase0
python3 -m unittest discover -s tests/xelo_phase0 -p 'test_*.py' -v

if [[ "$MODE" == "check" ]]; then
  echo "==> Static checks passed. Full C++ build was not requested."
  exit 0
fi

if [[ "$(uname -s)" != "Linux" || "$(uname -m)" != "x86_64" ]]; then
  echo "Full build helper supports x86_64 Linux only." >&2
  echo "Run check mode on Raspberry Pi/ARM; use a dedicated x86_64 VM for the full build." >&2
  exit 2
fi

echo "==> Bootstrapping dependencies"
bash scripts/bootstrap-deps.sh
echo "==> Configuring MPL-only agent"
cmake --preset linux-free-release -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
echo "==> Enforcing excluded nonfree controller"
python3 scripts/xelo_verify_free_build.py \
  --cache build-linux-free-release/CMakeCache.txt \
  --compile-commands build-linux-free-release/compile_commands.json
echo "==> Building"
cmake --build --preset linux-free-release --parallel 2
echo "==> Running upstream selftest"
./build-linux-free-release/zerotier-selftest
echo "==> Phase 0 local build and selftest finished successfully."
