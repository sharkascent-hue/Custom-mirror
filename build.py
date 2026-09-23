#!/usr/bin/env python3
"""Builds the static Cut to Size Mirrors & Glass site.

Every page shares one header, footer and <head>, defined once below.
Edit this file, then run:  python3 build.py
Output is plain HTML next to this script, ready to upload to any static host.
Links inside templates start with "~/", which becomes the right relative path.
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
DOMAIN = "https://cuttosizemirrors.co.uk"
PHONE = "01630 638389"
TEL = "tel:+441630638389"
EMAIL = "info@cuttosizemirrors.co.uk"
ADDRESS = "Unit C27 Rosehill Industrial Estate, Market Drayton, TF9 2JU"
TRUSTPILOT = "https://www.trustpilot.com/review/www.cuttosizemirrors.co.uk"
MIRROR = "~/product/custom-mirror/"
GLASS = "~/product/custom-glass/"
SPLASH = "~/product/made-to-measure-custom-splashback/"

# ---------------------------------------------------------------- icons
def icon(d, extra=""):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"{extra}>{d}</svg>')

I = {
    "truck": icon('<path d="M3 6h11v9H3zM14 9h4l3 3v3h-7"/><circle cx="7" cy="17" r="2"/><circle cx="17" cy="17" r="2"/>'),
    "shield": icon('<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>'),
    "phone": icon('<path d="M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a2 2 0 01-2 2A16 16 0 013 6a2 2 0 012-2"/>'),
    "basket": icon('<path d="M3 5h2l2.2 10.2a2 2 0 002 1.8h7.6a2 2 0 002-1.6L20 8H6"/><circle cx="10" cy="20.5" r="1"/><circle cx="17" cy="20.5" r="1"/>'),
    "menu": icon('<path d="M4 7h16M4 12h16M4 17h16"/>'),
    "close": icon('<path d="M6 6l12 12M18 6L6 18"/>'),
    "arrow": icon('<path d="M5 12h14M13 6l6 6-6 6"/>'),
    "ruler": icon('<path d="M3 17L17 3l4 4L7 21z"/><path d="M7 13l2 2M10 10l2 2M13 7l2 2"/>'),
    "cut": icon('<rect x="4" y="4" width="16" height="16" rx="1.5"/><path d="M4 12h16M12 4v16" stroke-dasharray="2 2.5"/>'),
    "clock": icon('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
    "lock": icon('<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 018 0v3"/>'),
    "pin": icon('<path d="M12 21s7-6.2 7-12a7 7 0 00-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="9" r="2.5"/>'),
    "mail": icon('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>'),
    "users": icon('<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0113 0"/><path d="M16 4.5a3.5 3.5 0 010 7M18 14a6 6 0 013.5 6"/>'),
    "sparkle": icon('<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M6 18l2.5-2.5M15.5 8.5L18 6"/>'),
    "heart": icon('<path d="M12 20s-7.5-4.5-7.5-10A4.5 4.5 0 0112 7a4.5 4.5 0 017.5 3c0 5.5-7.5 10-7.5 10z"/>'),
    "star": icon('<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>'),
    "building": icon('<path d="M4 21V5l8-2v18M12 8h8v13M8 8v.01M8 12v.01M8 16v.01M16 12v.01M16 16v.01M2 21h20"/>'),
    "tool": icon('<path d="M14.7 6.3a4 4 0 00-5.4 5.2L3 17.8V21h3.2l6.3-6.3a4 4 0 005.2-5.4l-2.5 2.5-2.3-.5-.5-2.3z"/>'),
    "layers": icon('<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/>'),
    "check": icon('<path d="M5 12l5 5 9-10"/>'),
    "drop": icon('<path d="M12 3s6 6.5 6 11a6 6 0 01-12 0c0-4.5 6-11 6-11z"/>'),
    "bath": icon('<path d="M3 12h18v3a5 5 0 01-5 5H8a5 5 0 01-5-5zM6 12V5a2 2 0 014 0M6 20l-1 1.5M18 20l1 1.5"/>'),
    "gym": icon('<path d="M6.5 6.5v11M17.5 6.5v11M3 9.5v5M21 9.5v5M6.5 12h11"/>'),
    "dance": icon('<circle cx="13" cy="4" r="2"/><path d="M13 7l-2 5 3 3v6M11 12l-4 1M13 8l4 3M14 15l-4 6"/>'),
    "bed": icon('<path d="M3 18V6M3 14h18v4M21 14v-2a3 3 0 00-3-3h-7v5"/><circle cx="7" cy="11" r="2"/>'),
    "kitchen": icon('<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 10h18M7 6.5h.01M11 6.5h.01M9 14v3M15 14v3"/>'),
    "store": icon('<path d="M3 9l1.5-5h15L21 9M3 9v11h18V9M3 9h18M9 20v-6h6v6"/>'),
}
STAR = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2.5l2.9 6.3 6.9.7-5.2 4.6 1.5 6.8L12 17.3l-6.1 3.6 1.5-6.8L2.2 9.5l6.9-.7z"/></svg>'
STARS = '<span class="stars" role="img" aria-label="Rated 4.7 out of 5">' + ("<i>" + STAR + "</i>") * 4 + '<i class="half">' + STAR + "</i></span>"
STARS_SM = STARS.replace('class="stars"', 'class="stars stars--sm"')

MARK = ('<svg class="mark" viewBox="0 0 64 64" aria-hidden="true">'
        '<rect x="8" y="17" width="23" height="23" fill="#5FAAE1"/>'
        '<rect x="33" y="25" width="15" height="15" fill="#5FAAE1" opacity=".9"/>'
        '<rect x="18" y="41" width="13" height="13" fill="#5FAAE1" opacity=".85"/>'
        '<path d="M32 3v37M3 40.5h55" stroke="#3C8FCB" stroke-width="1.6"/></svg>')

def logo(light=False):
    return (f'<a class="logo{" logo--light" if light else ""}" href="~/" aria-label="Cut to Size Mirrors — home">{MARK}'
            '<span class="logo__text"><span class="logo__name">CutToSizeMirrors</span><span class="logo__tld">.co.uk</span></span></a>')

# ---------------------------------------------------------------- layout
NAV = [
    ("Mirrors", MIRROR, "mirror"),
    ("Glass", GLASS, "glass"),
    ("Splashbacks", SPLASH, "splash"),
    ("Gym & Studio", "~/gym-studio-mirrors/", "gym"),
    ("Fitting", "~/fitting/", "fitting"),
    ("Trade", "~/trade/", "trade"),
    ("FAQ", "~/faq/", "faq"),
]
DRAWER_EXTRA = [("How to measure", "~/how-to-measure/", "measure"), ("About us", "~/about/", "about"), ("Contact us", "~/contact-us/", "contact")]

def nav_links(items, active):
    cur = ' aria-current="page"'
    return "".join(f'<a href="{h}"{cur if k == active else ""}>{l}</a>' for l, h, k in items)

def header(active):
    return f"""
<a class="skip" href="#main">Skip to content</a>
<div class="topbar">
  <div class="wrap">
    <p class="topbar__msg mb-0">{I['truck']}<span>Delivered across UK mainland in 14 working days. <a href="~/fitting/">Fitting available</a> — ask for a quote.</span></p>
    <div class="topbar__right">
      <a class="tp-mini" href="{TRUSTPILOT}" rel="noopener" target="_blank">{STARS_SM}<span><strong>4.7</strong> Excellent on Trustpilot</span></a>
      <a href="{TEL}">{PHONE}</a>
    </div>
  </div>
</div>
<header class="header">
  <div class="wrap">
    {logo()}
    <nav class="nav" aria-label="Main">{nav_links(NAV, active)}</nav>
    <div class="header__actions">
      <a class="header__phone" href="{TEL}"><small>Need help? Call us</small><strong>{PHONE}</strong></a>
      <a class="icon-btn" href="~/basket/" aria-label="Basket">{I['basket']}<span class="badge" data-basket-count hidden>0</span></a>
      <a class="btn btn--cta" href="{MIRROR}">Get a price</a>
      <button class="icon-btn menu-btn" type="button" aria-label="Open menu" aria-controls="drawer" aria-expanded="false" data-open-drawer>{I['menu']}</button>
    </div>
  </div>
</header>
<div class="drawer" id="drawer" aria-hidden="true">
  <div class="drawer__scrim" data-close-drawer></div>
  <div class="drawer__panel" role="dialog" aria-modal="true" aria-label="Menu">
    <div class="drawer__top">{logo()}<button class="icon-btn" type="button" aria-label="Close menu" data-close-drawer>{I['close']}</button></div>
    <nav aria-label="Mobile">{nav_links(NAV + DRAWER_EXTRA, active)}</nav>
    <div class="drawer__foot">
      <a class="btn btn--block" href="{MIRROR}">Get an instant price</a>
      <a class="btn btn--ghost btn--block" href="{TEL}">{I['phone']} Call {PHONE}</a>
      <p>Mon–Fri · Unit C27, Market Drayton</p>
    </div>
  </div>
</div>
"""

FOOTER = f"""
<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">
      <div class="footer__about">
        {logo(light=True)}
        <p>We specialise in made-to-measure mirrors and bespoke glass for homes, interiors and businesses across the UK. As a family-run company we take pride in precision craftsmanship, personal service and reliable delivery.</p>
        <a class="tp-mini" href="{TRUSTPILOT}" rel="noopener" target="_blank">{STARS_SM}<span>4.7 Excellent · Trustpilot</span></a>
      </div>
      <div>
        <h2>Shop</h2>
        <ul>
          <li><a href="{MIRROR}">Made to measure mirrors</a></li>
          <li><a href="{GLASS}">Toughened glass</a></li>
          <li><a href="{SPLASH}">Glass splashbacks</a></li>
          <li><a href="~/gym-studio-mirrors/">Gym &amp; studio mirrors</a></li>
          <li><a href="~/basket/">Your basket</a></li>
        </ul>
      </div>
      <div>
        <h2>Help</h2>
        <ul>
          <li><a href="~/how-to-measure/">How to measure</a></li>
          <li><a href="~/fitting/">Measure &amp; fit service</a></li>
          <li><a href="~/trade/">Trade &amp; commercial</a></li>
          <li><a href="~/faq/">FAQs</a></li>
          <li><a href="~/about/">About us</a></li>
        </ul>
      </div>
      <div>
        <h2>Contact</h2>
        <ul>
          <li><a href="{TEL}">{PHONE}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>Unit C27 Rosehill Industrial Estate,<br>Market Drayton, TF9 2JU</li>
          <li><a href="~/contact-us/">Send us a message</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__bottom">
      <span>© <span data-year>2026</span> Cut to Size Mirrors &amp; Glass. All rights reserved.</span>
      <div class="pay" aria-label="Payment methods accepted"><span>VISA</span><span>Visa Debit</span><span>Mastercard</span><span>Maestro</span><span>🔒 takepayments</span></div>
    </div>
  </div>
</footer>
<div class="mobile-bar">
  <a class="btn btn--ghost" href="{TEL}">{I['phone']} Call</a>
  <a class="btn" href="{MIRROR}">Get a price</a>
</div>
"""

LOCAL_BUSINESS = {
    "@context": "https://schema.org", "@type": "HomeAndConstructionBusiness",
    "@id": DOMAIN + "/#business", "name": "Cut to Size Mirrors & Glass", "url": DOMAIN + "/",
    "telephone": "+44 1630 638389", "email": EMAIL, "logo": DOMAIN + "/assets/img/logo.svg",
    "image": DOMAIN + "/assets/img/og-image.png",
    "description": "Family-run UK company making made-to-measure mirrors, toughened glass and coloured glass splashbacks, with UK mainland delivery and fitting.",
    "address": {"@type": "PostalAddress", "streetAddress": "Unit C27 Rosehill Industrial Estate",
                "addressLocality": "Market Drayton", "postalCode": "TF9 2JU", "addressCountry": "GB"},
    "areaServed": "GB", "priceRange": "££",
}

INTRO = """<div class="intro" aria-hidden="true">
  <div class="intro__half intro__half--top"></div><div class="intro__half intro__half--bot"></div>
  <div class="intro__logo">
    <svg viewBox="0 0 64 64"><rect class="sq sq1" x="8" y="17" width="23" height="23"/><rect class="sq sq2" x="33" y="25" width="15" height="15"/><rect class="sq sq3" x="18" y="41" width="13" height="13"/><path class="ln ln1" d="M32 3v37"/><path class="ln ln2" d="M3 40.5h55"/></svg>
    <span>Cut to Size <b>Mirrors</b></span>
  </div>
  <div class="intro__cut"></div>
</div>"""

def page(path, title, desc, body, active="", scripts=(), schema=(), body_class="has-mobile-bar"):
    depth = path.count("/")
    rel = "../" * depth if depth else "./"
    url = DOMAIN + "/" + (path.rsplit("index.html", 1)[0] if path.endswith("index.html") else path)
    if path == "404.html":
        rel = "/"
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schema)
    js = "".join(f'<script src="~/assets/js/{s}" defer></script>' for s in ("config.js", "site.js", "motion.js") + tuple(scripts))
    intro = INTRO
    html = f"""<!DOCTYPE html>
<html lang="en-GB" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#ffffff">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Cut to Size Mirrors &amp; Glass">
<meta property="og:locale" content="en_GB">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}/assets/img/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="~/assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="~/assets/img/apple-touch-icon.png">
<link rel="manifest" href="~/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Poppins:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="~/assets/css/site.css">
{ld}
<script>try{{if(sessionStorage.getItem('ctsm-intro')||matchMedia('(prefers-reduced-motion: reduce)').matches)document.documentElement.classList.add('intro-skip');sessionStorage.setItem('ctsm-intro','1')}}catch(e){{}}</script>
{js}
</head>
<body class="{body_class}">
<div class="scroll-progress" aria-hidden="true"></div>
{intro if path == "index.html" else ""}
{header(active)}
<main id="main">
{body}
</main>
{FOOTER}
</body>
</html>
"""
    html = html.replace('href="~/"', f'href="{rel}"').replace("~/", rel)
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return url

# ---------------------------------------------------------------- shared blocks
def crumbs(*items):
    li = "".join(f'<li><a href="{h}">{l}</a></li>' if h else f'<li aria-current="page">{l}</li>' for l, h in items)
    return f'<ol class="crumbs">{li}</ol>'

USPS = f"""
<section class="usp-strip" aria-label="Why customers choose us">
  <ul class="wrap">
    <li><span class="usp-ico">{I['cut']}</span><span><strong>Cut in-house</strong>To the exact millimetre</span></li>
    <li><span class="usp-ico">{I['truck']}</span><span><strong>14 working days</strong>UK mainland delivery</span></li>
    <li><span class="usp-ico">{I['tool']}</span><span><strong>Measure &amp; fit</strong>Across 18 counties</span></li>
    <li><span class="usp-ico">{I['star']}</span><span><strong>4.7 on Trustpilot</strong>Rated Excellent</span></li>
    <li><span class="usp-ico">{I['lock']}</span><span><strong>Secure checkout</strong>Cheapest online price guaranteed</span></li>
  </ul>
</section>"""

def fitting_cta(heading="Want it measured and fitted?"):
    return f"""
<section class="section section--tight">
  <div class="wrap">
    <div class="cta-dark reveal">
      <div class="cta-dark__grid">
        <div>
          <p class="eyebrow">Measure · deliver · fit</p>
          <h2>{heading}</h2>
          <p class="lead">Tell us about your project and where you are, and we'll come back with a tailored quote — from a single bathroom mirror to a full gym wall.</p>
          <div class="cta-dark__btns">
            <a class="btn btn--light btn--lg" href="~/fitting/">Get your fitting quote</a>
            <a class="btn btn--outline-light btn--lg" href="{TEL}">{I['phone']} {PHONE}</a>
          </div>
        </div>
        <div>
          <p class="label" style="color:#fff;margin-bottom:12px">We fit across</p>
          <ul class="chips" data-fitting-areas></ul>
        </div>
      </div>
    </div>
  </div>
</section>"""

REVIEWS = [
    ("Bespoke mirrors for our new-build in Bedfordshire. The install team were professional, friendly and left everything very neat and tidy.", "New-build, Bedfordshire"),
    ("Wasn't sure on sizing for our bathroom and WC, so I called — they came out and measured for us.", "Bathroom &amp; WC"),
    ("Glass balustrade installed efficiently and carefully, spotless afterwards, and great communication throughout.", "Glass balustrade"),
    ("Cut-to-size mirror at a reasonable price. The team rang ahead to check the fittings and it was delivered on time.", "Cut-to-size mirror"),
]

def reviews_block():
    cards = "".join(f'<article class="review reveal">{STARS_SM}<p>{t}</p><footer>{w} · via Trustpilot</footer></article>' for t, w in REVIEWS)
    # TODO(client): swap this block for the official Trustpilot TrustBox widget once the business ID is available.
    return f"""
<section class="section section--soft" id="reviews">
  <div class="wrap">
    <div class="section__head">
      <p class="eyebrow">Reviews</p>
      <h2>Customers rate us Excellent</h2>
    </div>
    <div class="reviews">
      <div class="tp-score reveal">
        <div class="tp-logo">{STAR.replace('<svg', '<svg style="color:var(--star)"')} Trustpilot</div>
        <div class="tp-score__big" data-count="4.7" data-decimals="1">4.7</div>
        <div style="margin-top:10px">{STARS}</div>
        <p>Rated <strong>Excellent</strong> from 26 reviews by homeowners, developers and businesses.</p>
        <a class="btn btn--ghost btn--block" href="{TRUSTPILOT}" rel="noopener" target="_blank">Read all reviews</a>
      </div>
      <div class="review-list">{cards}</div>
    </div>
  </div>
</section>"""

def faq_items(items):
    return "".join(f'<details><summary>{q}</summary><div class="faq__a"><p>{a}</p></div></details>' for q, a in items)

def faq_schema(items):
    import re
    strip = lambda s: re.sub(r"<[^>]+>", "", s).replace("&amp;", "&")
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in items]}

FAQ = {
    "Ordering & pricing": [
        ("Can I order a mirror cut to any size?", f"Yes. Every mirror is cut to your exact dimensions. Enter your width and height in our <a href=\"{MIRROR}\">mirror calculator</a>, choose your options and the price updates instantly. The largest single sheet is 2400 × 1300mm."),
        ("Do you offer glass cut to size?", f"Yes — toughened glass for shelving, tabletops, balustrades, shower screens and more, all made to measure with polished edges. <a href=\"{GLASS}\">Price your glass</a>."),
        ("Can I get an instant quote online?", "Yes. Pick a product, enter your dimensions and the price updates automatically as you type, with the area shown in m² next to it."),
        ("Do you supply made to measure splashbacks?", f"Yes. Our 6mm toughened coloured glass splashbacks are cut to your exact size for kitchens or bathrooms, in any RAL, Dulux, Crown, Laura Ashley or Farrow &amp; Ball colour. <a href=\"{SPLASH}\">Get a splashback quote</a>."),
        ("I'm not sure of my measurements — what should I do?", "Have a look at our <a href=\"~/how-to-measure/\">how to measure guide</a>. If you're still unsure, give us a call on " + PHONE + " — we can also come out and measure for you."),
    ],
    "Delivery & fitting": [
        ("How long does delivery take?", "Orders are delivered within 14 working days. We cut all our own glass in-house, which keeps lead times reliable."),
        ("How much is delivery?", "We deliver to the whole of UK mainland. Delivery costs are added at checkout, based on your order and location."),
        ("Do you offer delivery and fitting?", "Yes — choose delivery only, delivery and fitting, or our full measure, delivery and fitting service. Fitting is priced by quote depending on your location and the job."),
        ("What areas do you cover for fitting?", "We deliver UK-wide, and fit across Cheshire, Denbighshire, Derbyshire, East Midlands, Essex, Flintshire, Greater London, Greater Manchester, Lancashire, Leicestershire, Merseyside, Oxfordshire, Shropshire, Staffordshire, Surrey, Warwickshire, West Midlands and Worcestershire. <a href=\"~/fitting/\">Ask for a fitting quote</a>."),
    ],
    "Choosing & fixing": [
        ("Which thickness should I choose?", "6mm is perfect for bathroom and gym mirrors. 4mm is better for smaller framed mirrors and is available in silver only."),
        ("What thickness is best for a gym or dance studio?", "6mm mirror, ideally with foil safety backing. It's sturdier on large walls, and the backing helps the mirror meet BS6206 Class C for high-traffic spaces."),
        ("What is foil safety backing?", "A protective safety layer on the back of the mirror that also shields the silver coating from moisture and salt damage. It works with mirror adhesives and helps mirrors meet the BS6206 Class C safety standard, which building regulations often require in public and commercial areas, kitchens, bathrooms and busy spaces. Note that foil backing isn't the same as plastic backing — plastic films shouldn't be used on wall mirrors, as the chemicals can react and the mirror can separate from the adhesive."),
        ("How should I fix my mirror to the wall?", "For most jobs, mirror adhesive is the safest, strongest and simplest fixing — allow one tube per m². Holes and screws are also available (holes are positioned 50mm from the edges, with standard 1¼″ screws), but we don't recommend them for mirrors over 1 m²."),
        ("Can you cut holes or sockets in splashbacks?", "Get in touch with your socket and switch positions and we'll advise on what's possible for your splashback."),
    ],
}
FAQ_ALL = [x for v in FAQ.values() for x in v]

def use_tiles():
    tiles = [
        ("Bathrooms", "Moisture-ready, foil-backed", "bath", "linear-gradient(135deg,#6f97b6,#23405a)", MIRROR),
        ("Gyms", "Full walls, seamed panels", "gym", "linear-gradient(135deg,#566272,#141a22)", "~/gym-studio-mirrors/"),
        ("Dance studios", "Floor-to-ceiling, safety backed", "dance", "linear-gradient(135deg,#8497ab,#27374a)", "~/gym-studio-mirrors/"),
        ("Bedrooms &amp; wardrobes", "Doors, alcoves and dressing", "bed", "linear-gradient(135deg,#b59d84,#574535)", MIRROR),
        ("Kitchens", "Coloured glass splashbacks", "kitchen", "linear-gradient(135deg,#579a84,#1d473b)", SPLASH),
        ("Commercial", "Washrooms, retail, hotels", "store", "linear-gradient(135deg,#4679aa,#0d2240)", "~/trade/"),
    ]
    thin = lambda svg: svg.replace('stroke-width="1.8"', 'stroke-width="1.3"')
    return "".join(f'<a class="use reveal" href="{h}" style="--g:{g}">{thin(I[i])}<h3>{t}</h3><p>{s}</p></a>' for t, s, i, g, h in tiles)

def product_cards():
    return f"""
<div class="grid grid--3">
  <a class="pcard reveal" href="{MIRROR}">
    <div class="pcard__art"><div class="art art--mirror"><div class="pane"></div><div class="basin"></div></div><span class="art-tag">Silver · Bronze · Grey</span></div>
    <div class="pcard__body"><h3>Mirrors</h3><p>4mm &amp; 6mm, polished or 25mm bevel edge, foil safety backing and fixings.</p>
      <div class="pcard__foot"><span class="pcard__price">From £44 <small>/m²</small></span><span class="pcard__go">{I['arrow']}</span></div></div>
  </a>
  <a class="pcard reveal" href="{GLASS}">
    <div class="pcard__art"><div class="art art--glass"><div class="shelf"></div><div class="shelf"></div><div class="shelf"></div></div><span class="art-tag">Toughened · polished edges</span></div>
    <div class="pcard__body"><h3>Glass</h3><p>6, 8 &amp; 10mm toughened glass for shelves, tabletops, shower screens and balustrades.</p>
      <div class="pcard__foot"><span class="pcard__price">From £95 <small>/m²</small></span><span class="pcard__go">{I['arrow']}</span></div></div>
  </a>
  <a class="pcard reveal" href="{SPLASH}">
    <div class="pcard__art"><div class="art art--splash"><span class="pendant" style="left:30%"></span><span class="pendant" style="left:68%"></span><div class="worktop"></div><div class="tap"></div></div><span class="art-tag">Any colour</span></div>
    <div class="pcard__body"><h3>Splashbacks</h3><p>6mm toughened coloured glass in any RAL, Dulux, Crown, Laura Ashley or Farrow &amp; Ball shade.</p>
      <div class="pcard__foot"><span class="pcard__price">Quote to your colour</span><span class="pcard__go">{I['arrow']}</span></div></div>
  </a>
</div>"""

TRADE_LOGOS = """<div class="logos" aria-label="Some of the businesses we supply">
  <span>Taylor Wimpey</span><span class="serif">MARKS &amp; SPENCER</span><span>Ladbrokes</span><span>McCarthy Stone</span><span>Miller Homes</span>
</div>"""

# ---------------------------------------------------------------- pages
def home():
    body = f"""
<section class="hero">
  <div class="wrap hero__grid">
    <div>
      <p class="eyebrow rise" style="--d:0">Family-run · Cut in Market Drayton</p>
      <h1 class="words"><span class="w"><span style="--i:0">Custom</span></span> <span class="w"><span style="--i:1">mirrors</span></span> <em><span class="w"><span style="--i:2">cut</span></span> <span class="w"><span style="--i:3">to</span></span> <span class="w"><span style="--i:4">size</span></span></em><span class="w"><span style="--i:5">,</span></span> <span class="w"><span style="--i:6">made</span></span> <span class="w"><span style="--i:7">to</span></span> <span class="w"><span style="--i:8">measure</span></span> <span class="w"><span style="--i:9">in</span></span> <span class="w"><span style="--i:10">the</span></span> <span class="w"><span style="--i:11">UK</span></span></h1>
      <p class="lead rise" style="--d:5">Enter your dimensions and get an accurate price in seconds. Every mirror is cut to your exact size — you choose the width, height, thickness and finish. Perfect for bathrooms, bedrooms, gyms and bespoke interiors.</p>
      <div class="hero__ctas rise" style="--d:6">
        <a class="btn btn--lg magnetic" href="{MIRROR}">Get an instant price {I['arrow']}</a>
        <a class="btn btn--ghost btn--lg" href="~/fitting/">Measure &amp; fit quote</a>
      </div>
      <div class="hero__proof rise" style="--d:7">
        <a class="proof-item" href="{TRUSTPILOT}" rel="noopener" target="_blank" style="text-decoration:none;color:inherit">{STARS_SM}<span><strong>4.7</strong> Excellent</span></a>
        <span class="proof-item">{I['truck']} Delivery in <strong>14 working days</strong></span>
        <span class="proof-item">{I['cut']} Cut <strong>in-house</strong></span>
      </div>
    </div>
    <div class="quote-stage rise rise--card" style="--d:3" data-tilt-stage>
      <div class="quote-stage__mirror" aria-hidden="true" data-parallax="-18"><span class="glint"></span></div>
      <span class="quote-stage__cross quote-stage__cross--v" aria-hidden="true"></span>
      <span class="quote-stage__cross quote-stage__cross--h" aria-hidden="true"></span>
      <form class="card-glass qp" data-quick-price onsubmit="return false">
        <h2>What size do you need?</h2>
        <p>Your price updates as you type.</p>
        <div class="tabs" role="tablist" aria-label="Product">
          <button type="button" role="tab" aria-selected="true" data-kind="mirror">Mirror</button>
          <button type="button" role="tab" aria-selected="false" tabindex="-1" data-kind="glass">Glass</button>
          <button type="button" role="tab" aria-selected="false" tabindex="-1" data-kind="splashback">Splashback</button>
        </div>
        <div class="qp__dims">
          <div class="field"><label for="qw">Width</label><div class="input-unit"><input class="input" id="qw" name="qw" type="number" inputmode="decimal" min="1" placeholder="1200"><span>mm</span></div></div>
          <span class="qp__x" aria-hidden="true">×</span>
          <div class="field"><label for="qh">Height</label><div class="input-unit"><input class="input" id="qh" name="qh" type="number" inputmode="decimal" min="1" placeholder="800"><span>mm</span></div></div>
        </div>
        <div class="qp__result" data-qp-out aria-live="polite"></div>
        <a class="btn btn--block btn--lg" href="{MIRROR}" data-qp-go data-mirror="{MIRROR}" data-glass="{GLASS}" data-splashback="{SPLASH}">Choose your options {I['arrow']}</a>
        <p class="qp__note">Starting price shown. Edging, backing and fixings on the next step.</p>
      </form>
    </div>
  </div>
</section>
{USPS}
<section class="section">
  <div class="wrap">
    <div class="section__head section__head--split">
      <div><p class="eyebrow">Made to measure</p><h2>Mirrors, glass &amp; splashbacks — priced instantly</h2></div>
      <p class="lead mb-0">Pick a product, enter your size, see your price. No waiting for a quote.</p>
    </div>
    {product_cards()}
  </div>
</section>
<section class="section section--soft">
  <div class="wrap">
    <div class="section__head section__head--center"><p class="eyebrow">How it works</p><h2>From your measurements to your wall</h2></div>
    <ol class="steps">
      <li class="reveal"><h3>Enter your size</h3><p>In mm, cm or inches. See the area and price instantly.</p></li>
      <li class="reveal"><h3>Choose your options</h3><p>Colour, thickness, edge, safety backing and fixings.</p></li>
      <li class="reveal"><h3>Order securely</h3><p>Pay online with Visa, Mastercard or Maestro.</p></li>
      <li class="reveal"><h3>Delivered or fitted</h3><p>Within 14 working days — or let our team fit it.</p></li>
    </ol>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section__head section__head--split">
      <div><p class="eyebrow">Where our mirrors go</p><h2>Made for every room — and every gym wall</h2></div>
      <a class="link-arrow" href="~/gym-studio-mirrors/">Gym &amp; studio mirrors</a>
    </div>
    <div class="uses">{use_tiles()}</div>
  </div>
</section>
<section class="section section--soft">
  <div class="wrap split">
    <div class="reveal">
      <div class="photo" style="--g:linear-gradient(160deg,#e9eff5 0%,#c5d3e0 40%,#f3f7fa 55%,#a9bccd 100%)">
        <!-- TODO(client): replace with a real photo of your workshop or a finished job -->
        <div class="photo__badge"><span class="usp-ico">{I['cut']}</span><div><strong>Cut &amp; finished in-house</strong><span>Market Drayton, Shropshire</span></div></div>
      </div>
    </div>
    <div>
      <p class="eyebrow">Why order from us</p>
      <h2>A family business that cuts every piece itself</h2>
      <p class="lead">We're a family-run UK company specialising in made-to-measure mirrors and custom glass for homes, interiors and businesses. Every piece is cut to your exact size on precision equipment, with a focus on accuracy, consistency and a clean, professional finish.</p>
      <div class="pillars mt-2">
        <div class="pillar reveal"><span class="usp-ico">{I['users']}</span><h3>Family-run</h3><p>Years of experience in glass and glazing.</p></div>
        <div class="pillar reveal"><span class="usp-ico">{I['ruler']}</span><h3>Bespoke</h3><p>Made to your exact requirements.</p></div>
        <div class="pillar reveal"><span class="usp-ico">{I['heart']}</span><h3>Personal service</h3><p>Reliable, and always a real person to talk to.</p></div>
        <div class="pillar reveal"><span class="usp-ico">{I['sparkle']}</span><h3>Professional finish</h3><p>On every order, whatever the size.</p></div>
      </div>
    </div>
  </div>
</section>
<section class="section section--tight">
  <div class="wrap">
    <p class="center fine" style="margin-bottom:24px;text-transform:uppercase;letter-spacing:.12em;font-weight:600">Trusted by developers &amp; businesses</p>
    {TRADE_LOGOS}
  </div>
</section>
{reviews_block()}
{fitting_cta()}
<section class="section">
  <div class="wrap split" style="align-items:start">
    <div>
      <p class="eyebrow">FAQ</p>
      <h2>Good questions, quick answers</h2>
      <p class="lead">Still unsure? Call us on <a href="{TEL}">{PHONE}</a> — we're happy to help you choose.</p>
      <a class="link-arrow" href="~/faq/">See all FAQs</a>
    </div>
    <div class="faq">{faq_items(FAQ["Ordering & pricing"][:3] + FAQ["Delivery & fitting"][:2] + FAQ["Choosing & fixing"][:1])}</div>
  </div>
</section>
"""
    return page("index.html", "Custom Mirrors Made to Measure | Cut to Size Mirrors UK",
                "Order custom mirrors made to measure, cut to size glass and splashbacks online with instant quotes and UK delivery. Fast, simple service.",
                body, "home", schema=[LOCAL_BUSINESS])


def configurator(kind):
    """Shared configurator page layout. Option cards are filled in from config.js."""
    unit_toggle = '<div class="unit-toggle" role="radiogroup" aria-label="Units">' + "".join(
        f'<label><input type="radio" name="unit" value="{u}"{" checked" if u == "mm" else ""}><span>{u.upper() if u != "in" else "INCHES"}</span></label>' for u in ("mm", "cm", "in")) + "</div>"
    step = [0]
    def title(t, small=""):
        step[0] += 1
        return f'<legend class="opt-title"><span><span class="step-n">{step[0]}</span>{t}</span>{f"<small>{small}</small>" if small else ""}</legend>'

    sizes = {"mirror": "Max 2400 × 1300mm", "glass": "Max 2400 × 1300mm", "splashback": "Max 2500 × 1300mm"}[kind]
    size_group = f"""
<fieldset class="opt-group">
  {title("Your size", sizes)}
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;gap:12px;flex-wrap:wrap"><span class="fine">Enter width × height</span>{unit_toggle}</div>
  <div class="dims">
    <div class="field"><label for="width">Width</label><div class="input-unit"><input class="input" id="width" name="width" type="number" inputmode="decimal" min="1" step="1" placeholder="e.g. 1200" required><span data-unit-label>mm</span></div></div>
    <div class="field"><label for="height">Height</label><div class="input-unit"><input class="input" id="height" name="height" type="number" inputmode="decimal" min="1" step="1" placeholder="e.g. 800" required><span data-unit-label>mm</span></div></div>
  </div>
  <p class="size-msg err" data-size-msg role="alert" hidden></p>
  <p class="fine" style="margin:10px 0 0">Not sure? <a href="~/how-to-measure/">How to measure</a> in 2 minutes.</p>
</fieldset>"""

    if kind == "mirror":
        groups = size_group + f"""
<fieldset class="opt-group">
  {title("Mirror colour")}
  <div class="opts opts--3" data-opts="type"></div>
  <p class="help" data-type-note hidden>Bronze and grey mirror come in 6mm with a polished edge.</p>
</fieldset>
<fieldset class="opt-group">
  {title("Thickness")}
  <div class="opts opts--2" data-opts="thickness"></div>
  <div class="help"><details><summary>Which thickness?</summary><div class="help__body"><p>6mm is perfect for bathroom and gym mirrors. 4mm is better for framed mirrors, and comes in silver only.</p><p>For larger jobs that need screws, use 6mm rather than 4mm.</p></div></details></div>
</fieldset>
<fieldset class="opt-group">
  {title("Edge finish")}
  <div class="opts opts--2" data-opts="edging"></div>
</fieldset>
<fieldset class="opt-group">
  {title("Safety backing", "Recommended")}
  <div class="opts opts--2" data-opts="backing"></div>
  <div class="help"><details><summary>What is foil safety backing?</summary><div class="help__body">
    <p>A protective safety layer that also shields the silver coating from moisture and salt damage. It works with mirror adhesives and lets mirrors meet the <strong>BS6206 Class C</strong> safety standard — often needed under building regulations in public and commercial areas, kitchens, bathrooms and busy spaces.</p>
    <p class="callout"><span><strong>Foil isn't plastic.</strong> Plastic films shouldn't be used on wall mirrors — the chemicals can react and the mirror can separate from the adhesive.</span></p>
  </div></details></div>
</fieldset>
<fieldset class="opt-group">
  {title("Fixings")}
  <div class="opts opts--3" data-opts="fixings"></div>
  <div class="tube-helper" data-tube-helper hidden><span data-tube-text></span><button type="button" data-use-tubes>Use</button></div>
  <p class="size-msg warn" data-fix-msg hidden></p>
  <div class="help"><details><summary>Adhesive or screws?</summary><div class="help__body">
    <p><strong>Mirror adhesive</strong> is the safest, strongest and simplest fixing for most jobs. Allow 1 tube per m².</p>
    <p><strong>Holes &amp; screws:</strong> holes are positioned 50mm from the mirror edges, with standard 1¼″ screws (other lengths and fittings available). We don't recommend screws on mirrors over 1 m².</p>
  </div></details></div>
</fieldset>"""
    elif kind == "glass":
        groups = size_group + f"""
<fieldset class="opt-group">
  {title("Glass thickness")}
  <div class="opts opts--3" data-opts="thickness"></div>
  <p class="help">All glass comes <strong>toughened with polished edges</strong> as standard.</p>
</fieldset>"""
    else:
        sw = [("RAL 9010 Pure White", "#f1ece1"), ("RAL 7016 Anthracite", "#383e42"), ("RAL 9005 Jet Black", "#0a0a0a"), ("RAL 5014 Pigeon Blue", "#637d96"),
              ("RAL 6021 Pale Green", "#89ac76"), ("RAL 3004 Purple Red", "#6d1f2b"), ("RAL 1015 Light Ivory", "#e6d2b5"), ("RAL 7035 Light Grey", "#cbd0cc")]
        swatches = "".join(f'<button type="button" class="swatch" style="--c:{h}" data-name="{n}" data-hex="{h}" aria-pressed="false" aria-label="{n}" title="{n}"></button>' for n, h in sw)
        groups = size_group + f"""
<fieldset class="opt-group">
  {title("Your colour")}
  <div class="colour-row">
    <div class="field"><label for="colour">Colour name or code</label><input class="input" id="colour" name="colour" type="text" autocomplete="off" placeholder="e.g. RAL 7016 or Farrow &amp; Ball Hague Blue" required></div>
    <div class="field"><span class="label" aria-hidden="true">Preview</span><span class="colour-pick"><input type="color" name="colourPick" value="#3f8a74" aria-label="Pick a preview colour"></span></div>
  </div>
  <p class="fine" style="margin:8px 0 0">Any RAL, Dulux, Crown, Laura Ashley or Farrow &amp; Ball colour. The preview is a guide — we match your code exactly.</p>
  <div class="swatches" aria-label="Popular colours">{swatches}</div>
</fieldset>
<fieldset class="opt-group" data-quote-fields hidden>
  {title("Where should we send your quote?")}
  <input type="hidden" name="_subject" value="Splashback quote request">
  <div class="form-grid">
    <div class="field"><label for="q-name">Name</label><input class="input" id="q-name" name="name" autocomplete="name" required></div>
    <div class="field"><label for="q-phone">Phone</label><input class="input" id="q-phone" name="phone" type="tel" autocomplete="tel"></div>
    <div class="field full"><label for="q-email">Email</label><input class="input" id="q-email" name="email" type="email" autocomplete="email" required></div>
  </div>
  <p class="form-status" role="status" hidden></p>
</fieldset>"""

    qty = '<div class="qty"><button type="button" data-qty="-1" aria-label="One fewer">−</button><input name="qty" value="1" inputmode="numeric" aria-label="Quantity"><button type="button" data-qty="1" aria-label="One more">+</button></div>'
    summary = f"""
<div class="summary">
  <div class="summary__top">
    <div><div class="summary__label">Your price</div><div class="summary__price is-empty" data-price aria-live="polite">Enter your size to see your price</div><div class="summary__vat" data-vat></div></div>
    <div class="summary__area">Area<strong data-area>—</strong></div>
  </div>
  <ul class="summary__lines" data-lines></ul>
  <div class="added" data-added hidden><span>{I['check'].replace('<svg', '<svg style="width:18px;height:18px;display:inline;vertical-align:-3px;margin-right:6px"')}<span data-added-text>Added</span></span><a href="~/basket/">View basket →</a></div>
  <div class="summary__actions">
    {qty}
    <button class="btn btn--lg" type="button" data-add disabled><span data-add-label>Add to basket</span></button>
    <p class="fine">{I['lock'].replace('<svg', '<svg style="width:14px;height:14px;display:inline;vertical-align:-2px"')} Secure checkout · Delivery within 14 working days · <a href="~/fitting/">Need fitting?</a></p>
  </div>
</div>"""

    preview = f"""
<div class="config__visual">
  <div class="preview" aria-hidden="true">
    <div class="preview__wall"></div>
    <div class="preview__stage">
      <div class="preview__piece is-empty" data-piece>
        <span class="preview__sheen"></span><span class="glint" style="mix-blend-mode:soft-light"></span>
        <span class="dim dim--w"><span data-dim-w>width</span></span>
        <span class="dim dim--h"><span data-dim-h>height</span></span>
      </div>
    </div>
    <div class="preview__caption"><span data-cap-desc></span><strong data-cap-area>—</strong></div>
  </div>
  <div class="trust-row">
    <div>{I['cut']}<span>Cut in-house to the millimetre</span></div>
    <div>{I['truck']}<span>Delivered in 14 working days</span></div>
    <div>{STARS_SM}<span>4.7 Excellent on Trustpilot</span></div>
    <div>{I['lock']}<span>Secure card payments</span></div>
  </div>
</div>"""
    if kind == "glass":
        preview = preview.replace('data-piece>', 'data-piece style="--piece:linear-gradient(135deg,rgba(214,238,241,.9),rgba(160,208,214,.75) 40%,rgba(226,245,247,.9) 60%,rgba(140,195,203,.8))">')
    return preview, groups, summary


def product_page(kind, path, name, h1, lead, title, desc, low, extra, crumb):
    preview, groups, summary = configurator(kind)
    body = f"""
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Home", "~/"), (crumb, None))}
    <p class="eyebrow">{name}</p>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
  </div>
</section>
<div class="wrap">
  <form class="config" data-config="{kind}" novalidate>
    {preview}
    <div>{groups}{summary}</div>
  </form>
</div>
{extra}
<div class="price-bar" aria-hidden="false">
  <div class="price-bar__p"><strong data-bar-price>Enter your size</strong><span data-bar-sub>Live price as you type</span></div>
  <button class="btn" type="button" data-add disabled><span data-add-label>Add to basket</span></button>
</div>
"""
    schema = [{"@context": "https://schema.org", "@type": "Product", "name": name, "description": desc,
               "brand": {"@type": "Brand", "name": "Cut to Size Mirrors & Glass"},
               "offers": {"@type": "AggregateOffer", "priceCurrency": "GBP", "lowPrice": low, "availability": "https://schema.org/MadeToOrder",
                          "seller": {"@id": DOMAIN + "/#business"}}}] if low else []
    return page(path, title, desc, body, {"mirror": "mirror", "glass": "glass", "splashback": "splash"}[kind], scripts=("configurator.js",), schema=schema, body_class="has-mobile-bar")


def product_pages():
    mirror_extra = f"""
<section class="section section--soft">
  <div class="wrap">
    <div class="section__head section__head--center"><p class="eyebrow">Good to know</p><h2>Choosing the right mirror</h2></div>
    <div class="grid grid--3">
      <div class="pillar reveal"><span class="usp-ico">{I['layers']}</span><h3>Size limits</h3><p>4mm silver and 6mm silver, grey &amp; bronze are cut from 2400 × 1300mm sheets. Bigger walls? We can join panels — <a href="{TEL}">call us</a>.</p></div>
      <div class="pillar reveal"><span class="usp-ico">{I['shield']}</span><h3>Safety first</h3><p>Foil backing helps your mirror meet BS6206 Class C — often required in bathrooms, kitchens, gyms and public areas.</p></div>
      <div class="pillar reveal"><span class="usp-ico">{I['drop']}</span><h3>Adhesive fixing</h3><p>Our recommended fixing for most jobs. Allow one tube per m² — the calculator suggests the right number for you.</p></div>
    </div>
  </div>
</section>
{fitting_cta("Rather we measured and fitted it?")}"""
    product_page("mirror", "product/custom-mirror/index.html", "Made to Measure Mirror",
                 "Your mirror, cut to the millimetre",
                 "Silver, bronze or grey mirror in 4mm or 6mm, with a polished or bevelled edge. Enter your size for an instant price.",
                 "Made to Measure Mirrors | Instant Price | Cut to Size Mirrors UK",
                 "Custom mirrors cut to your exact size. Silver, bronze or grey, 4mm or 6mm, polished or 25mm bevel edge, foil safety backing and fixings. Instant online price, UK delivery.",
                 "44.00", mirror_extra, "Mirrors")

    glass_extra = f"""
<section class="section section--soft">
  <div class="wrap">
    <div class="section__head section__head--center"><p class="eyebrow">Made for</p><h2>Toughened glass for every job</h2></div>
    <div class="grid grid--4">
      <div class="pillar reveal"><span class="usp-ico">{I['layers']}</span><h3>Shelving</h3><p>Clean, strong shelves with polished edges.</p></div>
      <div class="pillar reveal"><span class="usp-ico">{I['kitchen']}</span><h3>Tabletops</h3><p>Protective tops and full glass tables.</p></div>
      <div class="pillar reveal"><span class="usp-ico">{I['bath']}</span><h3>Shower screens</h3><p>Toughened for safety in wet rooms.</p></div>
      <div class="pillar reveal"><span class="usp-ico">{I['building']}</span><h3>Balustrades</h3><p>10mm for stairs, landings and decking.</p></div>
    </div>
  </div>
</section>
{fitting_cta("Need your glass fitted?")}"""
    product_page("glass", "product/custom-glass/index.html", "Made to Measure Glass",
                 "Toughened glass, cut to your size",
                 "6mm, 8mm or 10mm toughened glass with polished edges — for shelves, tabletops, shower screens and balustrades. Max 2400 × 1300mm.",
                 "Toughened Glass Cut to Size | Instant Price | Cut to Size Mirrors UK",
                 "Made to measure toughened glass with polished edges in 6mm, 8mm or 10mm. Shelving, tabletops, shower screens and balustrades. Instant online price and UK delivery.",
                 "95.00", glass_extra, "Glass")

    splash_extra = f"""
<section class="section section--soft">
  <div class="wrap split">
    <div class="reveal"><div class="photo photo--wide" style="--g:linear-gradient(180deg,#f7f6f3 0 38%,#3f8a74 38% 72%,#f1efea 72%)"><!-- TODO(client): real splashback job photo --></div></div>
    <div>
      <p class="eyebrow">Splashbacks</p>
      <h2>Any colour you can name</h2>
      <ul class="checks">
        <li>6mm toughened glass, cut to your exact size</li>
        <li>RAL, Dulux, Crown, Laura Ashley and Farrow &amp; Ball colours</li>
        <li>Up to 2500 × 1300mm in one piece</li>
        <li>For kitchens and bathrooms — easy to wipe clean</li>
      </ul>
      <p>Got sockets or switches in the way? Send us their positions and we'll advise.</p>
    </div>
  </div>
</section>
{fitting_cta("Want your splashback fitted?")}"""
    product_page("splashback", "product/made-to-measure-custom-splashback/index.html", "Coloured Glass Splashback",
                 "Glass splashbacks in any colour",
                 "6mm toughened coloured glass, cut to your exact size. Tell us your colour code and we'll match it.",
                 "Made to Measure Glass Splashbacks | Any Colour | Cut to Size Mirrors UK",
                 "Made to measure coloured glass splashbacks in 6mm toughened glass. Any RAL, Dulux, Crown, Laura Ashley or Farrow & Ball colour. Kitchens and bathrooms, UK delivery.",
                 None, splash_extra, "Splashbacks")


def quote_form(subject, product_default="", trade=False):
    opts = ["Mirrors", "Gym / studio mirror wall", "Toughened glass", "Splashback", "Shower screen", "Balustrade", "Something else"]
    options = "".join(f'<option{" selected" if o == product_default else ""}>{o}</option>' for o in opts)
    company = '<div class="field"><label for="f-company">Company</label><input class="input" id="f-company" name="company" autocomplete="organization"></div>' if trade else ""
    service = "" if trade else '<div class="field"><label for="f-service">Service</label><select class="select" id="f-service" name="service"><option>Measure, deliver &amp; fit</option><option>Deliver &amp; fit</option><option>Not sure yet</option></select></div>'
    return f"""
<form class="panel" data-enquiry novalidate>
  <input type="hidden" name="_subject" value="{subject}">
  <div class="form-grid">
    <div class="field"><label for="f-name">Name</label><input class="input" id="f-name" name="name" autocomplete="name" required></div>
    {company}
    <div class="field"><label for="f-phone">Phone</label><input class="input" id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
    <div class="field"><label for="f-email">Email</label><input class="input" id="f-email" name="email" type="email" autocomplete="email" required></div>
    <div class="field"><label for="f-postcode">Postcode</label><input class="input" id="f-postcode" name="postcode" autocomplete="postal-code" required></div>
    <div class="field"><label for="f-product">Product</label><select class="select" id="f-product" name="product">{options}</select></div>
    {service}
    <div class="field{' full' if trade else ''}"><label for="f-size">Rough size</label><input class="input" id="f-size" name="size" placeholder="e.g. 3 walls, 2400 × 1300 each"></div>
    <div class="field full"><label for="f-msg">Tell us about your project</label><textarea class="textarea" id="f-msg" name="message" placeholder="Where it's going, how many pieces, any deadlines…"></textarea></div>
    <div class="full"><button class="btn btn--lg btn--block" type="submit">Send my enquiry {I['arrow']}</button></div>
    <p class="fine full mb-0">Got photos of the space? Reply to our email with them — they help us quote accurately. We reply within one working day.</p>
    <p class="form-status full" role="status" hidden></p>
  </div>
</form>"""


def gym():
    body = f"""
<section class="page-hero">
  <div class="wrap split">
    <div>
      {crumbs(("Home", "~/"), ("Gym &amp; studio mirrors", None))}
      <p class="eyebrow">Gyms · Dance studios · Leisure centres</p>
      <h1>Gym &amp; studio mirror walls, measured and fitted</h1>
      <p class="lead">Floor-to-ceiling 6mm safety-backed mirror for home gyms, commercial gyms, dance and yoga studios. Order panels online or let us measure, deliver and fit the whole wall.</p>
      <div class="hero__ctas" style="margin-bottom:0">
        <a class="btn btn--lg" href="#quote">Get a wall quote</a>
        <a class="btn btn--ghost btn--lg" href="{MIRROR}?w=2400&amp;h=1300">Price a single panel</a>
      </div>
    </div>
    <div class="reveal"><div class="photo photo--wide" style="--g:linear-gradient(135deg,#566272,#141a22)"><!-- TODO(client): real gym wall photo -->
      <div class="photo__badge"><span class="usp-ico">{I['gym']}</span><div><strong>Full-wall installs</strong><span>Seamed panels, fitted in a day</span></div></div></div></div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section__head"><p class="eyebrow">The spec</p><h2>Built for busy, sweaty, high-traffic rooms</h2></div>
    <div class="grid grid--3">
      <div class="pillar reveal"><span class="usp-ico">{I['layers']}</span><h3>6mm mirror</h3><p>Sturdier on large walls and the right choice for gyms. Panels up to 2400 × 1300mm, joined neatly for full walls.</p></div>
      <div class="pillar reveal"><span class="usp-ico">{I['shield']}</span><h3>BS6206 Class C</h3><p>Foil safety backing holds glass together if broken and protects the silver from moisture — often required in public spaces.</p></div>
      <div class="pillar reveal"><span class="usp-ico">{I['drop']}</span><h3>Bonded, not screwed</h3><p>Mirror adhesive is the safest, strongest fixing for large panels — no holes to crack under vibration.</p></div>
      <div class="pillar reveal"><span class="usp-ico">{I['ruler']}</span><h3>We measure</h3><p>Uneven walls, sockets and skirting? Our team measures on site so everything lines up.</p></div>
      <div class="pillar reveal"><span class="usp-ico">{I['tool']}</span><h3>We fit</h3><p>Professional fitters across 18 counties, from Greater London to Merseyside.</p></div>
      <div class="pillar reveal"><span class="usp-ico">{I['building']}</span><h3>Commercial ready</h3><p>Trusted by developers and national brands. VAT receipts and trade accounts on request.</p></div>
    </div>
  </div>
</section>
<section class="section section--soft" id="quote">
  <div class="wrap split" style="align-items:start">
    <div>
      <p class="eyebrow">Free quote</p>
      <h2>Tell us about your wall</h2>
      <p class="lead">Give us rough sizes and your postcode and we'll come back with a price for supply, or supply and fit.</p>
      <ul class="checks"><li>Home gyms, garage gyms and commercial gyms</li><li>Dance, ballet, yoga and pilates studios</li><li>Leisure centres and schools</li></ul>
      <p>Prefer to talk? <a href="{TEL}">{PHONE}</a></p>
    </div>
    {quote_form("Gym / studio mirror quote", "Gym / studio mirror wall")}
  </div>
</section>
{reviews_block()}
"""
    page("gym-studio-mirrors/index.html", "Gym & Dance Studio Mirrors | Measured & Fitted | Cut to Size Mirrors",
         "Floor-to-ceiling gym and dance studio mirror walls in 6mm safety-backed mirror. Order panels online or get a measure, deliver and fit quote across 18 counties.",
         body, "gym")


def fitting():
    body = f"""
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Home", "~/"), ("Fitting", None))}
    <p class="eyebrow">Measure · deliver · fit</p>
    <h1>Let us measure and fit it for you</h1>
    <p class="lead">Not confident measuring, or it's a big job? Our team will measure on site, cut everything in our workshop and fit it — so it's right first time.</p>
  </div>
</section>
<section class="section section--tight">
  <div class="wrap">
    <div class="grid grid--3">
      <div class="pillar reveal"><span class="usp-ico">{I['truck']}</span><h3>Delivery only</h3><p>UK mainland. Order online and pay delivery at checkout.</p></div>
      <div class="pillar reveal"><span class="usp-ico">{I['tool']}</span><h3>Delivery + fitting</h3><p>You measure, we deliver and fit. Priced by quote.</p></div>
      <div class="pillar reveal" style="border-color:var(--accent);box-shadow:0 0 0 3px rgba(23,104,184,.1)"><span class="usp-ico">{I['ruler']}</span><h3>Full measure, delivery + fitting</h3><p>We handle everything, start to finish. Priced by quote.</p></div>
    </div>
  </div>
</section>
<section class="section section--soft">
  <div class="wrap split" style="align-items:start">
    <div>
      <p class="eyebrow">Coverage</p>
      <h2>Where we fit</h2>
      <p class="lead">We deliver to the whole of UK mainland and fit across these areas. Just outside? Ask anyway.</p>
      <ul class="chips" data-fitting-areas style="margin-bottom:28px"></ul>
      <div class="contact-cards">
        <a class="ccard" href="{TEL}"><span class="usp-ico">{I['phone']}</span><span><strong>{PHONE}</strong><span>Talk it through with us</span></span></a>
        <a class="ccard" href="mailto:{EMAIL}"><span class="usp-ico">{I['mail']}</span><span><strong>{EMAIL}</strong><span>Send photos and measurements</span></span></a>
      </div>
    </div>
    <div>
      <h2 style="font-size:1.4rem">Get your fitting quote</h2>
      {quote_form("Fitting quote request")}
    </div>
  </div>
</section>
{reviews_block()}
"""
    page("fitting/index.html", "Mirror & Glass Fitting | Measure & Fit Service | Cut to Size Mirrors",
         "Measure, delivery and fitting for made-to-measure mirrors, glass and splashbacks across Cheshire, Shropshire, Staffordshire, the Midlands, Greater Manchester, London and more.",
         body, "fitting")


def trade():
    body = f"""
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Home", "~/"), ("Trade &amp; commercial", None))}
    <p class="eyebrow">Trade &amp; commercial</p>
    <h1>Mirrors and glass for developers, gyms &amp; fit-outs</h1>
    <p class="lead">From new-build plots to washrooms and retail, we cut, deliver and fit consistent, high-quality glass on programme.</p>
  </div>
</section>
<section class="section section--tight">
  <div class="wrap">
    <p class="center fine" style="margin-bottom:24px;text-transform:uppercase;letter-spacing:.12em;font-weight:600">Trusted by</p>
    {TRADE_LOGOS}
  </div>
</section>
<section class="section section--soft">
  <div class="wrap">
    <div class="grid grid--4">
      <div class="pillar reveal"><span class="usp-ico">{I['building']}</span><h3>House builders</h3><p>Bathroom and wardrobe mirrors across whole developments.</p></div>
      <div class="pillar reveal"><span class="usp-ico">{I['gym']}</span><h3>Gyms &amp; leisure</h3><p>Full mirror walls with BS6206 safety backing.</p></div>
      <div class="pillar reveal"><span class="usp-ico">{I['store']}</span><h3>Retail &amp; hospitality</h3><p>Washrooms, changing rooms, hotels and bars.</p></div>
      <div class="pillar reveal"><span class="usp-ico">{I['tool']}</span><h3>Shopfitters</h3><p>Cut to your drawings, delivered ready to install.</p></div>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap split" style="align-items:start">
    <div>
      <p class="eyebrow">Why trade customers stay</p>
      <h2>Consistent, accurate and on time</h2>
      <ul class="checks">
        <li>All glass processed and cut in-house on precision equipment</li>
        <li>Measure, deliver and fit teams across 18 counties</li>
        <li>One point of contact from quote to handover</li>
        <li>Mirrors, toughened glass, splashbacks, shower screens and balustrades</li>
      </ul>
      <p>Send us drawings or a schedule and we'll price the whole job.</p>
    </div>
    {quote_form("Trade enquiry", trade=True)}
  </div>
</section>
"""
    page("trade/index.html", "Trade & Commercial Mirrors and Glass | Cut to Size Mirrors",
         "Made-to-measure mirrors and toughened glass for house builders, gyms, retail, hospitality and shopfitters. Cut in-house, delivered and fitted across the UK.",
         body, "trade")


MEASURE_SVG_W = """<svg viewBox="0 0 320 220" role="img" aria-label="Measure the width at the top, middle and bottom of the space">
  <rect x="40" y="20" width="240" height="180" rx="4" fill="#fff" stroke="#c4d0dc" stroke-width="2"/>
  <g stroke="#1768b8" stroke-width="2" marker-start="url(#a)" marker-end="url(#a)">
    <line x1="48" y1="45" x2="272" y2="45"/><line x1="48" y1="110" x2="272" y2="110"/><line x1="48" y1="175" x2="272" y2="175"/>
  </g>
  <g font-family="Poppins, sans-serif" font-size="12" font-weight="600" fill="#0f1b2a" text-anchor="middle">
    <rect x="130" y="34" width="60" height="20" rx="10" fill="#eaf4fc"/><text x="160" y="48">1202</text>
    <rect x="130" y="99" width="60" height="20" rx="10" fill="#eaf4fc"/><text x="160" y="113">1200</text>
    <rect x="130" y="164" width="60" height="20" rx="10" fill="#1768b8"/><text x="160" y="178" fill="#fff">1198 ✓</text>
  </g>
  <defs><marker id="a" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5 0 10z" fill="#1768b8"/></marker></defs>
</svg>"""
MEASURE_SVG_H = MEASURE_SVG_W.replace("width at the top, middle and bottom", "height at the left, middle and right").replace(
    '<line x1="48" y1="45" x2="272" y2="45"/><line x1="48" y1="110" x2="272" y2="110"/><line x1="48" y1="175" x2="272" y2="175"/>',
    '<line x1="80" y1="28" x2="80" y2="192"/><line x1="160" y1="28" x2="160" y2="192"/><line x1="240" y1="28" x2="240" y2="192"/>').replace(
    '<rect x="130" y="34" width="60" height="20" rx="10" fill="#eaf4fc"/><text x="160" y="48">1202</text>', '<rect x="52" y="60" width="56" height="20" rx="10" fill="#eaf4fc"/><text x="80" y="74">801</text>').replace(
    '<rect x="130" y="99" width="60" height="20" rx="10" fill="#eaf4fc"/><text x="160" y="113">1200</text>', '<rect x="130" y="100" width="60" height="20" rx="10" fill="#1768b8"/><text x="160" y="114" fill="#fff">798 ✓</text>').replace(
    '<rect x="130" y="164" width="60" height="20" rx="10" fill="#1768b8"/><text x="160" y="178" fill="#fff">1198 ✓</text>', '<rect x="212" y="140" width="56" height="20" rx="10" fill="#eaf4fc"/><text x="240" y="154">800</text>')


def measure():
    body = f"""
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Home", "~/"), ("How to measure", None))}
    <p class="eyebrow">Measuring guide</p>
    <h1>How to measure for a made-to-measure mirror</h1>
    <p class="lead">Two minutes and a tape measure is all it takes. Measure in millimetres if you can — it's the most accurate, and it's how we cut.</p>
  </div>
</section>
<section class="section section--tight">
  <div class="wrap measure-steps">
    <div class="measure-step reveal">
      <div><h3>Measure the width three times</h3><p>Measure across the top, middle and bottom of the space. Walls and alcoves are rarely perfectly square, so the three numbers are often slightly different.</p><p><strong>Use the smallest of the three.</strong></p></div>
      <figure>{MEASURE_SVG_W}</figure>
    </div>
    <div class="measure-step reveal">
      <div><h3>Measure the height three times</h3><p>Do the same on the left, middle and right. Again, use the smallest measurement so your mirror or glass fits without forcing.</p><p><strong>Width first, then height</strong> — that's the order our calculator asks for.</p></div>
      <figure>{MEASURE_SVG_H}</figure>
    </div>
    <div class="measure-step reveal">
      <div><h3>Check for obstacles</h3><p>Note any sockets, switches, pipes, taps or tiles that the glass needs to go around, and where they sit. For splashbacks, send us their positions and we'll advise.</p></div>
      <figure><ul class="checks" style="margin:0;padding:8px"><li>Plug sockets and switches</li><li>Taps and pipes</li><li>Skirting and coving</li><li>Tiles and window sills</li></ul></figure>
    </div>
    <div class="measure-step reveal">
      <div><h3>Check your max size</h3><p>Mirrors and toughened glass are cut from sheets up to <strong>2400 × 1300mm</strong>; splashbacks up to <strong>2500 × 1300mm</strong>. Bigger than that? We can join panels for a seamed finish — just call us.</p></div>
      <figure><ul class="checks" style="margin:0;padding:8px"><li>Mirrors: 2400 × 1300mm</li><li>Glass: 2400 × 1300mm</li><li>Splashbacks: 2500 × 1300mm</li></ul></figure>
    </div>
  </div>
</section>
<section class="section section--tight">
  <div class="wrap">
    <div class="cta-dark reveal">
      <div class="cta-dark__grid">
        <div><p class="eyebrow">Got your numbers?</p><h2>Get your price in seconds</h2><p class="lead">Or if you'd rather not measure at all, we'll come out and do it for you.</p></div>
        <div class="cta-dark__btns" style="margin:0"><a class="btn btn--light btn--lg" href="{MIRROR}">Price my mirror</a><a class="btn btn--outline-light btn--lg" href="~/fitting/">Book a measure</a></div>
      </div>
    </div>
  </div>
</section>
"""
    page("how-to-measure/index.html", "How to Measure for a Made to Measure Mirror | Cut to Size Mirrors",
         "A simple step-by-step guide to measuring for a made-to-measure mirror, glass or splashback. Measure three times, use the smallest, and check for obstacles.",
         body, "measure")


def about():
    body = f"""
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Home", "~/"), ("About us", None))}
    <p class="eyebrow">About us</p>
    <h1>Modern technology, traditional values</h1>
    <p class="lead">With years of experience in glass and glazing, we've built our reputation on craftsmanship, reliability and personal attention.</p>
  </div>
</section>
<section class="section">
  <div class="wrap split">
    <div class="reveal"><div class="photo" style="--g:linear-gradient(160deg,#e9eff5 0%,#c5d3e0 40%,#f3f7fa 55%,#a9bccd 100%)"><!-- TODO(client): team or workshop photo -->
      <div class="photo__badge"><span class="usp-ico">{I['pin']}</span><div><strong>Market Drayton, Shropshire</strong><span>Unit C27 Rosehill Industrial Estate</span></div></div></div></div>
    <div>
      <p class="eyebrow">Our story</p>
      <h2>A family business that treats every job as unique</h2>
      <p>We're a family-run company making mirrors and glass for homes, interiors and businesses across the UK. Every project is different, so every one gets a fully bespoke service — from a single bathroom mirror to a gym wall or a new-build development.</p>
      <p>We process and cut all our own glass in-house, combining modern precision equipment with traditional care. That's how we make mirrors, glass splashbacks, shower screens, balustrades, tabletops and more to your exact size, with a clean, professional finish.</p>
      <div class="grid grid--2 mt-2">
        <div class="pillar"><span class="usp-ico">{I['tool']}</span><h3>Supply, measure &amp; fit</h3><p>We measure on site, make it and fit it.</p></div>
        <div class="pillar"><span class="usp-ico">{I['ruler']}</span><h3>Made to measure</h3><p>Order online to your own sizes, delivered UK-wide.</p></div>
      </div>
    </div>
  </div>
</section>
{reviews_block()}
{fitting_cta("Let's talk about your project")}
"""
    page("about/index.html", "About Us | Family-Run Mirror & Glass Specialists | Cut to Size Mirrors",
         "Cut to Size Mirrors & Glass is a family-run company in Market Drayton making made-to-measure mirrors, toughened glass and splashbacks for homes and businesses across the UK.",
         body, "about")


def faq():
    sections = "".join(f'<h2 id="{k.split()[0].lower()}">{k.replace("&", "&amp;")}</h2><div class="faq">{faq_items(v)}</div>' for k, v in FAQ.items())
    nav = "".join(f'<a href="#{k.split()[0].lower()}">{k.replace("&", "&amp;")}</a>' for k in FAQ)
    body = f"""
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Home", "~/"), ("FAQ", None))}
    <p class="eyebrow">FAQ</p>
    <h1>Frequently asked questions</h1>
    <p class="lead">Everything you need to know about ordering made-to-measure mirrors and glass. Can't find your answer? Call <a href="{TEL}">{PHONE}</a>.</p>
  </div>
</section>
<section class="section section--tight">
  <div class="wrap faq-cats">
    <nav aria-label="FAQ sections">{nav}</nav>
    <div>{sections}</div>
  </div>
</section>
{fitting_cta("Still have a question?")}
"""
    page("faq/index.html", "FAQ | Made to Measure Mirrors & Glass | Cut to Size Mirrors",
         "Answers on ordering made-to-measure mirrors, glass and splashbacks: sizes, thickness, safety backing, fixings, delivery times and fitting areas.",
         body, "faq", schema=[faq_schema(FAQ_ALL)])


def contact():
    body = f"""
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Home", "~/"), ("Contact us", None))}
    <p class="eyebrow">Contact us</p>
    <h1>We're here to help</h1>
    <p class="lead">Questions about sizes, options or fitting? Call, email or send a message and a real person will get back to you.</p>
  </div>
</section>
<section class="section section--tight">
  <div class="wrap split" style="align-items:start">
    <div class="contact-cards">
      <a class="ccard" href="{TEL}"><span class="usp-ico">{I['phone']}</span><span><strong>{PHONE}</strong><span>The quickest way to reach us</span></span></a>
      <a class="ccard" href="mailto:{EMAIL}"><span class="usp-ico">{I['mail']}</span><span><strong>{EMAIL}</strong><span>We reply within one working day</span></span></a>
      <a class="ccard" href="https://www.google.com/maps/search/?api=1&amp;query=Unit+C27+Rosehill+Industrial+Estate+Market+Drayton+TF9+2JU" rel="noopener" target="_blank"><span class="usp-ico">{I['pin']}</span><span><strong>Unit C27 Rosehill Industrial Estate</strong><span>Market Drayton, TF9 2JU · Get directions</span></span></a>
      <a class="ccard" href="{TRUSTPILOT}" rel="noopener" target="_blank"><span class="usp-ico">{I['star']}</span><span><strong>4.7 Excellent on Trustpilot</strong><span>Read what our customers say</span></span></a>
    </div>
    <form class="panel" data-enquiry novalidate>
      <h2>Send us a message</h2>
      <input type="hidden" name="_subject" value="Website contact">
      <div class="form-grid">
        <div class="field"><label for="c-name">Name</label><input class="input" id="c-name" name="name" autocomplete="name" required></div>
        <div class="field"><label for="c-phone">Phone</label><input class="input" id="c-phone" name="phone" type="tel" autocomplete="tel"></div>
        <div class="field full"><label for="c-email">Email</label><input class="input" id="c-email" name="email" type="email" autocomplete="email" required></div>
        <div class="field full"><label for="c-msg">Message</label><textarea class="textarea" id="c-msg" name="message" required></textarea></div>
        <div class="full"><button class="btn btn--lg btn--block" type="submit">Send message {I['arrow']}</button></div>
        <p class="form-status full" role="status" hidden></p>
      </div>
    </form>
  </div>
</section>
"""
    page("contact-us/index.html", "Contact Us | Cut to Size Mirrors & Glass, Market Drayton",
         "Contact Cut to Size Mirrors & Glass on 01630 638389 or info@cuttosizemirrors.co.uk. Unit C27 Rosehill Industrial Estate, Market Drayton, TF9 2JU.",
         body, "contact", schema=[LOCAL_BUSINESS])


def basket():
    body = f"""
<section class="page-hero">
  <div class="wrap">
    {crumbs(("Home", "~/"), ("Basket", None))}
    <h1>Your basket</h1>
  </div>
</section>
<section class="section section--tight">
  <div class="wrap" data-basket>
    <div class="empty" data-empty hidden>
      <h2>Your basket is empty</h2>
      <p class="lead" style="margin:0 auto 24px">Enter your size and get an instant price on any of our products.</p>
      <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap"><a class="btn" href="{MIRROR}">Mirrors</a><a class="btn btn--ghost" href="{GLASS}">Glass</a><a class="btn btn--ghost" href="{SPLASH}">Splashbacks</a></div>
    </div>
    <div class="basket" data-full hidden>
      <div>
        <div data-items></div>
        <p class="mt-2"><a class="link-arrow" href="{MIRROR}">Add another piece</a></p>
      </div>
      <div style="display:grid;gap:16px">
        <div class="panel"><h2>Order summary</h2><ul class="totals" data-totals></ul></div>
        <form class="panel" novalidate>
          <h2>Your details</h2>
          <input type="hidden" name="_subject" value="New order request">
          <div class="form-grid">
            <div class="field full"><label for="o-name">Full name</label><input class="input" id="o-name" name="name" autocomplete="name" required></div>
            <div class="field"><label for="o-email">Email</label><input class="input" id="o-email" name="email" type="email" autocomplete="email" required></div>
            <div class="field"><label for="o-phone">Phone</label><input class="input" id="o-phone" name="phone" type="tel" autocomplete="tel" required></div>
            <div class="field full"><label for="o-address">Delivery address</label><textarea class="textarea" id="o-address" name="address" autocomplete="street-address" style="min-height:90px" required></textarea></div>
            <div class="field"><label for="o-postcode">Postcode</label><input class="input" id="o-postcode" name="postcode" autocomplete="postal-code" required></div>
            <div class="field"><label for="o-service">Service</label><select class="select" id="o-service" name="service"><option>Delivery only</option><option>Delivery + fitting (quote)</option></select></div>
            <div class="full"><button class="btn btn--lg btn--block" type="submit">{I['lock']} Place order request</button></div>
            <p class="fine full mb-0">We'll confirm your delivery cost and send a secure card payment link. Nothing is charged until you approve it. Delivery within 14 working days of payment.</p>
            <p class="form-status full" role="status" hidden></p>
          </div>
        </form>
      </div>
    </div>
  </div>
</section>
"""
    page("basket/index.html", "Your Basket | Cut to Size Mirrors", "Your made-to-measure mirror and glass order.", body, "", scripts=("basket.js",))


def not_found():
    body = f"""
<section class="page-hero" style="padding:clamp(80px,12vw,160px) 0">
  <div class="wrap center">
    <p class="eyebrow" style="justify-content:center">404</p>
    <h1 style="margin:0 auto 16px">This page has been cut</h1>
    <p class="lead" style="margin:0 auto 28px">We couldn't find that page. Try one of these instead.</p>
    <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap"><a class="btn" href="{MIRROR}">Price a mirror</a><a class="btn btn--ghost" href="~/">Home</a><a class="btn btn--ghost" href="~/contact-us/">Contact</a></div>
  </div>
</section>"""
    page("404.html", "Page not found | Cut to Size Mirrors", "Page not found.", body)


if __name__ == "__main__":
    home(); product_pages(); gym(); fitting(); trade(); measure(); about(); faq(); contact(); basket(); not_found()
    urls = ["", "product/custom-mirror/", "product/custom-glass/", "product/made-to-measure-custom-splashback/",
            "gym-studio-mirrors/", "fitting/", "trade/", "how-to-measure/", "about/", "faq/", "contact-us/"]
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{DOMAIN}/{u}</loc></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
    print("Built", len(urls) + 2, "pages")
