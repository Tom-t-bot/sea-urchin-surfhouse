#!/usr/bin/env python3
"""Builds the static site from these templates into the repo root.
Re-run after editing anything in this file: python3 build.py
"""
import os

NAV = [
    ("home", "home", "index.html"),
    ("surfhouse", "surf house", "surfhouse.html"),
    ("apartment", "apartment", "ribeiraapartment.html"),
    ("surf", "surf", "surf-spots.html"),
    ("contact", "contact", "contact.html"),
]

UNITS = [
    ("Studio Reef", "studio.html", "room-studio.jpg", 110, 440, 1320,
     "Welcome to our studio, a comfortable escape for surfers and travelers who want a bit more "
     "style and privacy. Located in a quiet and charming area, the studio is a cozy and well-equipped "
     "space for up to two people. It comes with a modern kitchen, a private bathroom, and a balcony "
     "where you can enjoy the ocean breeze. More than just a place to stay, it's where you can relax, "
     "feel at ease, and enjoy Ericeira with an extra touch of comfort."),
    ("Bungalow Coxos", "bungalow-coxos.html", "room-bungalow-coxos.jpg", 100, 370, 1100,
     "Welcome to our ocean-view bungalow, a perfect escape for surfers looking for comfort, "
     "convenience, and a touch of home away from home. Located in a peaceful and charming area, the "
     "bungalow is a cozy and fully equipped retreat for up to two people. Our bungalow is complete "
     "with a kitchen, bathroom and private veranda. More than just a place to sleep, it's a place "
     "where you can relax, recharge, and feel right at home."),
    ("Loft Backdoor", "loft-backdoor.html", "room-loft-backdoor.jpg", 100, 400, 1200,
     "Welcome to our modern and cozy loft, located just a few minutes from one of the best waves in "
     "Portugal. If you are looking for a comfortable space with all the essential resources for a "
     "surf trip, check out our Loft Backdoor. With the capacity to accommodate up to 4 people, our "
     "loft was designed to offer a stylish environment and also a homely atmosphere, thinking of "
     "every detail for your comfort. Featuring a fully equipped kitchen to prepare your meals and a "
     "modern bathroom."),
    ("Caravan Crazy Left", "caravan.html", "room-caravan.jpg", 80, 330, 950,
     "Welcome to our cozy caravan, a perfect escape for surfers looking for comfort, convenience, and "
     "a touch of home away from home. Located in a peaceful and charming area, the caravan is a cozy "
     "and fully equipped retreat for up to two people. Our caravan is complete with a kitchenette, "
     "bathroom, and comfortable sleeping area. Additionally, you'll have full access to our shared "
     "spaces, including a well-equipped kitchen, coworking space, bathrooms, and a barbecue area. "
     "Enjoy the best of both worlds: the privacy of your own retreat and the vibrant community of our "
     "surf house."),
    ("Container Pedra Branca", "container.html", "room-container.jpg", 70, 250, 800,
     "Welcome to our cozy container room, a perfect escape for surfers looking for comfort, "
     "convenience, and a touch of home away from home. Located in a peaceful and charming area, the "
     "container room is a cozy and fully equipped retreat for up to two people. Our container room is "
     "complete with a comfortable bed and a dedicated workspace. Additionally, you'll have full "
     "access to our shared spaces, including a well-equipped kitchen, coworking space, bathrooms, and "
     "a barbecue area."),
]

SPACES = [
    ("Chill Areas", "chill-areas.html", "space-chill-areas.jpg",
     "Our chill areas are designed to bring people together and create connections, no matter how far "
     "they've traveled. Set in a large garden, these spaces offer a shared kitchen, barbecue area, "
     "bathrooms, eating areas, storage for surfboards and wetsuits, and even paella pans for cooking. "
     "Every detail is crafted with personality and creativity, creating a unique atmosphere that "
     "encourages relaxation and camaraderie."),
    ("BBQ", "bbq.html", "space-bbq.jpg",
     "Our BBQ area is a vibrant space where guests come together to celebrate special occasions or "
     "simply relax with friends after a long day of surfing. Featuring an Argentinian-style grill, "
     "this large and well-designed area is perfect for cooking up a feast and enjoying great company."),
    ("Coworking", "coworking.html", "space-coworking.jpg",
     "Our coworking space is for those who want to enjoy perfect waves while keeping up with their "
     "work. Designed for a quiet and comfortable working environment, it features reliable high-speed "
     "internet and a tranquil atmosphere. Now you can surf and stay productive without missing a beat."),
    ("Living Room", "living-room.html", "space-living-room.jpg",
     "Our living room is the heart of our surf house, a place where guests can gather and unwind. "
     "Equipped with a dartboard, a TV for watching surf championships or movies, and a foosball "
     "table, there's always something to enjoy."),
]

SPOTS = [
    ("Coxos Beach", "spot-coxos.jpg",
     "Coxos is considered one of the best waves in Portugal, a perfect, long right that breaks over a "
     "slope that holds big swells and can make good tubes. It's not a wave for beginners and has a "
     "high degree of difficulty getting in and out depending on the tide. Respect the locals and "
     "avoid problems.",
     [("Tide", "Half-dry"), ("Swell", "West"), ("Wind", "East and Northeast"),
      ("Difficulty", "Advanced"), ("Localism", "Medium/Heavy")]),
    ("Ribeira D'ilhas", "spot-ribeira.jpg",
     "One of Ericeira's best-known waves. It's usually a more accessible wave because it's easy to "
     "get into and suits almost all levels of surfing — which also makes it a beach that's almost "
     "always very crowded. A very consistent wave that works practically all year round, though with "
     "a big swell it can get heavy. Venue for several World, European, and National championships.",
     [("Tide", "Half"), ("Swell", "West, works even small"), ("Wind", "East and Southeast"),
      ("Difficulty", "Beginner/Intermediate/Advanced"), ("Localism", "Medium")]),
    ("Pedra Branca", "spot-pedra-branca.jpg",
     "For the happiness of goofy-footers in the land of right-handers, Pedra Branca is a left-hand "
     "peak that almost always breaks perfectly, thanks to its rocky bottom. Next door is another peak "
     "with a right that breaks on bigger days, called “Backdoor.”",
     [("Tide", "Half full"), ("Swell", "West"), ("Wind", "East"),
      ("Difficulty", "Advanced"), ("Localism", "Heavy")]),
    ("Matadouro", "spot-matadouro.jpg",
     "Matadouro offers good lefts in the left corner and a point with fun rights on the other side, "
     "with several peaks scattered between them. The bottom is a mixture of sand and rocks, so be "
     "careful when entering and exiting the sea.",
     [("Tide", "Half tide, works well almost all tides"), ("Swell", "West/Northwest"), ("Wind", "East/North"),
      ("Difficulty", "Intermediate"), ("Localism", "Light")]),
    ("Foz do Lizandro", "spot-foz-do-lizandro.jpg",
     "A beach with a very consistent sandy bottom, with peaks scattered all over. On good days it can "
     "be a long, tubular wave. Usually very versatile for all levels and with low risks. Good for "
     "beginners.",
     [("Tide", "Half tide"), ("Swell", "Northwest/West"), ("Wind", "East"),
      ("Difficulty", "Beginner/Intermediate"), ("Localism", "Light/Medium")]),
]

INSTAGRAM = "https://www.instagram.com/ericeira_surf_house/"
EMAIL = "seaurchinsurfhouse@gmail.com"


def head(title, description):
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="icon" href="assets/favicon.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Young+Serif&family=Bitter:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">"""


def header(active):
    links = []
    for key, label, href in NAV:
        current = ' aria-current="page"' if key == active else ''
        links.append(f'<a href="{href}"{current}>{label}</a>')
    nav_links = "\n      ".join(links)
    return f"""<header class="site-header">
  <div class="container">
    <a class="brand" href="index.html">
      <img src="assets/img/logo.jpg" alt="">
      <span>Sea Urchin<br>Surf House</span>
    </a>
    <nav class="main-nav" aria-label="Primary">
      {nav_links}
    </nav>
    <button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false"><span></span></button>
  </div>
</header>"""


def footer():
    space_links = "\n        ".join(f'<a href="{href}">{name}</a>' for name, href, _, _ in SPACES)
    return f"""<footer class="site-footer">
  <div class="container">
    <div>
      <h4>Sea Urchin Surf House</h4>
      <p style="max-width:32ch;opacity:.85;">Ericeira, Portugal — the world surf reserve.</p>
      <div class="footer-links">
        <a href="mailto:{EMAIL}">{EMAIL}</a>
        <a href="{INSTAGRAM}">Instagram</a>
      </div>
    </div>
    <div class="footer-links">
      <h4>Explore</h4>
      <a href="surfhouse.html">Surf house</a>
      <a href="ribeiraapartment.html">Apartment</a>
      <a href="surf-spots.html">Surf spots</a>
      <a href="activities.html">Activities</a>
      <a href="contact.html">Contact</a>
    </div>
    <div class="footer-links">
      <h4>Shared spaces</h4>
      {space_links}
    </div>
  </div>
  <div class="footer-bottom">
    <div class="container">&copy; Sea Urchin Surf House, Ericeira, Portugal.</div>
  </div>
</footer>"""


def shared_spaces_strip():
    items = "\n      ".join(
        f'<a class="strip-item" href="{href}"><span>{name}</span><span aria-hidden="true">&rarr;</span></a>'
        for name, href, _, _ in SPACES
    )
    return f"""<section class="strip tight">
  <div class="container">
    <p class="eyebrow">Explore our shared spaces</p>
    <div class="strip-grid">
      {items}
    </div>
  </div>
</section>"""


def unit_card(name, href, img, day, week, month):
    return f"""<article class="card">
        <div class="frame"><img src="assets/img/{img}" alt="{name}" loading="lazy"></div>
        <div class="card-body">
          <h3>{name}</h3>
          <p class="price"><b>&euro;{day}</b>/day &middot; &euro;{week}/week &middot; &euro;{month}/month</p>
          <a class="btn btn-secondary btn-sm" href="{href}">Learn more</a>
        </div>
      </article>"""


def stays_grid(intro_id="stays"):
    cards = "\n      ".join(unit_card(n, h, i, d, w, m) for n, h, i, d, w, m, _ in UNITS)
    return f"""<div class="card-grid">
      {cards}
    </div>"""


def page(filename, title, description, active_nav, body):
    html = f"""<!doctype html>
<html lang="en">
<head>
{head(title, description)}
</head>
<body>
{header(active_nav)}
<main>
{body}
</main>
{footer()}
<script src="assets/nav.js"></script>
</body>
</html>
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", filename)


# ---------------------------------------------------------------- index.html
def build_index():
    apt_card = f"""<article class="card">
        <div class="frame"><img src="assets/img/hero-apartment.jpg" alt="Ribeira d'ilhas Apartment" loading="lazy"></div>
        <div class="card-body">
          <h3>Ribeira d'ilhas Apartment</h3>
          <p class="tag">Private apartment</p>
          <a class="btn btn-secondary btn-sm" href="ribeiraapartment.html">Learn more</a>
        </div>
      </article>"""
    unit_cards = "\n      ".join(
        f"""<article class="card">
        <div class="frame"><img src="assets/img/{img}" alt="{name}" loading="lazy"></div>
        <div class="card-body">
          <h3>{name}</h3>
          <p class="tag">Surf house</p>
          <a class="btn btn-secondary btn-sm" href="{href}">Learn more</a>
        </div>
      </article>""" for name, href, img, d, w, m, desc in UNITS
    )

    body = f"""<section class="hero" style="background-image:url('assets/img/hero-home.jpg')">
  <div class="container">
    <p class="dek">Experience the best of Ericeira with us</p>
    <h1>Welcome to the world surf reserve</h1>
    <a class="btn btn-primary" href="surfhouse.html">Explore our surf house</a>
  </div>
</section>

<section>
  <div class="container split">
    <div>
      <p class="eyebrow">Our place</p>
      <h2>The Surf House &amp; the Private Apartment</h2>
      <p class="lede">Passionate about surfing, Oliver found in Portugal not only the waves but the
        perfect place to build the surf house dream, where he also lives with his old four-legged
        companion, Nina.</p>
      <div class="facts" style="margin-top:24px;">
        <div><b>Location</b><span>Ericeira</span></div>
        <div><b>Surf skill</b><span>Beginner&ndash;Advanced</span></div>
        <div><b>Vibe</b><span>Surf city</span></div>
        <div><b>Season</b><span>All year</span></div>
      </div>
      <div style="display:flex;gap:12px;margin-top:28px;flex-wrap:wrap;">
        <a class="btn btn-primary" href="surfhouse.html">Explore our surf house</a>
        <a class="btn btn-secondary" href="ribeiraapartment.html">Explore our apartment</a>
      </div>
    </div>
    <div class="frame"><img src="assets/img/hero-surfhouse.jpg" alt="Sea Urchin Surf House" loading="lazy"></div>
  </div>
</section>

<section class="tight">
  <div class="container">
    <p class="eyebrow">Get 30% off this winter season</p>
    <h2>Find the stay that fits you</h2>
    <div class="card-grid">
      {apt_card}
      {unit_cards}
    </div>
  </div>
</section>

<section>
  <div class="container">
    <p class="eyebrow">How to get there</p>
    <h2>Thirty minutes from Lisbon Airport</h2>
    <p class="lede">The best way to get to our surf house is from Lisbon Airport, a 40-minute drive
      from Ericeira &mdash; one of Portugal's most popular beaches, both for the quality of the waves
      and the quick access it offers. Our Surf House (bungalow and loft) is 3 minutes from Coxos
      Beach; the Ribeira d'ilhas apartment sits close to the centre of Ericeira, facing Ribeira
      d'Ilhas Beach.</p>
    <div class="facts">
      <div><b>Surf house</b><span>3 min from Coxos Beach</span></div>
      <div><b>Apartment</b><span>5 min from Ribeira d'ilhas Beach</span></div>
    </div>
  </div>
</section>

{shared_spaces_strip()}
"""
    page("index.html", "Sea Urchin Surf House — Ericeira, Portugal",
         "A surf house and private apartment in Ericeira, Portugal, in the world surf reserve.",
         "home", body)


# ------------------------------------------------------------- surfhouse.html
def build_surfhouse():
    cards = "\n      ".join(unit_card(n, h, i, d, w, m) for n, h, i, d, w, m, _ in UNITS)
    body = f"""<section class="banner" style="background-image:url('assets/img/hero-surfhouse.jpg')">
  <div class="container"><h1>Our Surf House</h1></div>
</section>

<section>
  <div class="container">
    <p class="lede">From surfer to surfer, we blend comfort with the true energy of a surf space.
      Here, you'll enjoy engaging conversations, social gatherings, surf movies, and the tranquility
      of a good night's sleep &mdash; plus a coworking space and plenty of nature around.</p>
    <p>Each space has a different and unique personality, designed with a lot of love and creativity
      and often made by Oliver's own hands. This makes Sea Urchin Surf House such a welcoming place,
      providing everyone with a cozy stay and the cultural exchange that surfing offers.</p>
  </div>
</section>

<section class="tight">
  <div class="container">
    <h2>Choose your stay</h2>
    <div class="card-grid">
      {cards}
    </div>
  </div>
</section>

<section>
  <div class="container">
    <p>The space is inviting and relaxing, with a warm and friendly atmosphere &mdash; good surfing
      sessions and memorable moments with friends or family. Our Surf House is surrounded by a large
      garden and common area, perfect for barbecues and dinners with friends, close to all of
      Ericeira's local amenities while staying away from the noise and bustle of the village. Come and
      join us for a stay filled with nature, comfort, and convenience &mdash; we look forward to your
      visit!</p>
  </div>
</section>

{shared_spaces_strip()}
"""
    page("surfhouse.html", "Our Surf House — Sea Urchin",
         "Sea Urchin Surf House in Ericeira: five stays, a shared garden, and the true energy of a surf space.",
         "surfhouse", body)


# --------------------------------------------------------- ribeiraapartment.html
def build_apartment():
    cards = "\n      ".join(unit_card(n, h, i, d, w, m) for n, h, i, d, w, m, _ in UNITS)
    body = f"""<section class="banner" style="background-image:url('assets/img/hero-apartment.jpg')">
  <div class="container"><h1>Ribeira D'ilhas Apartment</h1></div>
</section>

<section>
  <div class="container split">
    <div class="frame"><img src="assets/img/hero-apartment.jpg" alt="Ribeira d'ilhas Apartment" loading="lazy"></div>
    <div>
      <p class="eyebrow">Get 30% off this winter season</p>
      <p class="lede">Welcome to our ocean-view apartment, located on one of the most famous beaches
        in Ericeira. Whether you're planning a vacation with family or friends, this is the perfect
        place for comfort and convenience &mdash; close to all the best of Ericeira, with the
        tranquility and beauty of the region.</p>
      <div class="price-panel">
        <div><span class="amount">&euro;350</span><span class="period">per day</span></div>
        <div><span class="amount">&euro;1,500</span><span class="period">per week</span></div>
        <div><span class="amount">&euro;4,000</span><span class="period">per month</span></div>
      </div>
      <a class="btn btn-primary" style="margin-top:20px;" href="mailto:{EMAIL}">Enquire to book</a>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <p>Guests staying in our private apartment can also enjoy full access to the shared spaces of our
      surf house &mdash; the vibrant BBQ area, the lively living room with a dartboard, TV, and
      foosball table, and the coworking space with high-speed internet. Relax in the large garden,
      dine with friends, store your surfboards and wetsuits, and cook using our special paella pans.</p>
  </div>
</section>

<section class="tight">
  <div class="container">
    <h2>Explore all stays</h2>
    <div class="card-grid">
      {cards}
    </div>
  </div>
</section>
"""
    page("ribeiraapartment.html", "Ribeira D'ilhas Apartment — Sea Urchin",
         "An ocean-view private apartment on Ribeira d'ilhas beach in Ericeira, Portugal.",
         "apartment", body)


# ------------------------------------------------------------- unit pages
def build_unit(name, href, img, day, week, month, desc):
    cap = " ".join(w if w.isupper() else w for w in name.split())
    body = f"""<section class="banner" style="background-image:url('assets/img/{img}')">
  <div class="container"><h1>{name}</h1></div>
</section>

<section>
  <div class="container split">
    <div class="frame"><img src="assets/img/{img}" alt="{name}" loading="lazy"></div>
    <div>
      <p class="lede">{desc}</p>
      <div class="price-panel">
        <div><span class="amount">&euro;{day}</span><span class="period">per day</span></div>
        <div><span class="amount">&euro;{week}</span><span class="period">per week</span></div>
        <div><span class="amount">&euro;{month}</span><span class="period">per month</span></div>
      </div>
      <a class="btn btn-primary" style="margin-top:20px;" href="mailto:{EMAIL}">Enquire to book</a>
    </div>
  </div>
</section>

{shared_spaces_strip()}
"""
    page(href, f"{name} — Sea Urchin",
         f"{name} at Sea Urchin Surf House, Ericeira, Portugal.",
         "surfhouse", body)


# ------------------------------------------------------------- space pages
def build_space(name, href, img, desc):
    others = "\n      ".join(
        f'<a class="strip-item" href="{h}"><span>{n}</span><span aria-hidden="true">&rarr;</span></a>'
        for n, h, i, d in SPACES if h != href
    )
    body = f"""<section class="banner" style="background-image:url('assets/img/{img}')">
  <div class="container"><h1>{name}</h1></div>
</section>

<section>
  <div class="container split">
    <div class="frame"><img src="assets/img/{img}" alt="{name}" loading="lazy"></div>
    <div>
      <p class="lede">{desc}</p>
      <a class="btn btn-primary" href="surfhouse.html">See all stays</a>
    </div>
  </div>
</section>

<section class="strip tight">
  <div class="container">
    <p class="eyebrow">Other shared spaces</p>
    <div class="strip-grid">
      {others}
    </div>
  </div>
</section>
"""
    page(href, f"{name} — Sea Urchin",
         f"{name} at Sea Urchin Surf House, Ericeira, Portugal.",
         "surfhouse", body)


# ------------------------------------------------------------- surf-spots.html
def build_surf_spots():
    cards = []
    for name, img, desc, stats in SPOTS:
        stat_items = "\n            ".join(f"<li><b>{k}</b>{v}</li>" for k, v in stats)
        cards.append(f"""<article class="spot-card">
        <div class="frame"><img src="assets/img/{img}" alt="{name}" loading="lazy"></div>
        <div class="spot-body">
          <h3>{name}</h3>
          <p style="margin-bottom:0;">{desc}</p>
          <ul class="spot-stats">
            {stat_items}
          </ul>
        </div>
      </article>""")
    body = f"""<section class="banner" style="background-image:url('assets/img/spot-coxos.jpg')">
  <div class="container"><h1>Surf spots</h1></div>
</section>

<section>
  <div class="container">
    <p class="lede">Five of the breaks closest to Sea Urchin Surf House, from Coxos' heavy barrels to
      Foz do Lizandro's forgiving beach break.</p>
    {"".join(c + chr(10) for c in cards)}
  </div>
</section>
"""
    page("surf-spots.html", "Surf Spots — Sea Urchin",
         "Guide to the surf spots near Ericeira: Coxos, Ribeira d'ilhas, Pedra Branca, Matadouro, and Foz do Lizandro.",
         "surf", body)


# ------------------------------------------------------------- activities.html
def build_activities():
    services = [
        ("01", "Surf Guide",
         "One of our main services. We know you're here to surf the best waves in the region, and "
         "we're ready to take you there. Our local guides know the best spots, are familiar with the "
         "ideal wind, tide and swell conditions, and will make sure you're in the right place at the "
         "right time."),
        ("02", "Yoga",
         "We also offer packages with yoga classes. Surfing and yoga complement each other perfectly, "
         "providing balance, flexibility and muscle strengthening. Our qualified instructors will "
         "guide you through sessions specially designed for surfers."),
        ("03", "Airport transfers",
         "We make it easy to get to us with our airport transfer service. Our staff will be waiting "
         "for you at the airport to take you directly to our surf house, so you can relax and start "
         "your adventure as soon as possible."),
    ]
    blocks = "\n      ".join(f"""<div class="service">
        <span class="num">{n}</span>
        <div><h3>{t}</h3><p style="margin-bottom:0;">{d}</p></div>
      </div>""" for n, t, d in services)
    body = f"""<section class="banner" style="background-image:url('assets/img/hero-activities.jpg')">
  <div class="container"><h1>Activities</h1></div>
</section>

<section>
  <div class="container">
    <p class="lede">At our Surf House, we offer much more than comfortable accommodation and a
      relaxed atmosphere &mdash; a complete surfing experience, with additional services that take
      your stay to the next level.</p>
    {blocks}
    <p style="margin-top:8px;"><em>All activities are subject to availability and require prior
      scheduling, done directly via WhatsApp.</em></p>
    <a class="btn btn-primary" href="contact.html">Talk to us</a>
  </div>
</section>
"""
    page("activities.html", "Activities — Sea Urchin",
         "Surf guiding, yoga, and airport transfers at Sea Urchin Surf House, Ericeira.",
         None, body)


# ------------------------------------------------------------- contact.html
def build_contact():
    body = f"""<section class="banner" style="background-image:url('assets/img/card-contact.jpg')">
  <div class="container"><h1>Contact</h1></div>
</section>

<section>
  <div class="container">
    <p class="lede">For all reservations, please contact us via email.</p>
    <a class="mailto-card" href="mailto:{EMAIL}">
      <span aria-hidden="true">&#9993;</span>
      <span class="amount">{EMAIL}</span>
    </a>

    <h2 style="margin-top:48px;">Extra activities</h2>
    <div class="card-grid">
      <article class="card"><div class="card-body"><h3>Surf Guide</h3></div></article>
      <article class="card"><div class="card-body"><h3>Yoga</h3></div></article>
      <article class="card"><div class="card-body"><h3>Airport Pickup</h3></div></article>
    </div>
    <a class="btn btn-secondary" style="margin-top:20px;" href="activities.html">Learn more</a>
  </div>
</section>
"""
    page("contact.html", "Contact — Sea Urchin",
         "Contact Sea Urchin Surf House in Ericeira, Portugal.",
         "contact", body)


if __name__ == "__main__":
    build_index()
    build_surfhouse()
    build_apartment()
    for name, href, img, day, week, month, desc in UNITS:
        build_unit(name, href, img, day, week, month, desc)
    for name, href, img, desc in SPACES:
        build_space(name, href, img, desc)
    build_surf_spots()
    build_activities()
    build_contact()
    print("done")
