#!/usr/bin/env python3
"""Generate data.json and data.csv for the Copilot model-lag site.

Every row is sourced from two public pages: the vendor's own announcement
and the GitHub Changelog entry. Edit ROWS and re-run.
"""

import csv
import json
from datetime import date, datetime
from pathlib import Path

GH = "https://github.blog/changelog/"

# model, vendor, vendor_date, copilot_date, stage, vendor_url, changelog_slug, note
ROWS = [
    ("OpenAI o1", "OpenAI", "2024-09-12", "2024-10-29", "preview",
     "https://openai.com/index/introducing-openai-o1-preview/", None,
     "Vendor date is o1-preview. Full o1 shipped 2024-12-05, so this lag is an upper bound."),
    ("Claude 3.5 Sonnet", "Anthropic", "2024-10-22", "2024-11-01", "preview",
     "https://www.anthropic.com/news/3-5-models-and-computer-use", None, None),
    ("OpenAI o3-mini", "OpenAI", "2025-01-31", "2025-01-31", "preview",
     "https://openai.com/index/openai-o3-mini/", None, None),
    ("Gemini 2.0 Flash", "Google", "2025-02-05", "2025-02-05", "preview",
     "https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-model-updates-february-2025/",
     None, "Vendor date is general availability; an experimental build existed from 2024-12-11."),
    ("Claude 3.7 Sonnet", "Anthropic", "2025-02-24", "2025-02-24", "preview",
     "https://www.anthropic.com/news/claude-3-7-sonnet", None, None),
    ("GPT-4.5", "OpenAI", "2025-02-27", "2025-02-27", "preview",
     "https://openai.com/index/introducing-gpt-4-5/", None, None),
    ("Gemini 2.5 Pro", "Google", "2025-03-25", "2025-04-11", "preview",
     "https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-model-thinking-updates-march-2025/",
     None, "Vendor date is the experimental release. GA was 2025-06-27, which would make the lag negative."),
    ("GPT-4.1", "OpenAI", "2025-04-14", "2025-04-14", "preview",
     "https://openai.com/index/gpt-4-1/", None, None),
    ("OpenAI o3 / o4-mini", "OpenAI", "2025-04-16", "2025-04-16", "preview",
     "https://openai.com/index/introducing-o3-and-o4-mini/", None, None),
    ("Claude Sonnet 4 / Opus 4", "Anthropic", "2025-05-22", "2025-05-22", "preview",
     "https://www.anthropic.com/news/claude-4", None, None),
    ("Claude Opus 4.1", "Anthropic", "2025-08-05", "2025-08-05", "preview",
     "https://www.anthropic.com/news/claude-opus-4-1", None, None),
    ("GPT-5", "OpenAI", "2025-08-07", "2025-08-07", "preview",
     "https://openai.com/index/introducing-gpt-5/", None, None),
    ("GPT-5 mini", "OpenAI", "2025-08-07", "2025-08-13", "preview",
     "https://openai.com/index/introducing-gpt-5/", None, None),
    ("Grok Code Fast 1", "xAI", "2025-08-28", "2025-08-26", "preview",
     "https://x.ai/news/grok-code-fast-1", None,
     "Shipped in Copilot as the stealth model 'sonic' two days before xAI's public announcement."),
    ("GPT-5-Codex", "OpenAI", "2025-09-15", "2025-09-23", "preview",
     "https://openai.com/index/introducing-upgrades-to-codex/",
     "2025-09-23-openai-gpt-5-codex-is-rolling-out-in-public-preview-for-github-copilot", None),
    ("Claude Sonnet 4.5", "Anthropic", "2025-09-29", "2025-09-29", "preview",
     "https://www.anthropic.com/news/claude-sonnet-4-5",
     "2025-09-29-anthropic-claude-sonnet-4-5-is-in-public-preview-for-github-copilot", None),
    ("Claude Haiku 4.5", "Anthropic", "2025-10-15", "2025-10-15", "preview",
     "https://www.anthropic.com/news/claude-haiku-4-5",
     "2025-10-15-anthropics-claude-haiku-4-5-is-in-public-preview-for-github-copilot", None),
    ("GPT-5.1 / Codex", "OpenAI", "2025-11-12", "2025-11-13", "preview",
     "https://openai.com/index/gpt-5-1/",
     "2025-11-13-openais-gpt-5-1-gpt-5-1-codex-and-gpt-5-1-codex-mini-are-now-in-public-preview-for-github-copilot",
     None),
    ("Gemini 3 Pro", "Google", "2025-11-18", "2025-11-18", "preview",
     "https://blog.google/products-and-platforms/products/gemini/gemini-3/",
     "2025-11-18-gemini-3-pro-is-in-public-preview-for-github-copilot", None),
    ("GPT-5.1-Codex-Max", "OpenAI", "2025-11-19", "2025-12-04", "preview",
     "https://openai.com/index/gpt-5-1-codex-max/",
     "2025-12-04-openais-gpt-5-1-codex-max-is-now-in-public-preview-for-github-copilot", None),
    ("Claude Opus 4.5", "Anthropic", "2025-11-24", "2025-11-24", "preview",
     "https://www.anthropic.com/news/claude-opus-4-5",
     "2025-11-24-claude-opus-4-5-is-in-public-preview-for-github-copilot", None),
    ("GPT-5.2", "OpenAI", "2025-12-11", "2025-12-11", "preview",
     "https://openai.com/index/introducing-gpt-5-2/",
     "2025-12-11-openais-gpt-5-2-is-now-in-public-preview-for-github-copilot", None),
    ("Gemini 3 Flash", "Google", "2025-12-17", "2025-12-17", "preview",
     "https://blog.google/products-and-platforms/products/search/google-ai-mode-update-gemini-3-flash/",
     "2025-12-17-gemini-3-flash-is-now-in-public-preview-for-github-copilot", None),
    ("GPT-5.2-Codex", "OpenAI", "2025-12-18", "2026-01-14", "GA",
     "https://openai.com/index/introducing-gpt-5-2-codex/",
     "2026-01-14-gpt-5-2-codex-is-now-generally-available-in-github-copilot", None),
    ("Claude Opus 4.6", "Anthropic", "2026-02-05", "2026-02-05", "GA",
     "https://www.anthropic.com/news/claude-opus-4-6",
     "2026-02-05-claude-opus-4-6-is-now-generally-available-for-github-copilot", None),
    ("GPT-5.3-Codex", "OpenAI", "2026-02-05", "2026-02-09", "GA",
     "https://openai.com/index/introducing-gpt-5-3-codex/",
     "2026-02-09-gpt-5-3-codex-is-now-generally-available-for-github-copilot", None),
    ("Claude Sonnet 4.6", "Anthropic", "2026-02-17", "2026-02-17", "GA",
     "https://www.anthropic.com/news/claude-sonnet-4-6",
     "2026-02-17-claude-sonnet-4-6-is-now-generally-available-in-github-copilot", None),
    ("Gemini 3.1 Pro", "Google", "2026-02-19", "2026-02-19", "preview",
     "https://deepmind.google/models/gemini/pro/",
     "2026-02-19-gemini-3-1-pro-is-now-in-public-preview-in-github-copilot", None),
    ("GPT-5.4", "OpenAI", "2026-03-05", "2026-03-05", "GA",
     "https://openai.com/index/introducing-gpt-5-4/",
     "2026-03-05-gpt-5-4-is-generally-available-in-github-copilot", None),
    ("GPT-5.4 mini", "OpenAI", "2026-03-17", "2026-03-17", "GA",
     "https://openai.com/index/introducing-gpt-5-4-mini-and-nano/",
     "2026-03-17-gpt-5-4-mini-is-now-generally-available-for-github-copilot", None),
    ("Claude Opus 4.7", "Anthropic", "2026-04-16", "2026-04-16", "GA",
     "https://www.anthropic.com/news/claude-opus-4-7",
     "2026-04-16-claude-opus-4-7-is-generally-available", None),
    ("GPT-5.5", "OpenAI", "2026-04-23", "2026-04-24", "GA",
     "https://openai.com/index/introducing-gpt-5-5/",
     "2026-04-24-gpt-5-5-is-generally-available-for-github-copilot", None),
    ("Gemini 3.5 Flash", "Google", "2026-05-19", "2026-05-19", "GA",
     "https://blog.google/innovation-and-ai/products/google-io-2026/",
     "2026-05-19-gemini-3-5-flash-is-generally-available-for-github-copilot", None),
    ("Claude Opus 4.8", "Anthropic", "2026-05-28", "2026-05-28", "GA",
     "https://www.anthropic.com/news/claude-opus-4-8",
     "2026-05-28-claude-opus-4-8-is-generally-available-for-github-copilot", None),
    ("MAI-Code-1-Flash", "Microsoft AI", "2026-06-02", "2026-06-02", "GA",
     "https://microsoft.ai/news/introducingmai-code-1-flash/",
     "2026-06-02-mai-code-1-flash-is-now-available-for-github-copilot", None),
    ("Claude Fable 5", "Anthropic", "2026-06-09", "2026-06-09", "GA",
     "https://www.anthropic.com/news/claude-fable-5-mythos-5",
     "2026-06-09-claude-fable-5-is-generally-available-for-github-copilot", None),
    ("Kimi K2.7 Code", "Moonshot AI", "2026-06-12", "2026-07-01", "GA",
     "https://moonshotai.github.io/", "2026-07-01-kimi-k2-7-is-now-available-in-github-copilot",
     "Vendor date corroborated by third-party coverage only."),
    ("Claude Sonnet 5", "Anthropic", "2026-06-30", "2026-06-30", "GA",
     "https://www.anthropic.com/news/claude-sonnet-5",
     "2026-06-30-claude-sonnet-5-is-generally-available-for-github-copilot", None),
    ("GPT-5.6 Sol/Terra/Luna", "OpenAI", "2026-07-09", "2026-07-09", "GA",
     "https://openai.com/index/introducing-gpt-5-6/",
     "2026-07-09-openais-gpt-5-6-sol-terra-and-luna-are-now-available-in-github-copilot",
     "A partner preview was available from 2026-06-26; the GA date is used here."),
    ("Grok 4.5", "xAI", "2026-07-16", "2026-07-28", "GA",
     "https://x.ai/news/grok-4-5", "2026-07-28-grok-4-5-is-now-available-in-github-copilot",
     "API access may have preceded the public announcement."),
    ("Kimi K3", "Moonshot AI", "2026-07-16", "2026-08-06", "GA",
     "https://moonshotai.github.io/", "2026-08-06-kimi-k3-is-now-available-in-github-copilot", None),
    ("Gemini 3.6 Flash", "Google", "2026-07-21", "2026-07-21", "GA",
     "https://ai.google.dev/gemini-api/docs/changelog",
     "2026-07-21-gemini-3-6-flash-is-now-available-in-github-copilot", None),
    ("Claude Opus 5", "Anthropic", "2026-07-24", "2026-07-24", "GA",
     "https://www.anthropic.com/news/claude-opus-5",
     "2026-07-24-claude-opus-5-is-now-available-in-github-copilot", None),
    ("MAI-Code-1.1-Flash", "Microsoft AI", "2026-08-11", "2026-08-11", "GA",
     "https://microsoft.ai/news/mai-code-1-1-flash-br-better-faster-at-a-quarter-of-the-cost/",
     "2026-08-11-mai-code-1-1-flash-available-in-github-copilot", None),
    ("Grok 4.6", "xAI", "2026-08-12", "2026-08-14", "GA",
     "https://x.ai/news/grok-4-6", "2026-08-14-grok-4-6-is-now-available-in-github-copilot", None),
    ("Gemini 3.7 Flash", "Google", "2026-08-13", "2026-08-13", "GA",
     "https://deepmind.google/models/gemini/flash/",
     "2026-08-13-gemini-3-7-flash-is-now-available-in-github-copilot", None),
]

FIELDS = ["model", "vendor", "vendorDate", "copilotDate", "stage",
          "lagDays", "vendorUrl", "changelogUrl", "note"]


def parse(d):
    return datetime.strptime(d, "%Y-%m-%d").date()


def build():
    models = []
    for model, vendor, vdate, cdate, stage, vurl, slug, note in ROWS:
        models.append({
            "model": model,
            "vendor": vendor,
            "vendorDate": vdate,
            "copilotDate": cdate,
            "stage": stage,
            "lagDays": (parse(cdate) - parse(vdate)).days,
            "vendorUrl": vurl,
            "changelogUrl": GH + slug if slug else None,
            "note": note,
        })
    models.sort(key=lambda m: m["vendorDate"])
    return models


def main():
    out = Path(__file__).parent
    models = build()

    payload = {
        "generated": date.today().isoformat(),
        "count": len(models),
        "models": models,
    }
    (out / "data.json").write_text(json.dumps(payload, indent=2) + "\n")

    with (out / "data.csv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(models)

    lags = sorted(m["lagDays"] for m in models)
    same_day = sum(1 for x in lags if x <= 0)
    print(f"{len(models)} models | median {lags[len(lags) // 2]}d | "
          f"mean {sum(lags) / len(lags):.1f}d | day-0 {same_day / len(lags):.0%}")


if __name__ == "__main__":
    main()
