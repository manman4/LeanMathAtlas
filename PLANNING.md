# Planning & Roadmap Notes

This document records design decisions and the reasoning behind things that were considered but not implemented.

---

## Current state

All planned modules are implemented (16 Lean proof files across ★☆☆ / ★★☆ / ★★★), with bilingual documentation (`docs/ja/` and `docs/en/`). See [CHANGELOG.md](CHANGELOG.md) for the full version history and [ROADMAP.md](ROADMAP.md) for the module list.

---

## Considered and deprioritized

### GitHub Actions CI

**Status:** Not implemented.

**What it would do:** Run `lake build` automatically on every push and pull request, and surface a "build passing" badge.

**Why it was deprioritized:**
- Currently a solo project — every push is already verified locally with `lake build` before it goes out.
- CI adds the most value when multiple contributors are pushing independently, or when dependency updates (e.g. a Mathlib version bump) could silently break things without anyone noticing.
- Technically feasible in ~5–10 min per run using `lake exe cache get` to pull pre-built Mathlib binaries from Lean's CDN, so compilation cost is not a blocker.

**Reconsider when:** The project has external contributors, or automated Mathlib version bumps are set up.

