# XELO Network — preliminary licensing register

**Engineering notes, not legal advice or commercial clearance.**
Review the actual copyright/license files and obtain qualified legal advice
before selling, hosting, branding, packaging, or redistributing anything.

## Source map observed on 2026-11-03

| Path | Upstream's stated licensing | XELO treatment |
| --- | --- | --- |
| `node/`, `osdep/`, `service/`, most source outside exceptions | MPL-2.0 | Preserve notices; document modified files; comply with MPL source obligations |
| `nonfree/` (including controller) | ZeroTier Source-Available License | Exclude from proposed XELO builds; do not copy implementation into new controller |
| `ext/` and fetched/vendor libraries | Their individual licenses | Inventory and review separately before any distribution |
| ZeroTier marks, logos and other assets | Trademark and asset permissions may differ | Do not imply affiliation; retain required notices |

References: `LICENSE.txt`, `LICENSE-MPL.txt`,
`nonfree/LICENSE.md` and upstream `README.md`.

## Important build observation

The upstream default CMake option is `ZT_NONFREE=ON`, which builds the
bundled FileDB controller. The free CMake presets set `ZT_NONFREE=OFF`;
the compiled controller target is then excluded. The XELO CI guard checks
cache settings and, where CMake supports it, the compiled-source manifest.

A successful check is **not** proof that distribution is lawful: dependency
licenses, patents, notices, linked artifacts and platform packaging remain
to be audited. The MPL-2.0 core can have commercial uses subject to its terms;
the `nonfree/` components expressly require a commercial license for
commercial use, including offering powered services.

## Outstanding release gates

- [ ] Complete dependency/SBOM inventory including fetched external code.
- [ ] Review MPL modifications, source availability and notices for distribution.
- [ ] Confirm no source-available controller code is linked or bundled.
- [ ] Review patents, protocol interoperability, cryptographic export rules.
- [ ] Review third-party icons/artwork, ZeroTier marks and product naming.
- [ ] Review hosted control plane, network roots and API/service terms.
- [ ] Review privacy/security policies for diagnostic telemetry.
- [ ] Obtain legal sign-off for commercial use and packaging.
- [ ] Establish responsible disclosure and a XELO security contact.

## Independent control plane

An independent controller is an engineering proposal, not a legal exemption.
Do not clone the `nonfree/` implementation into a new XELO service.
Specify interoperability from public documentation and independently developed
tests, with a legal review of the interface and protocol.
