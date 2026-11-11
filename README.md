# Spot the Scam

An interactive course that teaches people, especially older adults, to recognize scam
emails, text messages, WhatsApp/chat messages and phone calls.

- **Part 1: Learn** (13 lessons): phishing, spear phishing and whaling, smishing, chat-app
  scams, phone scams and their scripts, red flags, how to read a web address, and four
  safety habits. Most lessons end with a quick question.
- **Part 2: Practice** (10 exercises): realistic emails, texts, chat messages and call
  transcripts. Click the parts that look wrong; each click gets instant right/wrong
  feedback with an explanation, and found red flags are numbered on the message.
  There are also "Scam or safe?" and "What would you do?" rounds.
- **Results**: an overall score, a breakdown across 10 topics (what you understand well
  vs. what to review), and buttons that jump back to the matching lessons.

Made for ease of use: large text and buttons, text-size controls, a read-aloud button,
hover/tap explanations, keyboard arrows, light and dark mode, and progress saved in the
browser so people can take a break.

## Sharing it

The whole course is **one file**: `dist/index.html`. It needs no Python and no internet
connection (fonts fall back to system fonts when offline).

- **Send the file**: email or USB-stick `dist/index.html`; the recipient double-clicks it
  and it opens in their web browser. Some email services block `.html` attachments. If
  that happens, zip it first or use a link instead.
- **Host it free on GitHub Pages**: see below. You get a link like
  `https://<your-username>.github.io/scams_training/`.
- **Netlify Drop** (no account setup beyond a free sign-in): drag the `dist` folder onto
  <https://app.netlify.com/drop> to get a public link.

### GitHub Pages (free)

1. Create a free account at <https://github.com> and a new public repository named
   `scams_training`.
2. Push this folder to it:
   ```sh
   git init
   git add .
   git commit -m "Spot the Scam course"
   git branch -M main
   git remote add origin https://github.com/<your-username>/scams_training.git
   git push -u origin main
   ```
3. On GitHub, open **Settings → Pages** and set **Source** to **GitHub Actions**.
4. The included workflow (`.github/workflows/pages.yml`) builds and publishes the site on
   every push. Your link appears on the Pages settings screen after a minute or two.

## Working on it (uses uv)

```sh
uv run build     # writes dist/index.html
uv run serve     # builds, then opens http://localhost:8000 in your browser
```

The source is `web/app.html` (styles, content and logic all in one file). All lessons,
messages, red flags and questions are in the `SLIDES` array in its script. Red flags in
practice messages are marked like `[[key:text]]` (or `[[key>link text|url]]` for links),
and safe parts with a custom explanation are marked `{{text|why it's fine}}`.

All company names, phone numbers and web addresses in the examples are made up.
