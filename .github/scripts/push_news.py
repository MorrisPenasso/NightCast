#!/usr/bin/env python3
"""
NIGHT//CAST Watch Deck — push notizie RSS verso ntfy.sh
Da mettere in .github/scripts/push_news.py nel repo.
Configura i segreti del repo:
  NTFY_TOPIC = nome del topic ntfy (es. nightcast-x7k2-tuonome)
"""
import json
import os
import pathlib

import feedparser
import requests

SEEN_FILE = pathlib.Path("seen.json")
NTFY = "https://ntfy.sh"

FEEDS = [
    ("SKY", "https://tg24.sky.it/rss/tg24.xml"),
    ("CORR", "https://xml2.corriereobjects.it/rss/homepage.xml"),
    ("AGI", "https://www.agi.it/rss"),
]

MAX_PER_RUN = 6          # non floodare il polso
TITLE_MAX = 80           # taglio titoli lunghi (schermo watch piccolo)


def load_seen():
    if SEEN_FILE.exists():
        try:
            return set(json.loads(SEEN_FILE.read_text()))
        except Exception:
            pass
    return set()


def save_seen(seen):
    # tieni solo gli ultimi 500 per non far crescere il file all'infinito
    SEEN_FILE.write_text(json.dumps(sorted(list(seen))[-500:]))


def send(title, body):
    requests.post(
        f"{NTFY}/{os.environ['NTFY_TOPIC']}",
        data=body.encode("utf-8"),
        headers={
            "Title": title.encode("utf-8"),
            "Priority": "default",
            "Tags": "newspaper",
        },
        timeout=15,
    )


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
            # pulizia HTML dal sommario
            import re
            summary = re.sub(r"<[^>]+>", "", summary).strip()[:200]
            fresh.append({
                "src": src,
                "title": entry.get("title", "(senza titolo)")[:TITLE_MAX],
                "summary": summary,
                "key": key,
            })

    if not fresh:
        print("Nessuna notizia nuova.")
        return

    sent = 0
    for n in fresh[:MAX_PER_RUN]:
        title = f"[{n['src']}] {n['title']}"
        body = n["summary"] or "-"
        try:
            send(title, body)
            seen.add(n["key"])
            sent += 1
            print(f"[>] {title}")
        except Exception as e:
            print(f"[!] invio fallito ({e})")

    save_seen(seen)
    print(f"Inviate {sent} notifiche.")


if __name__ == "__main__":
    main()
