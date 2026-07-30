#!/usr/bin/env python3
"""Check every colour pair in the site's palette against WCAG 2.2 AA.

Run this any time you change a colour in css/style.css:

    python3 tools/contrast-check.py

Thresholds used:
  4.5:1  normal-size text on its background            (WCAG 1.4.3, AA)
  3.0:1  focus rings, borders that identify a control  (WCAG 1.4.11, AA)

If you edit a colour in style.css, edit it here too and re-run.
"""

import sys


def luminance(hex_colour):
    h = hex_colour.lstrip("#")
    channels = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    channels = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
                for c in channels]
    r, g, b = channels
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    hi, lo = sorted([luminance(a), luminance(b)], reverse=True)
    return (hi + 0.05) / (lo + 0.05)


# The live site palette (css/style.css). Keep these in sync with the
# :root block there. The site is light only — there is no dark variant.
LIVE = {
    "maple": {
        "paper": "#f8f5f2", "sunk": "#efeae5", "control": "#8b8177",
        "ink": "#241f1c", "muted": "#60564e", "accent": "#78352e",
        "deep": "#5a271f", "wash": "#f2e7e2", "focus": "#2d5f86",
        "anchor": "#43302b", "gold": "#7a6a2c",
    },
}

# Alternative palettes explored earlier, kept so one can be adopted later
# without redoing the verification. Note that the live palette is sampled from
# the portrait; swapping to one of these puts the photo out of key again.
STUDY = {
    "terracotta": {"paper": "#faf8f5", "sunk": "#f2eee8", "control": "#948874",
                   "ink": "#2a2622", "muted": "#6b635a", "accent": "#8a4b2e",
                   "deep": "#6d3a23", "wash": "#f0e6dd", "focus": "#2f5d7c"},
    "umber": {"paper": "#fbf9f4", "sunk": "#f3efe5", "control": "#93876b",
              "ink": "#262320", "muted": "#645c4c", "accent": "#5c4630",
              "deep": "#42311f", "wash": "#f0e9d9", "focus": "#2f5d7c"},
    "sand-ochre": {"paper": "#f7f3ea", "sunk": "#efe9db", "control": "#8f7c5c",
                   "ink": "#2b2620", "muted": "#665c4b", "accent": "#7a4f1d",
                   "deep": "#5c3a12", "wash": "#efe4cf", "focus": "#2f5d7c"},
    "oxblood": {"paper": "#fbfaf9", "sunk": "#f2f0ee", "control": "#8a8380",
                "ink": "#1e1c1b", "muted": "#5d5856", "accent": "#7a2b30",
                "deep": "#5c1d22", "wash": "#f2e8e8", "focus": "#2f5d7c"},
    "slate-navy": {"paper": "#f6f7f8", "sunk": "#ecedef", "control": "#82888e",
                   "ink": "#1c2024", "muted": "#565d63", "accent": "#1f4f75",
                   "deep": "#153a58", "wash": "#e6ecf0", "focus": "#8a4b2e"},
    "verdigris": {"paper": "#f8f7f5", "sunk": "#efedea", "control": "#8a857d",
                  "ink": "#23211f", "muted": "#5e5a55", "accent": "#2f5b57",
                  "deep": "#1f403d", "wash": "#e6eceb", "focus": "#8a4b2e"},
    "graphite": {"paper": "#f7f7f6", "sunk": "#eeeeec", "control": "#84847e",
                 "ink": "#1f1f1e", "muted": "#5a5a58", "accent": "#1f1f1e",
                 "deep": "#000000", "wash": "#e8e8e5", "focus": "#2f5d7c"},
}

PALETTES = {**LIVE, **STUDY}

# (foreground, background, minimum ratio, what it is)
CHECKS = [
    ("ink",     "paper", 4.5, "body text"),
    ("muted",   "paper", 4.5, "muted text (dates, affiliation, venue)"),
    ("accent",  "paper", 4.5, "link"),
    ("deep",    "paper", 4.5, "link, hovered"),
    ("ink",     "sunk",  4.5, "text inside a callout"),
    ("accent",  "sunk",  4.5, "link inside a callout"),
    ("muted",   "sunk",  4.5, "muted text inside a callout"),
    ("deep",    "wash",  4.5, "publication tag, hovered"),
    ("focus",   "paper", 3.0, "focus ring"),
    ("control", "paper", 3.0, "border identifying a clickable tag"),
    # The tags also sit on the sunk surface inside the sidebar callout, so the
    # border has to clear 3:1 against that background too.
    ("control", "sunk",  3.0, "clickable border on a callout"),
    ("accent",  "paper", 3.0, "current-page marker in the nav"),
]

# Tokens only the live palette defines. Checked separately so the older study
# palettes, which have no anchor or gold, do not error out.
LIVE_ONLY = [
    ("anchor", "paper", 3.0, "serrated masthead edge"),
    ("gold",   "paper", 4.5, "gold, if ever used as text"),
]


def main():
    verbose = "-v" in sys.argv or "--verbose" in sys.argv
    failed = False

    for name, theme in PALETTES.items():
        problems = []
        checks = CHECKS + (LIVE_ONLY if name in LIVE else [])
        for fg, bg, required, label in checks:
            r = ratio(theme[fg], theme[bg])
            if r < required:
                problems.append((label, r, required))
            if verbose:
                print(f"  {'pass' if r >= required else 'FAIL'}  {r:5.2f}:1  "
                      f"(need {required})  {name} — {label}")
        failed |= bool(problems)
        if not verbose:
            if problems:
                print(f"FAIL  {name}")
                for label, r, required in problems:
                    print(f"        {r:5.2f}:1 (need {required})  {label}")
            else:
                print(f"pass  {name}")

    print()
    if failed:
        print("Some pairs fail. Fix the colour in the theme's CSS AND here.")
    else:
        print(f"All {len(PALETTES)} palettes meet WCAG 2.2 AA.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
