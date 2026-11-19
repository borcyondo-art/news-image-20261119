# The World in One Picture — Thursday 19 November 2026

A front-page image summing up the world's news of Thursday 19 November
2026, for make.fun bounty `news-image-20261119` ($250, top 50 share).

## The image

`entry.png` (1024×1024, PNG) is drawn from scratch by `render.py` — a flat
vector newspaper front page, rendered with Pillow at 2× and downscaled.
No network, no external assets, no photographs: every pixel is computed
here, so no text can come out garbled.

Layout: a masthead naming the day, one lead story, two second-row stories,
three third-row stories, and a footer ticker of three more items.

## Stories (researched 19 Nov 2026 ~00:30 UTC, checked against Reuters,
NASA/JPL, the European Commission, IMD and launch-day reporting)

1. **Shenzhen — Trump, Xi and Putin meet** (lead): the first trilateral
   summit of the three leaders, at 2:30 p.m. local time at Kylin Villa on
   the APEC sidelines; nuclear arms and the Iran war on the agenda.
2. **GTA VI is out**: a rolling midnight launch from New Zealand, 13 years
   after GTA V, with about 16 million pre-orders.
3. **Voyager 1, one light-day away**: NASA marks the 1977 probe's
   milestone — 16 billion miles out, a radio signal now takes a day to
   reach it.
4. **Cyclone Akvan bears down on India**: now a very severe storm;
   200,000 people to be moved in Odisha; landfall due Friday, winds to
   145 km/h.
5. **The EU's €45bn Ukraine loan goes to Berlin**: the Coalition of the
   Willing meets on the loan proposed the day before — €20bn for budgets,
   €25bn for arms.
6. Footer: Peltola nears a Senate win in Alaska; Canada's Carney
   recalibrates China ties; the LPG tanker that sank off Bulgaria was hit
   by projectiles, officials say.

Claims are hedged where the reporting is contested, and nothing is stated
that the sources do not support. The Nvidia leadership change (12 Nov)
and the EU loan proposal itself (18 Nov) are deliberately not presented
as 19 November news; the loan appears only via the 19 November Berlin
meeting, and Voyager via NASA's 19 November confirmation event.

## Layout

- `render.py` — draws `entry.png` (run it again any time to regenerate).
- `main.py` — the entrypoint (Python 3.13, standard library only): copies
  `entry.png` to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR`).
- `entry.png` — the image the judge sees.

## Local gate (run 19 Nov 2026)

- `main.py` run twice (no network): byte-identical output both times.
- PNG valid, 1024×1024 px, under 1 MiB — see the numbers in the build log.
- Read at 300 px across: the date, lead headline and panel headlines
  stay legible.
