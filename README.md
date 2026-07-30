# Personal academic website

Source for my research site. Plain HTML and CSS — no build step, no
dependencies, no JavaScript, no web fonts. Hosted on GitHub Pages.

To work on it, open `index.html` in a browser. There is nothing to install and
nothing to compile.

## Layout

```
index.html            the site
research.html         written, not yet linked — see "Turning the other pages on"
publications.html     written, not yet linked
css/style.css         all styling; design tokens at the top
assets/headshot.jpeg  the original photograph, kept as the source for re-crops
assets/headshot-maple.jpeg  the cropped, colour-corrected portrait the site uses
assets/cv.pdf         the CV the site links to
cv/Chris_Lee_CV.tex   CV source (compile with LuaLaTeX)
tools/contrast-check.py     verifies every palette against WCAG AA
```

## Design

**Institutional profile layout, compact scale, light only.** A serrated rule
across the top, a department line, then a two-column body: writing on the left, a
factual sidebar on the right. Publications are an indexed record with the year in
a left gutter.

**The palette is sampled from the portrait rather than chosen alongside it.**
Measuring the photograph's hue content gave blue 33%, clay/maroon 32%, neutral
12%, skin 10%, gold 6%, and green 0.5%. An earlier draft was accented in sage —
the one hue the photo essentially does not contain — which is why the portrait
read as pasted on. The values now come from the maple foliage behind me
(`#54483b`), its backlit gold (`#85773f`) and its deepest shadow (`#323135`).

The photograph is corrected to match: blue muted to 38% saturation, skin eased to
78% on bright pixels only, leaving the maple's maroon and gold to carry the
image. The correction is baked into `headshot-maple.jpeg` rather than applied as
a CSS filter, so a saved copy or a link preview looks like the page does. Do not
stack a `filter:` on top of it.

**Compact type scale**: 15px body, 13px metadata, 12px labels. Twelve pixels is
the floor — below that, letterspaced uppercase labels stop being comfortable to
read.

**One deliberate flourish.** `.masthead::before` draws a 5px sawtooth across the
top of each page, echoing the toothed margin of a maple leaf. It is a CSS mask
over a solid colour rather than a coloured SVG, so it follows the `--anchor`
token instead of hard-coding a hex; browsers without mask support fall back to a
plain rule.

Everything visual comes from the `:root` block at the top of `css/style.css`.
Seven alternative palettes drafted along the way are kept in the `STUDY` dict in
`tools/contrast-check.py`, each already verified. Note that swapping to one puts
the photograph back out of key unless it is re-graded too.

## Accessibility

Built to WCAG 2.2 Level AA.

- Every text and border colour pair is verified — `python3 tools/contrast-check.py`.
- Full keyboard reachability, a visible focus ring on every focusable element,
  and a skip link.
- One `<h1>` per page, headings in order, real landmarks, publications marked up
  as lists.
- Repeated link labels carry a visually-hidden paper title, so a screen reader
  user listing every link on the page can tell them apart.
- No horizontal scrolling down to a 320px viewport or at 400% zoom.
- Colour is never the only signal: links are underlined, and the current nav item
  carries `aria-current` as well as a coloured rule.
- Honours `prefers-reduced-motion`; borders survive Windows High Contrast Mode.

**The one real gap**: the CV is a PDF, and a PDF built by `pdflatex` is untagged
— no reading order, no heading structure, no language. A screen reader gets an
unstructured wall of text, and good HTML does not fix it. LuaLaTeX with
`\DocumentMetadata{pdfstandard=ua-2}` helps; publishing an HTML CV alongside the
PDF is the only complete fix.

If you change a colour, update it in `tools/contrast-check.py` too and re-run.

## Maintenance

### Adding a publication

Copy one `<li class="pub"> … </li>` block and edit it. Wrap your own name in
`<span class="self">` so it renders bold, and repeat the paper title inside the
`<span class="visually-hidden">` so screen reader users can tell links apart.

Each paper carries a single **arXiv** link pointed at the abstract page
(`arxiv.org/abs/…`), never the PDF. One source of truth, so no stale copy can
drift; arXiv outlives any hosting; and the publisher usually owns the typeset
version of record, so self-hosting it breaches a lot of agreements. The abstract
page also carries arXiv's HTML rendering, which is accessible in a way a PDF is
not.

The tag row takes more than one link if a `Journal` (DOI) or `Code` link is
wanted later.

### Alphabetical author order

Individual papers are marked rather than the page making a blanket claim, because
the list spans two traditions with opposite defaults — learning theory, via
theoretical computer science, is usually alphabetical; operations research
usually is not. Append to the author list:

```html
<span class="alpha" aria-hidden="true">&dagger;</span><span class="visually-hidden"> (authors listed alphabetically)</span>
```

and keep the `<p class="pub-legend">` line at the foot of that page. Two rules:

- **Never use an asterisk.** In machine learning venues `*` means *equal
  contribution*; a reader will take the marker as a co-first-author claim that
  was not made.
- **The legend must appear wherever a dagger does.** An unexplained symbol is
  worse than no symbol.

The dagger is hidden from screen readers, which would otherwise announce it as
"dagger"; the adjacent span carries the meaning.

### Turning the other pages on

Only the home page and the CV are live. `research.html` and `publications.html`
are written and sitting in the repo, unlinked, until there is more to put on
them. Every switch is tagged:

```
grep -rn "DISABLED-PAGES" *.html
```

| File | Switch |
| --- | --- |
| `index.html` | uncomment the two nav links |
| `index.html` | uncomment the "More on what I work on" sentence |
| `index.html` | uncomment the "All publications" link |
| `index.html` | revert the heading `Publications` to `Selected work` |
| `research.html`, `publications.html` | delete the `noindex` meta tag |

The `noindex` tags keep the unfinished pages out of search results if a crawler
reaches them another way; deleting them is what actually publishes the pages.
While Publications is off, the home page list is the only copy of the papers, so
edit that one and keep `publications.html` in step.

### Updating the CV

`cv/` holds the LaTeX source. Build it, then copy the PDF to `assets/cv.pdf`,
which is what the site links. Build artefacts (`.aux`, `.log`, `.fls`,
`.synctex.gz`) are gitignored — the logs embed absolute paths from the machine
that built them.

## Deploying

Settings → Pages → deploy from `main`, root. `.nojekyll` is present so GitHub
serves the files as-is instead of running them through Jekyll.

Once the URL is fixed, add a canonical link to the `<head>` of each page:

```html
<link rel="canonical" href="https://YOUR-URL/">
```

## Deliberately absent

No JavaScript, no web fonts, no analytics, no animation, no dark mode. The site
declares `color-scheme: light` so browsers do not apply an automatic dark
treatment of their own. Each of these would add a maintenance burden or a
distraction without making the site better at its actual job: letting someone
decide, in under a minute, whether to read the papers or send an email.

## License

Code — the HTML structure, CSS, and the scripts in `tools/` — is MIT licensed;
take any of it. The content is not: the written text, the photographs, the CV and
the publication list are all rights reserved. See [LICENSE](LICENSE).
