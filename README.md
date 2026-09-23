# CutToSizeMirrors.co.uk — rebuild

A custom-coded static site for **Cut to Size Mirrors & Glass**, built from the rebuild brief. It uses no framework and no build tools beyond one Python script, and needs no WordPress. It's fast, mobile-first, and works on any static host (Netlify, Cloudflare Pages, Vercel, or plain Apache/Nginx).

## Preview locally

```bash
cd cuttosizemirrors
python3 -m http.server 8000     # then open http://localhost:8000
```

## How it's put together

| File | What it does |
|---|---|
| `assets/js/config.js` | **All prices, size limits, fitting areas and contact details.** Change a number, re-upload, done. |
| `build.py` | Holds the shared header, footer, `<head>` and every page's content. Edit it, then run `python3 build.py` to regenerate the HTML. |
| `assets/css/site.css` | The design system: colours, type and components. |
| `assets/js/site.js` | Header, mobile menu, basket count, homepage quick price, forms. |
| `assets/js/configurator.js` | Live price calculators for mirror, glass and splashback. |
| `assets/js/basket.js` | Basket page and order request. |
| `_redirects` | 301s from old WooCommerce URLs (Netlify/Cloudflare format). |

Product, About, FAQ and Contact pages keep their **existing URLs** (`/product/custom-mirror/`, `/about/`, `/faq/`, `/contact-us/` …), so rankings carry over.

## What's in it

- **Home**: hero with a live size-to-price widget, USP strip, product cards, how it works, use-case tiles, trade logos, reviews, fitting CTA and FAQ preview.
- **Mirror / Glass / Splashback configurators**:
  - Visual option cards instead of dropdowns.
  - Live price inc and ex VAT, with the area in m² shown next to it.
  - A to-scale preview that shows the colour and bevel.
  - Units in mm, cm or inches.
  - Max-size checks with a friendly "we can join panels" message.
  - Bronze and grey can't be combined with 4mm or bevel.
  - A glue-tube helper that suggests 1 tube per m².
  - A warning when screws are chosen for a mirror over 1 m².
  - A sticky price bar on mobile.
  - "Enter your size to see your price" shows instead of "£1.00".
- **Gym & Studio**, **Fitting**, **Trade**, **How to Measure**, **About**, **FAQ** (with FAQPage schema), **Contact**, **Basket** and a **404** page.
- Every item on the brief's "problems to fix" list is addressed:
  - Pinch-zoom works.
  - `og:locale` is `en_GB`.
  - The copyright year updates itself.
  - There is one CTA colour.
  - The mobile header is compact.
  - Help text sits inline under each option.
  - The typos are fixed.
- LocalBusiness and Product schema, a sitemap, robots.txt, the favicon and a social share image.

## Before launch — needs the client

1. **Pricing formula.** The site calculates `area × (type rate + edge rate) + flat add-ons`, then adds 20% VAT. Confirm this, plus any minimum charge (`minChargeArea` in config.js) and whether the headline prices are ex VAT.
2. **Splashback price per m².** Until `perM2` is set in config.js, that page collects a quote request instead of showing a price.
3. **Payments and checkout.** The basket currently sends an *order request*, and the business then confirms delivery and sends a takepayments link. For true online checkout, connect Stripe Checkout or takepayments. That needs a small server or serverless function.
4. **Where forms go.** Set `formEndpoint` in config.js (for example Formspree or Basin). Until then, forms open the visitor's email app with everything filled in.
5. **Real job photos.** The CSS-drawn scenes are placeholders. Search `TODO(client)` in `build.py` for every photo slot.
6. **Fitting county list** (config.js), and whether 5mm mirror or a bevel on bronze/grey exist.
7. **Trade logos.** Get permission to show them and the two unnamed logos. They're currently plain text wordmarks; swap in the SVG/PNG files.
8. **Reviews.** Swap the summarised snippets for the official Trustpilot TrustBox widget.
9. **Terms, Privacy, Delivery & Returns.** Port the existing text; the returns policy for made-to-order items is needed.
10. **The how-to-measure advice.** Have the client check it matches how they cut.
11. **Analytics.** Add GA4 and Search Console, with a UK cookie banner at the same time. There is no tracking yet, so no banner is needed yet.
12. **"Under new ownership".** Deliberately not mentioned anywhere until the client decides.
