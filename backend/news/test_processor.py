from news.collector import collect_all_sources, is_transfer_article
from news.processor import process_article


articles = collect_all_sources()

transfer_candidates = [
    article
    for article in articles
    if is_transfer_article(article)
]

print(f"Total articles: {len(articles)}")
print(f"Transfer candidates: {len(transfer_candidates)}")


for article in transfer_candidates[:3]:
    print("\nProcessing:", article["title"])

    rumour = process_article(article)

    if rumour:
        print("Saved:", rumour)
    else:
        print("Skipped")