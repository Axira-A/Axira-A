# Axira-A GitHub Profile — V4 maintenance guide

This repository is the source of the public GitHub profile for `Axira-A`.

## Architecture

The profile has three layers:

1. **Static vector UI** — `scripts/build_visuals.py` generates the hero, footer, divider, and local icons.
2. **Manual project state** — `profile-status.json` is the single source of truth for the `CURRENTLY FORGING` panel.
3. **Live public GitHub data** — `scripts/update_profile.py` queries GitHub's public API, generates the dashboard/activity SVGs, and updates the marker-delimited public repository table in `README.md`.

The main README does not depend on a third-party statistics renderer. External images are limited to small enhancement badges; if they fail, the core profile remains readable.

## Routine edits

### Change the active development focus

Edit `profile-status.json` only. Keep 1–4 items, each with:

```json
{
  "project": "MaplesAdventure",
  "status": "ACTIVE BUILD",
  "detail": "short human-readable focus line"
}
```

Update the top-level `updated` date when the roadmap changes.

### Change projects, featured repositories, or toolchain

Edit `profile-config.json`.

- `projects` controls the portfolio/project definition.
- `featured_repositories` controls the live table order.
- `tools` documents the local tool icons and labels.

If a new tool is added, create a matching local SVG icon or extend `write_icons()` in `scripts/build_visuals.py`.

## Automation

### Profile refresh

`.github/workflows/profile-refresh.yml`

Runs:

- daily at 03:17 UTC;
- manually with **Run workflow**;
- after edits to the config/status/generator files.

It rebuilds vector UI, refreshes public GitHub metadata, validates the result, then commits only when generated output actually changed.

### Validate profile

`.github/workflows/validate-profile.yml`

Runs on profile changes and pull requests. It checks:

- configuration JSON;
- local README references;
- required SVGs;
- SVG XML validity;
- unsupported `<script>` / `foreignObject` constructs;
- accidental local raster UI regressions;
- Python syntax;
- accidental email exposure in the public README.

## Failure behavior

`update_profile.py` is deliberately conservative. If the GitHub API is temporarily unavailable, it keeps the last valid dashboard and timeline rather than overwriting them with an error state. The cached featured repository metadata lives at `data/live-cache.json`.

## GitHub Actions permissions

The refresh workflow needs repository **Contents: write** permission. The workflow declares this with:

```yaml
permissions:
  contents: write
```

If organization/account policy overrides workflow permissions, enable read/write workflow permissions in repository settings.

## Cache busting

The README references core SVGs with `?v=4`. When a future visual redesign changes static assets substantially, increment this version consistently (for example `?v=5`) to reduce stale GitHub image caching.

## Design constraints

Keep these rules unless there is a deliberate redesign:

- Core UI remains SVG/vector.
- No JavaScript in SVG.
- No `foreignObject`.
- Animation uses native SVG/SMIL only and must degrade gracefully to a readable still image.
- No invented project completion percentages.
- Dynamic public data must come from GitHub itself.
- Maintenance/debug explanations belong here, not in the public profile README.
