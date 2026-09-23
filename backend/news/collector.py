import feedparser
from datetime import datetime, timezone

from .sources import RSS_SOURCES


def fetch_feed(feed_url):
    feed = feedparser.parse(feed_url)

    articles = []

    for entry in feed.entries:

        published_at = entry.get("published_parsed")

        if published_at:
            published_at = datetime(
                published_at.tm_year,
                published_at.tm_mon,
                published_at.tm_mday,
                published_at.tm_hour,
                published_at.tm_min,
                published_at.tm_sec,
                tzinfo=timezone.utc,
            )

        article = {
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "description": entry.get("description", ""),
            "published_at": published_at,
        }

        articles.append(article)

    return articles


def collect_all_sources():
    all_articles = []

    for source in RSS_SOURCES:
        print(f"Fetching: {source['name']}")

        articles = fetch_feed(source["url"])

        print(f"Found {len(articles)} articles")

        for article in articles:
            article["source"] = source["name"]

        all_articles.extend(articles)

    return all_articles

TRANSFER_KEYWORDS = [
    "transfer",
    "signing",
    "join",
    "transfer target",
    "transfer interest",
    "transfer talks",
    "in talks",
    "negotiations",
    "bid",
    "offer",
    "agreement",
    "loan",
    "move to",
    "linked with",
    "linked to",
    "transfer window",
]

def is_transfer_article(article):
    text = (
        article["title"] + " " + article["description"]
    ).lower()

    return any(keyword in text for keyword in TRANSFER_KEYWORDS)

if __name__ == "__main__":
    articles = collect_all_sources()

    transfer_articles = [
        article
        for article in articles
        if is_transfer_article(article)
    ]

    print(f"Total articles: {len(articles)}")
    print(f"Transfer-related articles: {len(transfer_articles)}")

    for article in transfer_articles[:10]:
        print(article)