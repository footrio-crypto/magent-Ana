import feedparser


RSS_FEEDS = {
    "Gold": [
        "https://feeds.marketwatch.com/marketwatch/commodities",
        "https://www.kitco.com/rss",
    ],
    "Silver": [
        "https://feeds.marketwatch.com/marketwatch/commodities",
        "https://www.kitco.com/rss",
    ],
    "DBS": [
        "https://feeds.finance.yahoo.com/rss/2.0/headline?s=D05.SI&region=US&lang=en-US",
    ],
    "Bank of China": [
        "https://feeds.finance.yahoo.com/rss/2.0/headline?s=3988.HK&region=US&lang=en-US",
    ],
    "AI Stocks": [
        "https://feeds.finance.yahoo.com/rss/2.0/headline?s=NVDA&region=US&lang=en-US",
        "https://feeds.finance.yahoo.com/rss/2.0/headline?s=AMZN&region=US&lang=en-US",
        "https://feeds.finance.yahoo.com/rss/2.0/headline?s=GOOGL&region=US&lang=en-US",
        "https://feeds.finance.yahoo.com/rss/2.0/headline?s=AVGO&region=US&lang=en-US",
    ],
}


POSITIVE_WORDS = [
    "buy", "bullish", "upgrade", "outperform", "strong",
    "gain", "rally", "record", "surge", "higher",
    "accumulate", "positive", "growth", "beat"
]

NEGATIVE_WORDS = [
    "sell", "bearish", "downgrade", "risk", "weak",
    "fall", "drop", "decline", "correction", "lower",
    "overvalued", "pressure", "miss", "slowdown"
]


def score_headline(text):
    text_lower = text.lower()

    positive = sum(1 for word in POSITIVE_WORDS if word in text_lower)
    negative = sum(1 for word in NEGATIVE_WORDS if word in text_lower)

    return positive, negative


def get_sentiment_label(positive, negative):
    if positive > negative:
        return "Bullish / Positive"
    if negative > positive:
        return "Bearish / Cautious"
    return "Neutral / Mixed"


def collect_market_views(max_items_per_asset=5):
    views = {}

    for asset, feeds in RSS_FEEDS.items():
        headlines = []
        positive_total = 0
        negative_total = 0

        for feed_url in feeds:
            feed = feedparser.parse(feed_url)

            for entry in feed.entries[:max_items_per_asset]:
                title = entry.get("title", "").strip()
                link = entry.get("link", "").strip()

                if not title:
                    continue

                positive, negative = score_headline(title)
                positive_total += positive
                negative_total += negative

                headlines.append({
                    "title": title,
                    "link": link
                })

        views[asset] = {
            "sentiment": get_sentiment_label(positive_total, negative_total),
            "positive_score": positive_total,
            "negative_score": negative_total,
            "headlines": headlines[:max_items_per_asset]
        }

    return views


def format_market_views(views):
    text = "\nExternal Market Views\n"
    text += "----------------------\n"

    for asset, data in views.items():
        text += f"\n{asset}: {data['sentiment']}\n"
        text += f"Positive score: {data['positive_score']} | Negative score: {data['negative_score']}\n"

        for item in data["headlines"]:
            text += f"- {item['title']}\n"

    return text
