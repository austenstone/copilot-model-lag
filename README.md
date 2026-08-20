# How fast do new AI models reach GitHub Copilot?

**[View the site →](https://austenstone.github.io/copilot-model-lag/)**

Every time a frontier model ships, someone asks how long until it lands in GitHub Copilot.
This measures it: the gap between a vendor's public release and the model showing up in Copilot,
across 46 launches from September 2024 to August 2026.

## The short answer

- **Median lag: 0 days.** 70% of launches shipped in Copilot the same day the vendor announced them.
- **80% shipped within a week.**
- Frontier models from Anthropic, OpenAI, and Google are effectively day-0 — GitHub is a launch partner.
- Lag shows up on **sub-variants** (Codex-Max, mini tiers) and **non-launch-partner vendors**.
- One model had *negative* lag: Grok Code Fast 1 was in Copilot as the stealth model "sonic" two days
  before xAI announced it.

## Data

| File | What |
| --- | --- |
| [`data.json`](data.json) | Canonical dataset, one record per launch |
| [`data.csv`](data.csv) | Same data, spreadsheet-friendly |
| [`build.py`](build.py) | Source of truth. Edit `ROWS`, re-run, both files regenerate |

Each record carries a `vendorUrl` and a `changelogUrl` so every number traces back to a public page.

```bash
python3 build.py   # regenerates data.json and data.csv
python3 -m http.server   # then open http://localhost:8000
```

No build step, no dependencies. The site is a single `index.html` that fetches `data.json`.

## Method

- **Vendor date** — the public announcement date from the vendor's own blog or newsroom.
  Not an API model-ID snapshot date; strings like `claude-opus-4-5-20251101` are training cutoffs,
  not release dates.
- **Copilot date** — the first [GitHub Changelog](https://github.blog/changelog/label/copilot/) entry
  announcing availability. Where a model shipped to public preview first, the preview date is used,
  since that is when users could actually select it.
- **Lag** — calendar days between the two. Negative means Copilot was first.

Rows where the vendor date is genuinely ambiguous (experimental vs. GA, partner preview vs. public
launch) carry a `note` field explaining the choice.

## Corrections

Found a wrong date or a missing model? [Open an issue](https://github.com/austenstone/copilot-model-lag/issues)
or send a PR editing `ROWS` in [`build.py`](build.py). Please include the vendor announcement URL and
the changelog URL.

## Disclaimer

Independent analysis of public data. Not affiliated with or endorsed by GitHub or any model vendor.
Not a commitment, roadmap, or service-level agreement, and not a predictor of future releases.

## License

[MIT](LICENSE) for the code. Data is compiled from public sources.
