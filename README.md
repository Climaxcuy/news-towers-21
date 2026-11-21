[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/climaxcuy/news-towers-21/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/climaxcuy/news-towers-21/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# NEWS TOWERS — Saturday 21 November 2026

The whole day as a 3D city at dusk, in a single 1024×1024 picture:
40 stories from Saturday 21 November 2026, every one of them dated
to that day.

- 13 main stories stand as illuminated towers in a real-time 3D
  skyline (Three.js): the bigger the story, the taller its tower.
  Each tower carries a headline panel with two facts, a data chip
  and a source/certainty tag.
- 27 more stories run as one-line briefs in the street-level band,
  numbered on from the towers.
- A numbers strip binds six big figures to their stories, a UTC
  timeline walks the day from the overnight strike to stumps in
  Wellington, and a DATE CHECK box names the Friday stories that
  were deliberately left out.

## Build

- `scene.html` — the deterministic Three.js city (seeded PRNG,
  lit windows, neon sign bands, street lights); hero towers are
  solved onto the panel grid by projection.
- `shoot.mjs` — maker's tool: renders `scene.html` in headless
  Chrome to `scene.png` + `anchors.json`.
- `stories.py` — every headline, fact, brief and tag on the page.
- `main.py` — the entry program: composites the dusk sky, the
  monumental masthead, the city render and all typography (Pillow,
  Archivo + Playfair) and writes `/output/entry.png`.

Deterministic, no network. `python3 main.py` reproduces the entry.
