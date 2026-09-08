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
