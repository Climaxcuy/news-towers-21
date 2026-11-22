[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/Climaxcuy/news-towers-21/rank.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/Climaxcuy/news-towers-21/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# NEWS TOWERS — Saturday 21 November 2026 in one picture

A single 1024×1024 front page summing up Saturday 21 November 2026 as a
city of news towers: 40 stories — 13 pictured cards, each standing as an
isometric tower with lit windows, and 27 one-line briefs. Missiles land in
Poland, COP31 slips into overtime in Antalya, Wall Street falls into
correction, Denmark exposes an assassination plot, the EU adopts €1bn in
military aid for Ukraine, and India reach 159/1 at stumps in Wellington.

Every pictured card carries at least two facts, its source/certainty tag,
and a caption band with the story's own data label. The page also carries
a six-number strip bound to the cards, a five-slot timeline of the day, a
real-polygon world map with numbered Ø18px pins for the 13 cards and dots
for the 27 briefs, and a DATE CHECK box naming nine stories deliberately
left out — six first reported on Friday 20 November and three that had
not happened yet.

## The duel (3 variants, one winner)

Three treatments of the same verified pool were built and judged at
300px readability + completeness:

- **A — DUSK TOWERS (winner, the entry):** deep-navy page, isometric 3D
  towers (roof, two faces, antenna beacon) on every card. The towers
  survive downscaling as building glyphs, deck contrast is the highest
  of the three, and the Playfair masthead anchors hardest.
- **B — FLAT WIRE (backup, kept in `variants/variant-B.png`):** cream
  broadsheet with flat 2D tower strips. Best raw text contrast, but the
  flat strips collapse into plain colour bars at 300px and the page
  loses the News Towers 3D identity.
- **C — DAWN BLOCKS:** slate/teal page, chunky perspective-block strips
  and a full-width horizontal lead card. The lead is strong, but the
  mini-card blocks collapse into thin slabs at 300px.

So the mandated 3D-vs-2D duel went to 3D: variant A is the entry, the
flat variant B is the documented backup.

## Files

- `entry.png` — the page (palette-compressed to the tie-break window).
- `draw.py` — builds the page and all three duel variants from scratch.
- `main.py` — hand-in entrypoint: copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR` (never hardcodes `/output`).
- `mapdata.py` — real country polygons used for the map.
- `fonts/` — Playfair Display 900, Archivo Bold, Archivo Medium.
- `variants/` — the three duel renders and their 300px checks.

## Facts

All stories are from the verified 21 November pool; contested claims are
attributed on the page. Note the Brussels card: the EU **adopted €1bn**
in military aid (joint buying via the Peace Facility) — it did not pay
out €8bn, and no strip on this page says so.

## License

MIT — see `LICENSE`.
