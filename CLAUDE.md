# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this is

"Spot the Scam": an interactive, single-page course that teaches people, especially
older adults, to recognize scam emails, texts, chat messages, phone calls and in-person
travel scams. It must work as **one standalone HTML file** that people can double-click
or host on GitHub Pages. Recipients never need Python.

## Layout

- `web/app.html`: the **only source file**. It holds the styles, content and logic. The
  part above the `<!-- /head -->` marker is head content (title, fonts, `<style>`).
  Everything below it is body markup and the script.
- `src/scams_training/cli.py`: `build()` wraps `web/app.html` into `dist/index.html`
  (adds the doctype, `<html>/<head>/<body>`, base CSS). `serve()` builds the file, then
  serves `dist/` on http://localhost:8000.
- `dist/index.html`: the built, shareable file. **It is committed**, so rebuild it after
  every change to `web/app.html`.
- `.github/workflows/pages.yml`: on every push to `main`, it runs `uv run build` and
  deploys `dist/` to GitHub Pages.

## Commands (always use uv)

```sh
uv run build   # web/app.html -> dist/index.html
uv run serve   # build, then serve on http://localhost:8000
```

There is no test suite. Check changes in a browser. Headless Chrome screenshots and
click-through tests work. Also check a ~400px width for horizontal overflow.

## How the app script is organized (in `web/app.html`)

- `CONCEPTS`: topic keys used for scoring and per-topic feedback on the results pages.
- `SLIDES`: all content, in order. Each slide has a type: lesson, quiz, spot-the-flag
  practice, results, and so on.
- `TRACKS`: the two tabs, each with its own slides, progress and results page:
  - `scams`: messages and calls
  - `travel`: travel scams abroad

  There is no combined score across tabs.
- Message markup in practice slides, parsed by `segs()`:
  - `[[conceptKey:text]]`: a red flag the learner should click.
  - `[[conceptKey>link text|url]]`: a red-flag link.
  - `{{text|why it's fine}}`: a safe part with a custom explanation.
- `renderMsg()` message kinds: `email`, `sms`, `chat`, `call`, `talk`, `popup`.
- Key functions: `renderSlide()`, `tally()`/`renderResults()` for scoring, `go()` for
  navigation, and `doAct()` for button actions (`reveal`, `goto`, `tab`, `retry`,
  `restart`, `confirm-restart`, `cancel-restart`).
- Progress is saved in `localStorage` under `spot-the-scam-v1`. Wrap all storage access
  in try/catch. The app must still work when storage is unavailable.

## Conventions

- **Audience is older adults:** use plain language, large text and big tap targets, and
  keep it readable at every text-size setting. Explanations should say *why* something
  is a red flag. Don't scold the learner.
- **All examples are fictional:** company names, phone numbers, web addresses and people
  are invented. Only real **reporting/help resources** may be real, such as the FTC,
  7726, AARP, the State Dept and emergency numbers. Verify those before changing them.
- Keep the file self-contained. The only external resource is Google Fonts, and every
  face needs a system-font fallback. No other CDNs and no runtime fetches.
- Colors are CSS tokens on `:root` with dark-mode overrides. Never use literal colors in
  component rules.
- Don't use `alert()`, `confirm()` or `prompt()`. Build confirmations into the page, as
  "Start this tab over" does.
- When adding a slide that scores points, give each flag or question a `CONCEPTS` key.
  Then check that the results page totals and review links still make sense for that
  tab.
- When content changes, update the lesson and exercise counts in `README.md`.
