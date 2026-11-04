# XELO Network — no-cost development and build strategy

The public repository can use standard GitHub-hosted runners without billed
Actions minutes under the current GitHub public-repository policy; normal
platform restrictions, storage policies, abuse protections and future policy
changes still apply. We intentionally minimize unnecessary runs.

## What runs automatically?

The workflow `.github/workflows/build.yml` only executes fast Python/preset
checks on pull requests to `dev` and pushes to `dev`. The existing build
jobs no longer run on every feature-branch push or PR. The fast checks do not
build a C++ binary or publish artifacts.

## How to request a complete build

After the workflow exists on the default branch and Actions are enabled:
**Actions → XELO - Phase 0 validation → Run workflow**. Select `linux`,
`windows`, or `both` and then run it.

Manual build jobs always set the free CMake preset and check
`ZT_NONFREE=OFF` and `ZT1_CENTRAL_CONTROLLER=OFF`. Linux additionally
checks its CMake compilation database for `nonfree/` source paths.
Windows's Visual Studio generator does not provide the same compilation
manifest in the current configuration; its check is less comprehensive.

## Local developer commands

Lightweight checks on **SAIA Raspberry Pi** or any supported Linux host:

```bash
git switch feature/xelo-phase0-foundation
bash scripts/xelo_phase0_local.sh check
```

Full Linux build **only in an isolated x86_64 development VM** after installing
the prerequisites in `README.XELO.md`:

```bash
bash scripts/xelo_phase0_local.sh build
```

Windows local checks in PowerShell:

```powershell
.\scripts\xelo_phase0_local.ps1
```

Windows full build in a dedicated development VM with VS 2022 C++ tools, Git,
CMake, Python, Rust and vcpkg:

```powershell
.\scripts\xelo_phase0_local.ps1 -FullBuild
```

## Safety and infrastructure limitations

- **Do not** install the fork over production ZeroTier services or re-use a
  production `identity.secret` file.
- **Do not** register SAIA (hosting other applications) as a GitHub Actions
  self-hosted runner for a public repository. Untrusted PR code and workflows
  can attack the host. Use an isolated disposable VM for privileged tests.
- Running Python checks on SAIA does not install network drivers or start the
  agent, but avoid installing an entire development toolchain solely for this.
- Raspberry Pi 4 may not support assumptions in the current upstream ARM
  build flags. Full-build helper deliberately refuses non-x86_64 Linux.
- Manual CI builds require GitHub Actions enabled on the fork, and the
  workflow file available on the default branch.
- Build success is not legal clearance or proof of a secure networking product.
- No automatic scheduled jobs, artifact uploads, release publications or
  paid larger-runner selections are configured.

## Release gate

Before releasing any binary: complete dependency/SBOM and license checks,
repeatable builds, isolated network functional tests, security tests, legal
review and XELO attribution/trademark review.
