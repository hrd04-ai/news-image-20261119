[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/hrd04-ai/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/hrd04-ai/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

# The World in One Day — 19 November 2026

A newspaper front-page infographic that sums up Thursday 19 November 2026
in one image: a bold masthead naming the day, then six panels covering the
day's most consequential stories across regions and fields — the first
three-way Trump–Xi–Putin summit in Shenzhen, Ukraine striking the Crimean
Bridge for a third time in a week, the US–Iran fire exchange widening
across the Gulf, Hakeem Jeffries poised to become the first Black Speaker
of the US House, Pew projecting Islam to pass Christianity as the world's
largest faith by 2035, and NASA's Voyager 1 reaching one light-day from
Earth. Each panel pairs a simple drawn pictogram with a short headline and
one factual sublabel, so the whole day reads clearly from the image alone.
A briefs strip adds Anthropic's record stock-market debut, the four-nation
call for aid into flooded Gaza, and Nvidia halting H-series chip shipments
to China. The image is drawn locally with Pillow (`make_image.py`) and
shipped as a finished `entry.png`; `main.py` (standard library only)
simply copies it to the output path, so both grader runs produce
byte-identical output.

## How to run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This writes the image to `out/entry.png` (1024x1024 PNG, under 1 MiB).

## License

MIT — see `LICENSE`.
