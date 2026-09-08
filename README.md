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
