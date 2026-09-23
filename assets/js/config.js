/* ==========================================================================
   Cut to Size Mirrors & Glass — SITE CONFIG
   --------------------------------------------------------------------------
   Every price, size limit and contact detail lives in this one file.
   Change a number here, save, re-upload — no other code needs touching.

   All money values are in pounds, EXCLUDING VAT.
   perM2  = charged per square metre of glass
   each   = flat charge per mirror/panel
   ========================================================================== */
window.CTSM = {
  business: {
    name: "Cut to Size Mirrors & Glass",
    phone: "01630 638389",
    phoneHref: "tel:+441630638389",
    email: "info@cuttosizemirrors.co.uk",
    address: "Unit C27 Rosehill Industrial Estate, Market Drayton, TF9 2JU"
  },

  // Where quote / contact / order forms are sent.
  // Leave empty to open the visitor's email app with everything filled in.
  // To receive them directly, paste a form endpoint here (e.g. Formspree,
  // Basin, or your own server) — the form data is POSTed to it.
  formEndpoint: "",

  vatRate: 0.20,

  // Smallest area charged per piece (m²). 0 = charge the exact area.
  // TODO(client): confirm minimum order / minimum area charge.
  minChargeArea: 0,

  products: {
    mirror: {
      title: "Made to Measure Mirror",
      minMM: 100,
      types: {
        silver: { label: "Silver", sub: "Classic clear reflection", perM2: 44.00, swatch: "linear-gradient(135deg,#fdfefe,#cfdbe6 35%,#f4f8fb 50%,#aebfcf 70%,#e7eef4)", thickness: ["4", "6"], edging: ["polished", "bevel"] },
        bronze: { label: "Bronze", sub: "Warm, tinted reflection", perM2: 172.00, swatch: "linear-gradient(135deg,#d9c3a5,#a88a66 35%,#d2bb9b 50%,#8e7254 70%,#c9b08e)", thickness: ["6"], edging: ["polished"] },
        grey:   { label: "Grey",   sub: "Smoked, contemporary", perM2: 172.00, swatch: "linear-gradient(135deg,#b9bec3,#7c848c 35%,#aab0b6 50%,#646c74 70%,#9aa1a8)", thickness: ["6"], edging: ["polished"] }
      },
      thickness: {
        "4": { label: "4mm", sub: "Ideal for small framed mirrors", maxLong: 2400, maxShort: 1300 },
        "6": { label: "6mm", sub: "Bathrooms & gym walls", maxLong: 2400, maxShort: 1300 }
      },
      defaultThickness: "6",
      edging: {
        polished: { label: "Polished edge", sub: "Clean, flat polished edge", perM2: 2.50 },
        bevel:    { label: "25mm bevel",    sub: "Angled frame-like border", perM2: 44.00 }
      },
      backing: {
        none: { label: "No backing", each: 0 },
        foil: { label: "Foil safety backing", sub: "Meets BS6206 Class C", each: 7.50 }
      },
      fixings: {
        none:   { label: "No fixings", each: 0 },
        screws: { label: "Holes & screws", sub: "Holes 50mm from edges", each: 12.00 },
        glue1:  { label: "Adhesive × 1 tube", each: 8.50, tubes: 1 },
        glue2:  { label: "Adhesive × 2 tubes", each: 17.00, tubes: 2 },
        glue3:  { label: "Adhesive × 3 tubes", each: 25.50, tubes: 3 },
        glue4:  { label: "Adhesive × 4 tubes", each: 34.00, tubes: 4 }
      }
    },

    glass: {
      title: "Made to Measure Toughened Glass",
      minMM: 100,
      maxLong: 2400, maxShort: 1300,
      thickness: {
        "6":  { label: "6mm",  sub: "Shelves & splash panels", perM2: 95.00 },
        "8":  { label: "8mm",  sub: "Tabletops & screens",     perM2: 165.00 },
        "10": { label: "10mm", sub: "Balustrades & heavy use", perM2: 210.00 }
      },
      defaultThickness: "6"
    },

    splashback: {
      title: "Made to Measure Coloured Glass Splashback",
      minMM: 100,
      maxLong: 2500, maxShort: 1300,
      // TODO(client): price per m² for splashbacks. While this is null the
      // page shows "Request a quote" instead of a live price.
      perM2: null
    }
  },

  // TODO(client): confirm the fitting county list (About page list is shorter).
  fittingAreas: [
    "Cheshire", "Denbighshire", "Derbyshire", "East Midlands", "Essex", "Flintshire",
    "Greater London", "Greater Manchester", "Lancashire", "Leicestershire", "Merseyside",
    "Oxfordshire", "Shropshire", "Staffordshire", "Surrey", "Warwickshire",
    "West Midlands", "Worcestershire"
  ]
};
