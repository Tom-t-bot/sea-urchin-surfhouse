# Sea Urchin Surf House — static site mirror

Static HTML mirror of the Sea Urchin Surf House Squarespace site
(`raspberry-bellflower-hhkg.squarespace.com`), pulled with `wget --mirror`
on 2026-09-08 for migration off Squarespace to GitHub Pages + Cloudflare.

## What's here

- `*.html` — the site's pages (originally nested under the Squarespace
  hostname folder; flattened to repo root so it serves correctly from a
  GitHub Pages root)
- `images.squarespace-cdn.com/`, `static1.squarespace.com/`,
  `assets.squarespace.com/`, `file.squarespace-cdn.com/`,
  `definitions.sqspcdn.com/` — mirrored CDN assets (images, CSS, JS) that
  the pages reference via relative links

Verified locally with `python3 -m http.server` — pages, images, and internal
nav all load correctly.

## Known limitations of a raw mirror

- Squarespace's generated markup/CSS/JS is heavy (this is Squarespace's own
  framework output, not hand-written HTML) — it works, but it's not "simple"
  in the sense of lightweight hand-rolled HTML.
- Forms (e.g. contact form) will not work — Squarespace's form submission
  backend isn't part of a static mirror. Needs a replacement (e.g. Formspree,
  a `mailto:`, or a rebuild of that one page) before going live.
- `images.squarespace-cdn.com/` is ~107MB — mostly multiple resolutions of
  the same images that Squarespace generates for responsive `srcset`. Worth
  pruning to the sizes actually used before publishing, to keep the repo and
  GitHub Pages build lean.

## Next steps

1. Review pages, decide whether to keep as-is or rebuild any by hand.
2. Fix/replace the contact form.
3. Push to GitHub, enable GitHub Pages.
4. Point domain at GitHub Pages via Cloudflare DNS (see migration plan
   discussed in chat).

## Translations (es/fr/pt)

The site is translated into Spanish, French, and (European) Portuguese,
served from `es/`, `fr/`, `pt/` subfolders — the header's language picker
switches between them. English stays at the repo root.

This was done as a precise text-node substitution over the *original*
mirrored English HTML: every visible string was extracted once, translated,
then spliced back in without touching any markup, styling, or Squarespace
block structure. Asset/CSS references in the subfolder copies are rewritten
with a `../` prefix so they resolve back to the shared `images.squarespace-cdn.com/`
etc. folders at the repo root — nothing is duplicated per language.

If the English page content ever changes, translations do **not** update
automatically — regenerate them:

```
python3 i18n/translate_build.py
```

This re-derives `es/`, `fr/`, `pt/` (and re-applies the language-picker
markup + `lang-picker.js` tag) from the current root `*.html` files. Add any
new English string to `i18n/translations.py` first — the script errors out
listing exactly what's missing rather than silently shipping untranslated
text.

Note: the script rewrites the root `*.html` files in place (to populate the
picker and add the script tag) — don't run it twice in a row without
committing or resetting between runs, since it isn't idempotent against its
own output (it would double up the `<script>` tag).

## Known fixed bug: broken photo-gallery carousels

Squarespace's "Explore Our Shared Spaces" strip and each room's own photo
gallery (the `user-items-list-carousel` widget, on 11 pages) never rendered
any images in the raw mirror. Root cause: Squarespace loads that carousel's
layout/positioning logic from a webpack chunk fetched at runtime — code a
static `wget` crawl can't discover, since it's never referenced in the HTML,
only requested dynamically by already-running JS. Without it, every slide's
`<img>` has no `src` at all (only a JS-only `data-src`), and the ones that
do get a `src` collapse to `width:0` with `transform:translateX(-9999px)`,
since that positioning is also computed by the same missing JS.

Fixed by: giving every carousel `<img>` a real `src` (derived from its
`data-image` attribute, converted to the already-mirrored local path — 84
of the 95 unique gallery images had never actually been fetched by the
original mirror at all, since `data-src`/`data-image` aren't attributes
`wget --page-requisites` follows; fetched those from Squarespace's still-live
CDN), and replacing the JS-dependent layout with a plain CSS horizontal
scroll strip (`theme.css`, `.user-items-list-carousel__*` rules). The dead
prev/next arrow buttons are hidden since the strip is natively scrollable.

If you add a new page that uses this same carousel pattern, run the fix
again — it's not part of `i18n/translate_build.py` since it's a one-time
content fix, not a build step. Ask Claude, or see the session history for
the exact script.

## Studio Reef photos

`studio-reef/` holds real, current photos of Studio Reef (added directly to
the repo, not from the Squarespace mirror). `studio.html`'s main photo and
its 7-slide gallery use these; the old mirrored photos for that room were
removed. Referenced as `studio-reef/...` from the root pages and
`../studio-reef/...` from the `es/fr/pt` copies, same convention as
`theme.css`.
