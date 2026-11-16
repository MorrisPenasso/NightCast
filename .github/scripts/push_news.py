#!/usr/bin/env python3
"""
NIGHT//CAST Watch Deck v2 — push notizie RSS verso ntfy.sh
Novità: notifica clickabile -> apre watch.html, testo espanso (big text),
tag sorgente colorati. Configura i segreti del repo:
  NTFY_TOPIC   = nome del topic ntfy
  WATCH_URL    = URL della pagina watch.html (es. https://user.github.io/nightcast/watch.html)
"""
import json
import os
import pathlib
import re

import feedparser
import requests

SEEN_FILE = pathlib.Path("seen.json")
NTFY = "https://ntfy.sh"

FEEDS = [
    ("SKY", "https://tg24.sky.it/rss/tg24.xml"),
    ("CORR", "https://xml2.corriereobjects.it/rss/homepage.xml"),
    ("AGI", "https://www.agi.it/rss"),
]

MAX_PER_RUN = 6
TITLE_MAX = 80


def load_seen():
    if SEEN_FILE.exists():
        try:
            return set(json.loads(SEEN_FILE.read_text()))
        except Exception:
            pass
    return set()


def save_seen(seen):
    SEEN_FILE.write_text(json.dumps(sorted(list(seen))[-500:]))


def send(title, body):
    watch_url = os.environ.get("WATCH_URL", "").strip()
    headers = {
        "Title": title.encode("utf-8"),
        "Priority": "default",
        "Tags": "newspaper",
    }
    if watch_url:
        # bottone esplicito + tap sull'intera notifica
        headers["Actions"] = f"view, APRI DECK, {watch_url}, clear=true"
        headers["Click"] = watch_url
    r = requests.post(
        f"{NTFY}/{os.environ['NTFY_TOPIC']}",
        data=body.encode("utf-8"),
        headers=headers,
        timeout=15,
    )
    r.raise_for_status()  # ora un rifiuto di ntfy NON passa più in silenzio

def main():
    seen = load_seen()
    fresh = []

    for src, url in FEEDS:
        try:
            feed = feedparser.parse(url)
        except Exception as e:
            print(f"[!] {src}: {e}")
            continue
        for entry in feed.entries[:20]:
            link = entry.get("link", "")
            key = link or entry.get("title", "")
            if not key or key in seen:
                continue
            summary = entry.get("summary", "") or ""
            summary = re.sub(r"<[^>]+>", "", summary).strip()
            # formato espanso: sommario + link, leggibile trascinando la notifica
            expanded = summary[:400]
            if link:
                expanded += "\n\n📰 " + link
            fresh.append({
                "src": src,
                "title": entry.get("title", "(senza titolo)")[:TITLE_MAX],
                "body": expanded,
                "key": key,
            })

    if not fresh:
        print("Nessuna notizia nuova.")
        return

    sent = 0
    for n in fresh[:MAX_PER_RUN]:
        title = f"[{n['src']}] {n['title']}"
        try:
            send(title, n["body"])
            seen.add(n["key"])
            sent += 1
            print(f"[>] {title}")
        except Exception as e:
            print(f"[!] invio fallito ({e})")

    save_seen(seen)
    print(f"Inviate {sent} notifiche.")


if __name__ == "__main__":
    main()
