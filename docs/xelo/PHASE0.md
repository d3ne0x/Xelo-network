# XELO Network — Phase 0 engineering baseline

Status: **implementation in review** (build and functional validation not yet confirmed).
Base: `zerotier/ZeroTierOne` `dev`, fork branch `dev` at
`899352e38405968516bb12a770f0ac02f6058fa8` (2026-11-03 audit).

## Objective

Build a reproducible, non-distributing baseline for an independently branded
management experience on top of the permissible networking agent source.
Do not alter cryptographic primitives, peer protocol, identity format, trusted
roots, routing behavior, or upstream attribution in Phase 0.

## Repository and branch policy

- `dev` stays the integration branch.
- Work happens on `feature/xelo-*` branches, reviewed via PRs.
- Upstream is tracked as `zerotier/ZeroTierOne`; record upstream SHAs in
  future updates and avoid rebasing release history.
- Preserve upstream notices, the upstream README, and attribution.
- Build and test in isolated virtual machines, not on a daily-use host.
- Require CI plus peer/network smoke testing before integration.
- No release packages, signed installers, or app distribution until audited.

## Why inherited workflows were changed

The upstream `build.yml` and `validate.yml` ran ordinary make builds, which
may include the source-available FileDB controller. The upstream
`central-controller.yaml` targeted ZeroTier-owned GCP/container infrastructure
and self-hosted runners. XELO now runs **fast Python/preset checks automatically**
on PRs and on pushes to `dev`. Full `ZT_NONFREE=OFF` Linux/Windows builds require
an explicit manual GitHub Actions dispatch or the local build helper. Both
legacy deployment/extended-validation jobs are disabled pending audit.
See [BUILD_STRATEGY.md](BUILD_STRATEGY.md) for the free-hosted-runner policy,
local SAIA checks and isolated VM full builds.

## Build gate

- Linux: `linux-free-release`
- Windows x64: `windows-x64-free`
- Required cache values: `ZT_NONFREE=OFF` and `ZT1_CENTRAL_CONTROLLER=OFF`
- On Linux the compilation manifest is checked for `nonfree/` source files.
- Run upstream selftest on Linux; add Windows smoke tests after CI stability.
- Do not upload generated executable artifacts during Phase 0.
- The build guard does not inspect every linked dependency, generated object,
  copied source, runtime behavior or patent requirement.

## Manual smoke-test checklist (not yet executed)

1. Build cleanly on Windows and Linux and collect CI logs.
2. Run the daemon in a disposable VM with isolated state; never overwrite a
   currently installed ZeroTier service or production identity.
3. Confirm version/status and local API work with loopback-only binding.
4. With an authorized test controller, join a disposable network and confirm
   two test nodes can exchange traffic.
5. Test reconnect, NAT path change, direct vs relay reporting and disconnect.
6. Document CPU/memory baseline, latency, packet loss and NAT scenarios.
7. Confirm agent logs do not expose authentication secrets or private keys.
8. Check upstream regression selftests and conduct source/dependency SBOM scan.
9. Review third-party licenses and source-available separation before release.

## Exit criteria

CI green on supported platforms, peer connection tests recorded, licensing
inventory reviewed, security defaults inspected, and next-phase UI/API scope
approved. Until then, Phase 0 is **not complete**.

## Immediate follow-up

Prototype a local-only XELO Desktop read-only dashboard using the loopback
service API and secure token handling; design a controller-neutral interface.
