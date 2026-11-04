# XELO Network — proposed modular architecture

This describes future XELO-owned components. They do not yet exist in the
fork and must not be mistaken for implemented features.

## Layers

1. **Agent/transport:** keep ZeroTierOne's MPL-compatible peer networking
   implementation as an isolated, replaceable integration.
2. **Local bridge:** privileged local helper wrapping the loopback agent API;
   restrict token access, audit mutations and do not expose bearer secrets to
   a browser frontend.
3. **Desktop:** status, networks, membership, peer health, latency/relay
   diagnostics and read-only telemetry first.
4. **Management API:** later adds user/device inventory, policy templates,
   approval workflows and audit history.
5. **Control plane:** use an appropriately authorized external controller for
   initial development; independently design the XELO controller only after
   licensing, security and feasibility work.
6. **Topology integration:** exchange verified overlay facts with XELO
   Network Architect; do not conflate overlay edges with physical cabling.
7. **Cloud gateway:** explicitly provisioned/approved VPN gateway hosts
   for Azure/AWS/GCP in later phases.

## Local API security rules

- Keep agent management on loopback; do not expose TCP/9993 to LAN or cloud.
- Never log or return `authtoken.secret`, private identities or credential
  contents to the UI, diagnostics exports or crash reports.
- Prefer `X-ZT1-Auth` header over URL query parameters.
- Require OS authorization for configuration changes.
- Treat join/leave, route updates and firewall policies as privileged changes.
- Gate automation behind explicit user approval and rollback capability.

## First GUI development contract

Phase 1 should be a professional, accessible, read-only Desktop screen with
Connection Summary, Networks, Peers, Diagnostics and Settings navigation.
Use mock data for visual acceptance tests and then wire a local adapter to the
running agent. Visual parity must be screenshot-tested at fixed viewports.

## Operational portability

Avoid coupling the XELO management tier to a single cloud provider. Keep
configuration environment-based, use portable service containers and a
relational datastore if/when a backend becomes necessary.
