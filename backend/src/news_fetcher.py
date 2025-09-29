import requests
from datetime import datetime, timedelta
from dateutil import parser as date_parser

def fetch_legal_news(news_api_key: str, page_size: int = 5):
    """
    Fetches the latest trending legal news articles with readable dates.
    Returns a list of dictionaries with keys: title, url, publishedAt, publishedAtFormatted, source, description.
    """
    today = datetime.today().strftime('%Y-%m-%d')
    last_week = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')

    url = (
        "https://newsapi.org/v2/everything?"
        "q=("
        "%22court ruling%22 OR %22supreme court%22 OR %22high court%22 OR lawsuit OR "
        "%22legal battle%22 OR %22constitutional law%22 OR %22judicial decision%22 OR "
        "%22human rights law%22 OR %22legal reform%22 OR %22legislation passed%22"
        ") AND NOT entertainment AND NOT cinema AND NOT film AND NOT tv AND NOT drama&"
        f"from={last_week}&to={today}&"
        "language=en&"
        "sortBy=popularity&"
        f"pageSize={page_size}&"
        f"apiKey={news_api_key}"    
    )

    response = requests.get(url)
    if response.status_code != 200:
        print(f"Warning: Unable to fetch news, status code: {response.status_code}")
        return []

    articles = response.json().get("articles", [])
    formatted_articles = []

    for article in articles:
        published_at = article.get("publishedAt")
        try:
            published_at_dt = date_parser.parse(published_at)
            published_at_formatted = published_at_dt.strftime('%d %b %Y, %H:%M')
        except Exception:
            published_at_formatted = "Unknown"

        formatted_articles.append({
            "title": article.get("title"),
            "url": article.get("url"),
            "publishedAt": published_at,
            "publishedAtFormatted": published_at_formatted,
            "source": article.get("source", {}).get("name"),
            "description": article.get("description")
        })

    return formatted_articles
