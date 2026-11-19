[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/hrd04-ai/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/hrd04-ai/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

# The World in One Day — 19 November 2026

One image that tells Thursday 19 November 2026 at a glance. A newspaper
front page: masthead with the date, six illustrated stories, and a strip
of three more briefs at the foot.

## The six stories

- **Summit of three** — Trump, Xi and Putin meet together for the first
  time, in Shenzhen on the APEC sidelines.
- **Bridge hit again** — Ukraine strikes the Crimean Bridge for the
  third time in a week; traffic is halted while damage is assessed.
- **Gulf in flames** — the US–Iran exchange of fire spreads across the
  Gulf after the US strike on Qeshm Island.
- **A first for the House** — Hakeem Jeffries is lined up to become the
  first Black Speaker of the US House.
- **Faith in 2035** — Pew Research projects Islam passing Christianity
  as the world's largest religion by 2035.
- **One light-day out** — NASA's Voyager 1 becomes the first
  human-made object to travel one light-day from Earth.

Every panel carries a hand-drawn pictogram, a headline and one factual
sublabel, so a reader who missed the day can follow it from the picture
alone. The briefs strip adds Anthropic's record market debut, the
four-nation call for aid into flooded Gaza, and Nvidia halting H-series
chip shipments to China.

## How it was made

`make_image.py` draws the page with Pillow and saves `entry.png`
(1024×1024, under 1 MiB). `main.py` only copies that finished image to
the output path — standard library only, no network, no randomness — so
repeated runs produce byte-identical output.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see `LICENSE`.
