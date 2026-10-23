# Seven ZoroPrint feature videos. Every claim is sourced (see SOURCES at the bottom).
# Rect = (x, y, w, h) in capture pixels (captures are 2880 x 1800, Studio at 1440 x 900, 2x).
# Text markup: *word* = orange accent. "say" = what the voice says when it differs from the caption text.

ART = (900, 350, 920, 660)       # the gang sheet's artwork, top part of the A4 sheet
WIN = (0, 0, 2880, 1800)         # the whole window
PANEL = (2160, 300, 700, 1300)   # the right-hand settings column

END = {"say": "ZoroPrint. Start free at zoroprint dot com.", "text": "ZoroPrint. Start free at zoroprint.com."}

VIDEOS = [
 {"id": "v1-knockout", "day": "2026-10-25", "kicker": "KNOCKOUT", "title": "Stop printing *black* on black shirts",
  "hook": ["Black shirt?", "Stop printing", "the *black.*"],
  "hook_vo": "Printing on a black shirt? Stop printing the black.",
  "shots": [
   {"img": "ko_off_white", "img2": "ko_on_white", "swap": True, "title": "Knock out a *colour*", "cam": [WIN, (2150, 860, 720, 420)],
    "ring": (2186, 955, 650, 200), "chip": "Use garment colour · Black",
    "vo": "In ZoroPrint, tick Knock out a colour, and use the garment colour."},
   {"img": "white", "img2": "ko_on_white", "title": "The shirt shows *through*", "cam": [ART], "wipe": True,
    "labels": ["WHITE LAYER · BEFORE", "WHITE LAYER · KNOCKOUT"],
    "vo": "Every black part drops out of the white layer. The shirt shows through instead."},
   {"img": "ko_on_white", "title": "Softer feel. *Less ink.*", "cam": [ART, (1250, 560, 560, 380)],
    "vo": "Softer feel, less ink. Only for shirts of that colour."},
  ],
  "caption": "Printing on black shirts? Stop printing the black 🖤 Knock out a colour in ZoroPrint and the black parts of your design drop out of the white layer, so the shirt itself shows through. Softer feel, less ink. Only for garments of that colour.\n\nStart free → zoroprint.com\n\n#dtf #dtfprinting #dtftransfers #blackshirt #printshop #smallbusiness",
  "tt_title": "Stop printing black on black shirts"},

 {"id": "v2-soft-hand", "day": "2026-10-26", "kicker": "SOFT HAND", "title": "Big prints that *don't* feel like plastic",
  "hook": ["Big print feels", "like a *plastic*", "sticker?"],
  "hook_vo": "Does your big print feel like a plastic sticker?",
  "shots": [
   {"img": "soft0_white", "title": "It's the *solid white*", "cam": [WIN, ART],
    "vo": "That's the solid white layer underneath."},
   {"img": "soft0_white", "title": "Turn up *Soft hand*", "cam": [(2150, 820, 720, 320)], "ring": (2186, 920, 650, 110), "chip": "Soft hand · 40%", "img2": "soft40_white", "swap": True,
    "vo": "Turn up Soft hand in ZoroPrint."},
   {"img": "soft0_white", "img2": "soft40_white", "title": "A grid of *tiny holes*", "cam": [ART], "wipe": True,
    "labels": ["SOLID WHITE", "SOFT HAND 40%"],
    "vo": "It punches a fine grid of holes into the white, so the transfer bends and feels softer."},
   {"img": "soft40_white", "title": "Softer. *Less white ink.*", "cam": [ART, (1180, 560, 520, 400)], "chip": "Sheet total 0.28 → 0.27 USD",
    "vo": "More holes, softer hand, less white ink. On dark shirts, go easy."},
  ],
  "caption": "Big DTF prints feel like a plastic sticker? That's the solid white underneath. Soft hand in ZoroPrint punches a fine grid of holes into the white, so the transfer bends and feels softer, with less white ink. More holes = softer, but less opacity on dark shirts, so go easy there.\n\nStart free → zoroprint.com\n\n#dtf #dtfprinting #dtftransfers #softhand #printshop #smallbusiness",
  "tt_title": "Soft hand: DTF that bends"},

 {"id": "v3-job-cost", "day": "2026-10-27", "kicker": "JOB COST", "title": "What does this sheet *cost* you?",
  "hook": ["What does", "one sheet", "*really cost?*"],
  "hook_vo": "What does one gang sheet really cost you?",
  "shots": [
   {"img": "costs", "title": "Counted *before* you print", "cam": [WIN, (2160, 320, 710, 480)], "ring": (2170, 340, 690, 440), "chip": "Costs tab",
    "vo": "ZoroPrint adds it up before you print. Film, powder, colour ink and white ink, at your own prices."},
   {"img": "costs", "title": "This A4 sheet: *$0.28*", "cam": [(2160, 560, 710, 240)], "ring": (2175, 640, 685, 60),
    "say": "This A4 sheet: twenty-eight cents.", "vo": "This A4 sheet: $0.28."},
   {"img": "costs", "title": "Then counted *drop by drop*", "cam": [(2160, 820, 710, 330)], "ring": (2170, 840, 690, 290),
    "vo": "After printing, it counts the ink really used, drop by drop. Price your transfers on real numbers."},
  ],
  "note": "Costs: Solo plan",
  "caption": "Do you know what one gang sheet costs you? ZoroPrint adds it up before you print: film, powder, colour ink and white ink, at your own prices. After printing it counts the ink really used, drop by drop. Price transfers on numbers, not guesses. (Costs are in the Solo plan, $8/month.)\n\nzoroprint.com\n\n#dtf #dtfprinting #gangsheet #dtfbusiness #printshop #smallbusiness",
  "tt_title": "What one gang sheet really costs"},

 {"id": "v4-less-white-dark", "day": "2026-10-28", "kicker": "WHITE UNDER DARK", "title": "Dark colours need *less white*",
  "hook": ["Dark designs", "coming out", "*stiff?*"],
  "hook_vo": "Dark designs coming out stiff and heavy?",
  "shots": [
   {"img": "wud0_white", "title": "Full white under *everything*", "cam": [WIN, ART],
    "vo": "Dark colours hide the shirt by themselves. They don't need full white."},
   {"img": "wud0_white", "img2": "wud60_white", "title": "Less white under *dark*", "cam": [(2150, 840, 720, 300)], "ring": (2186, 925, 650, 110), "chip": "Less white under dark · 60%", "swap": True,
    "vo": "Slide Less white under dark colours."},
   {"img": "wud0_white", "img2": "wud60_white", "title": "Light colours keep *full white*", "cam": [ART], "wipe": True,
    "labels": ["WHITE LAYER · 0%", "WHITE LAYER · 60%"],
    "vo": "ZoroPrint thins the white under dark tones, and keeps it under light ones. Less ink, less bleed, same look."},
  ],
  "caption": "Dark designs coming out stiff and heavy? Dark colours hide the shirt by themselves, so they don't need full white. \"Less white under dark colours\" in ZoroPrint thins the white under dark tones and keeps it under light ones. Less ink, less bleed, same look.\n\nStart free → zoroprint.com\n\n#dtf #dtfprinting #dtftransfers #whiteink #printshop #smallbusiness",
  "tt_title": "Dark colours need less white"},

 {"id": "v5-mac", "day": "2026-10-29", "kicker": "DTF ON A MAC", "title": "A DTF RIP that runs on *your Mac*",
  "hook": ["DTF printer.", "But you work", "on a *Mac?*"],
  "hook_vo": "Got a DTF printer, but you work on a Mac?",
  "shots": [
   {"img": "preview", "mac": True, "title": "Native on *macOS*",
    "vo": "Most DTF RIPs only run on Windows. ZoroPrint runs natively on macOS."},
   {"img": "printers", "title": "Pick your *converted Epson*", "cam": [WIN, (28, 180, 860, 760)], "ring": (40, 782, 830, 64), "chip": "L1800 · verified",
    "say": "Pick your converted Epson, like the L eight-oh-five, the L eighteen hundred, or the E T eighty-five fifty.",
    "vo": "Pick your converted Epson, like the L805, L1800 or ET-8550."},
   {"img": "white", "title": "USB. *No driver. No dongle.*", "cam": [ART, WIN],
    "vo": "It builds the white and prints straight over USB. No driver, no dongle, no second PC."},
  ],
  "caption": "Got a DTF printer but you work on a Mac? 💻 Most DTF RIPs are Windows-only. ZoroPrint runs natively on macOS (and Windows and Linux), builds the white for you and prints over USB to your converted Epson. No driver, no dongle, no second PC.\n\nStart free → zoroprint.com\n\n#dtf #dtfprinting #macbook #dtfprinter #ripsoftware #smallbusiness",
  "tt_title": "DTF RIP that runs on a Mac"},

 {"id": "v6-on-garment", "day": "2026-10-30", "kicker": "ON GARMENT", "title": "Check the size *before* you press",
  "hook": ["Will it look", "right on", "the *shirt?*"],
  "hook_vo": "Will this design look right on the shirt?",
  "shots": [
   {"img": "preview", "img2": "garment_centre", "title": "Real size on a *size L tee*", "cam": [WIN, (640, 300, 1500, 1320)], "swap": True,
    "vo": "Check before you press. ZoroPrint puts your design on a size L T-shirt, at real size."},
   {"img": "garment_centre", "img2": "garment_left", "title": "Centre chest or *left chest*", "cam": [(640, 300, 1500, 1320)], "ring": (1225, 350, 325, 72), "swap": True,
    "say": "Switch to left chest, and this banner is clearly too wide for it.", "vo": "Switch to left chest, and this banner is clearly too wide for it."},
   {"img": "garment_left", "title": "Fix it *before* the film", "cam": [(1240, 540, 560, 480)],
    "vo": "Fix the size here, before it's on film. Film costs money. A preview doesn't."},
  ],
  "caption": "Will that design look right on the shirt? Check before you press. ZoroPrint's garment view puts your design on a size L T-shirt at real size (56 cm across the chest). Switch between centre chest and left chest and fix the size before it's on film.\n\nStart free → zoroprint.com\n\n#dtf #dtfprinting #tshirtbusiness #heatpress #printshop #smallbusiness",
  "tt_title": "Check the size before you press"},

 {"id": "v7-ink-limit", "day": "2026-10-31", "kicker": "TOTAL INK LIMIT", "title": "Why transfers *crack*",
  "hook": ["Transfers", "*cracking* after", "one wash?"],
  "hook_vo": "Transfers cracking after the first wash?",
  "shots": [
   {"img": "ink200", "title": "Check your *total ink limit*", "cam": [WIN, (2150, 640, 720, 460)], "ring": (2186, 925, 650, 100), "chip": "Total ink limit",
    "vo": "Check your total ink limit. It's the most ink all channels together can lay on one spot."},
   {"img": "ink200", "title": "200% = *two layers*", "cam": [(2150, 860, 720, 220)], "ring": (2186, 925, 650, 100),
    "say": "Two hundred percent means two layers.", "vo": "200% means two layers."},
   {"img": "ink200", "title": "No limit? The film *floods*", "cam": [ART, (1000, 380, 700, 520)],
    "vo": "Without a limit, the film floods, the powder clumps, and the transfer cracks."},
  ],
  "caption": "Transfers cracking after the first wash? Check your total ink limit: the most ink all channels together may lay on one spot. 200% means two layers. Without a limit, the film floods, the powder clumps and the transfer cracks. Find it in ZoroPrint under Colour → Total ink limit.\n\nStart free → zoroprint.com\n\n#dtf #dtfprinting #dtftransfers #dtfprinter #printshop #smallbusiness",
  "tt_title": "Why DTF transfers crack"},
]

SOURCES = {
 "knockout": "dtfPro apps/desktop/src/renderer/i18n.js why_knockout; live Studio control 'Knock out a colour (garment shows through)' + 'Use garment colour Black'",
 "softHand": "i18n.js why_softHand: 'Punches a fine grid of holes into the white so the transfer bends and feels softer. More holes, softer hand — and less opacity on dark garments.' Total 0.28 → 0.27 USD in the live capture",
 "costs": "live Studio Costs tab: Job cost (estimate) film/powder/colour ink/white ink, total 0.28 USD; 'Ink really used: counted drop by drop while printing'; Costs = Solo (app.js:65)",
 "whiteUnderDark": "i18n.js why_whiteUnderDark; imaging.js makeWhite: v *= 1 - ud*(1-luminance)",
 "mac": "docs/ANALIZA-COMPETITIVA.md (Mac native, USB without driver); Studio printer list (L805/L800/L1800 verified, ET-8550 supported)",
 "garment": "live Studio garment view: 'Real size on a size-L T-shirt (56 cm across the chest)', Centre chest / Left chest",
 "inkLimit": "i18n.js why_inkLimit: '200 % means 2 layers. Above it the film floods, the powder clumps and the transfer cracks.'",
}
