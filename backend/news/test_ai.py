from news.collector import collect_all_sources, is_transfer_article
from news.ai_processor import extract_transfer_info


articles = collect_all_sources()

transfer_candidates = [
    article
    for article in articles
    if is_transfer_article(article)
]

print(f"Total articles: {len(articles)}")
print(f"Transfer candidates: {len(transfer_candidates)}")

for article in transfer_candidates:
    result = extract_transfer_info(article)

    print("\nTITLE:", article["title"])
    print("AI:", result)