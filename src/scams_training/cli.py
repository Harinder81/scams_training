"""Command-line tools.

    uv run build   -> writes dist/index.html, a single standalone file you can
                      double-click, email, or host (e.g. GitHub Pages).
    uv run serve   -> builds, then opens the course in your browser at
                      http://localhost:8000
"""

from __future__ import annotations

import argparse
import functools
import http.server
import re
import socketserver
import sys
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "web" / "app.html"
DIST = ROOT / "dist"
OUTPUT = DIST / "index.html"
HEAD_MARKER = "<!-- /head -->"

BASE_CSS = """<style>
html{color-scheme:light;padding:env(safe-area-inset-top,0px) 0 env(safe-area-inset-bottom,0px)}
body{margin:0;font:14px/1.4 system-ui,sans-serif}
img{max-width:100%}
[hidden]{display:none!important}
</style>"""


def build_html() -> str:
    """Wrap the page source (head part + body part) into a complete HTML document."""
    src = SOURCE.read_text(encoding="utf-8")
    if HEAD_MARKER not in src:
        sys.exit(f"error: {SOURCE} is missing the '{HEAD_MARKER}' marker")
    head, body = src.split(HEAD_MARKER, 1)
    # The artifact-only viewport hint is harmless but unnecessary in a standalone file.
    head = re.sub(r'<meta name="claude:[^"]+"[^>]*>\s*', "", head)
    return (
        "<!doctype html>\n"
        '<html lang="en">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        f"{BASE_CSS}\n{head.strip()}\n</head>\n<body>\n{body.strip()}\n</body>\n</html>\n"
    )


def build() -> None:
    DIST.mkdir(exist_ok=True)
    OUTPUT.write_text(build_html(), encoding="utf-8")
    size_kb = OUTPUT.stat().st_size / 1024
    print(f"Built {OUTPUT.relative_to(ROOT)} ({size_kb:.0f} KB)")
    print("Double-click that file to open the course, or send it to someone.")


def serve() -> None:
    parser = argparse.ArgumentParser(prog="serve", description="Preview the course locally.")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--no-open", action="store_true", help="don't open a browser window")
    args = parser.parse_args(sys.argv[1:])

    build()
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(DIST))
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", args.port), handler) as httpd:
        url = f"http://localhost:{args.port}/"
        print(f"Serving at {url}  (press Ctrl+C to stop)")
        if not args.no_open:
            webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")
