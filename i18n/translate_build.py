#!/usr/bin/env python3
import re, html as html_mod, os, sys

sys.path.insert(0, os.path.dirname(__file__))
from translations import T

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAGES = ['index.html','surfhouse.html','ribeiraapartment.html','studio.html','bungalow-coxos.html',
         'loft-backdoor.html','caravan.html','container.html','chill-areas.html','bbq.html',
         'coworking.html','living-room.html','activities.html','surf-spots.html','contact.html']

LANGS = ['es', 'fr', 'pt']
LANG_LABEL = {'en': 'English', 'es': 'Español', 'fr': 'Français', 'pt': 'Português'}
HTML_LANG = {'en': 'en-US', 'es': 'es-ES', 'fr': 'fr-FR', 'pt': 'pt-PT'}
CDN_DOMAINS = ['images.squarespace-cdn.com', 'static1.squarespace.com', 'assets.squarespace.com',
               'file.squarespace-cdn.com', 'definitions.sqspcdn.com']

missing_log = []


def excluded_spans(text):
    return [(m.start(), m.end()) for m in re.finditer(r'<(script|style)\b[^>]*>.*?</\1>', text, re.S | re.I)]


def in_excluded(pos, spans):
    return any(s <= pos < e for s, e in spans)


def translate_text_nodes(text, lang, page):
    spans = excluded_spans(text)

    def repl(m):
        if in_excluded(m.start(), spans):
            return m.group(0)
        raw = m.group(1)
        stripped = raw.strip()
        if not stripped:
            return m.group(0)
        if re.fullmatch(r'[\d\s.,/€$%:-]*', stripped):
            return m.group(0)
        if re.fullmatch(r'&[a-zA-Z#0-9]+;', stripped):
            return m.group(0)
        key = html_mod.unescape(stripped)
        entry = T.get(key)
        if entry is None:
            missing_log.append((page, lang, key))
            return m.group(0)
        translated = entry[lang]
        # preserve original leading/trailing whitespace pattern
        lead = raw[:len(raw) - len(raw.lstrip())]
        trail = raw[len(raw.rstrip()):]
        new_inner = lead + html_mod.escape(translated, quote=False) + trail
        return '>' + new_inner + '<'

    return re.sub(r'>([^<>]+)<', repl, text)


def fix_asset_paths(text):
    for d in CDN_DOMAINS:
        text = text.replace(d + '/', '../' + d + '/')
    text = text.replace('href="theme.css"', 'href="../theme.css"')
    text = text.replace('href="cart.html"', 'href="../cart.html"')
    return text


def find_matching_div(text, start_open_idx):
    depth = 0
    for m in re.finditer(r'<div\b|</div>', text[start_open_idx:]):
        if m.group(0) == '</div>':
            depth -= 1
            if depth == 0:
                return start_open_idx + m.end()
        else:
            depth += 1
    return None


def hrefs_for(page, current_lang):
    """Return {lang: href} for linking to `page` in each language, from a document at `current_lang`."""
    out = {}
    for lang in ['en', 'es', 'fr', 'pt']:
        if current_lang == 'en':
            out[lang] = page if lang == 'en' else f'{lang}/{page}'
        else:
            out[lang] = f'../{page}' if lang == 'en' else f'../{lang}/{page}'
    return out


def build_desktop_picker(current_lang, hrefs):
    options = []
    for lang in ['en', 'es', 'fr', 'pt']:
        cur = ' aria-current="true"' if lang == current_lang else ''
        options.append(f'<a href="{hrefs[lang]}" role="option"{cur}>{LANG_LABEL[lang]}</a>')
    options_html = '\n                    '.join(options)
    return (
        '<div class="language-picker language-picker-desktop" id="multilingual-language-picker-desktop">\n'
        '                  <button type="button" class="current-language" aria-haspopup="listbox" '
        'aria-expanded="false" aria-controls="language-picker-menu">\n'
        f'                    <span data-wg-notranslate class="current-language-name">{LANG_LABEL[current_lang]}</span>\n'
        '                    <span class="lang-caret" aria-hidden="true">&#9662;</span>\n'
        '                  </button>\n'
        '                  <div class="language-picker-content" id="language-picker-menu" role="listbox" hidden>\n'
        f'                    {options_html}\n'
        '                  </div>\n'
        '                </div>'
    )


def build_mobile_picker(current_lang, hrefs):
    options = []
    for lang in ['en', 'es', 'fr', 'pt']:
        cur = ' aria-current="true"' if lang == current_lang else ''
        options.append(f'<a href="{hrefs[lang]}"{cur}>{LANG_LABEL[lang]}</a>')
    options_html = '\n                      '.join(options)
    return (
        '<div id="multilingual-language-picker-mobile" class="header-menu-nav-folder" data-folder="language-picker">\n'
        '                  <div class="header-menu-nav-folder-content">\n'
        '                    <div class="language-picker-content lang-picker-mobile-list">\n'
        f'                      {options_html}\n'
        '                    </div>\n'
        '                  </div>\n'
        '                </div>'
    )


def replace_block(text, marker_id, new_block):
    marker = text.find(marker_id)
    if marker == -1:
        raise ValueError(f"marker {marker_id} not found")
    open_idx = text.rfind('<div', 0, marker)
    end_idx = find_matching_div(text, open_idx)
    return text[:open_idx] + new_block + text[end_idx:]


def replace_lang_pickers(text, current_lang, page):
    hrefs = hrefs_for(page, current_lang)
    text = replace_block(text, 'multilingual-language-picker-desktop', build_desktop_picker(current_lang, hrefs))
    text = replace_block(text, 'multilingual-language-picker-mobile', build_mobile_picker(current_lang, hrefs))
    return text


def set_html_lang(text, lang):
    return re.sub(r'lang="en-US"', f'lang="{HTML_LANG[lang]}"', text, count=1)


def add_script_tag(text, src):
    tag = f'<script src="{src}"></script>\n</body>'
    return text.replace('</body>', tag, 1)


def main():
    for page in PAGES:
        path = os.path.join(SITE, page)
        original = open(path, encoding='utf-8').read()

        # 1. update the English root page in place: populate picker, add script tag
        en_updated = replace_lang_pickers(original, 'en', page)
        en_updated = add_script_tag(en_updated, 'lang-picker.js')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(en_updated)

        # 2. generate translated copies
        for lang in LANGS:
            translated = translate_text_nodes(original, lang, page)
            translated = replace_lang_pickers(translated, lang, page)
            translated = fix_asset_paths(translated)
            translated = set_html_lang(translated, lang)
            translated = add_script_tag(translated, '../lang-picker.js')
            out_dir = os.path.join(SITE, lang)
            os.makedirs(out_dir, exist_ok=True)
            with open(os.path.join(out_dir, page), 'w', encoding='utf-8') as f:
                f.write(translated)
        print("done:", page)

    if missing_log:
        print(f"\n!!! {len(missing_log)} MISSING TRANSLATIONS !!!")
        for p, l, k in missing_log[:30]:
            print(f"  {p} [{l}] {k!r}")
    else:
        print("\nAll text nodes translated, no missing keys.")


if __name__ == "__main__":
    main()
