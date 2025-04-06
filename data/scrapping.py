import feedparser
import json
import os
import time
from newspaper import Article

# Direct RSS Feed for Oracle News
RSS_FEED_URL = "https://techcrunch.com/tag/oracle/feed/"

# Directory to save scraped data
DATA_DIR = "data/oracle_scraped_data"
os.makedirs(DATA_DIR, exist_ok=True)

# Number of articles to scrape
MAX_ARTICLES = 200

def scrape_oracle_news():
    feed = feedparser.parse(RSS_FEED_URL)
    news_list = []
    count = 0  # Track successfully scraped articles

    for entry in feed.entries:
        if count >= MAX_ARTICLES:
            break  # Stop after scraping MAX_ARTICLES

        article_url = entry.link

        try:
            article = Article(article_url)
            article.download()
            article.parse()

            # Skip if content is empty
            if not article.text.strip():
                print(f"Skipping (no content): {article_url}")
                continue

            news_item = {
                "title": article.title if article.title else "No Title",
                "published": entry.published if hasattr(entry, "published") else "Unknown Date",
                "url": article_url,
                "content": article.text
            }
            news_list.append(news_item)
            count += 1

            print(f"Scraped [{count}/{MAX_ARTICLES}]: {article.title}")

            # Avoid hitting servers too fast
            time.sleep(2)

        except Exception as e:
            print(f"Failed to scrape: {article_url} | Error: {str(e)}")

    # Save results as JSON
    file_path = os.path.join(DATA_DIR, "oracle_news.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(news_list, f, indent=4)

    print(f"\n{len(news_list)} Oracle news articles saved in {file_path}!")

# Run scraper
scrape_oracle_news()
