# AGENTS.md

Instructions for Codex in this repository.

## Branching

This project follows **GitHub Flow**.

- **Never commit directly to `main`** — not even for trivial fixes or CHANGELOG updates.
- Before any edit, check the current branch: if on `main`, run `git checkout -b <type>/<description>` first.
- Branch naming: `feature/*`, `fix/*`, `docs/*`, `refactor/*`
- After work is done, merge to `main` via `git merge --no-ff` and tag if releasing.

## Releasing

1. Update `CHANGELOG.md` on the feature/fix branch (not on `main`)
2. Commit with `chore: release vX.Y.Z`
3. Merge to `main`, then `git tag vX.Y.Z`
4. Push: `git push origin main && git push origin vX.Y.Z`
