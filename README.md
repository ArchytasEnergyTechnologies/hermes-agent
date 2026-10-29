# Desktop UX pull-request evidence

Production Hermes desktop captures for fork PRs [#8](https://github.com/ghgoodreau/hermes-agent/pull/8) and [#9](https://github.com/ghgoodreau/hermes-agent/pull/9). This evidence-only branch does not change either source branch.

## Exact source revisions

- Before: actual shared PR base `fcc26fbd9f1641755e49793d7ed608f3b7214c3d`.
- PR #8 after: `67defefd4642acd4bedf059392195b28ee9a3344`.
- PR #9 after: `7a1c062a71264e812ca3b44039aa89e2ace96363`.

All three packaged application build stamps were clean. Application archive SHA-256 values and observed runtime states are recorded in each PR's provenance JSON. Verification used actual native Electron renderer screenshots and real pointer/key events through CDP; no replacement UI, mocked app paint, or injected focus/selection state.

## PR #8 — close-button spacing

- [Matched before/after hover comparison](pr-8/pr-8-before-after.png).
- [Continuous recording: hover and real context menu](pr-8/pr-8-hover-menu.gif).
- [Continuous recording: actual Close action](pr-8/pr-8-close.gif).
- [Close-action screenshot checkpoints](pr-8/pr-8-close-result.png).
- [Sanitized source, geometry, action and transformation provenance](pr-8/public-provenance.json).

The before/after comparison uses the same light theme, 100% zoom, viewport, generic titles and hover state. The before build loses its pane-tab marker through context-menu composition; the after build retains it, preserving the close target and label mask.

## PR #9 — keyboard navigation and visible focus

- [Session-tab keyboard checkpoints](pr-9/session-tabs-keyboard.gif).
- [Zone/sidebar keyboard checkpoints](pr-9/zone-sidebar-keyboard.gif).
- [Sidebar focus before/after](pr-9/sidebar-focus-before-after.png).
- [Find focus before/after](pr-9/find-focus-before-after.png).
- [Explicit Chromium forced-colors emulation](pr-9/forced-colors-menu.png).
- [Sanitized source, action, focus/selection and transformation provenance](pr-9/provenance.json).

PR #9 GIFs are genuine screenshot checkpoints after the indicated real key events, held for readability; they are not continuous video. The tab sequence demonstrates focus moving independently of selection, activation retaining tab focus after a settling interval, and Delete retaining sibling focus. The sidebar sequence explicitly labels its initial focus helper; subsequent navigation and menu actions use real keys.

## Privacy and presentation

Only the specifically reviewed crops, animations and sanitized JSON files in this branch are public. Full-window originals, raw recordings, local paths and detailed private traces are not uploaded. Public media excludes personal/account identifiers, avatars, project names, terminal content and user messages. The visible sidebar title is generic onboarding text; adjacent metadata is opaquely masked and explicitly labeled `METADATA HIDDEN`.

Captions are outside app pixels. Other transformations are disclosed cropping/scaling and the sidebar metadata mask; the controls being demonstrated are not painted over. All public images and decoded animation frames received visual review and an additional local OCR check for identifying names, home paths and email addresses. OCR is supplementary, not a guarantee replacing visual review.
