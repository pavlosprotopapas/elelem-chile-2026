# ELELEM · Epoch Tour Chile 2026

Participant site for the ELELEM Chile workshop — From LLMs to Agentic Systems. Santiago, 22–24 October 2026.

Live: https://pavlosprotopapas.github.io/elelem-chile-2026/

Static site. Two pages:

- `dev.html` — the team's page, with everything. **Edit this one.** (Unlisted and marked noindex, but public like the whole repo.)
- `index.html` — the participant page, generated: `python3 publish.py` copies `dev.html` and shows only the slide PDFs listed in `PUBLIC` at the top of `publish.py`; every other slide link becomes "Slides soon".

Then commit both pages and push to `main`. Slides go in `slides/`, notebooks in `notebooks/`.
