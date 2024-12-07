from django.http import JsonResponse
from .rss_feed_aggregator import fetch_and_process_rss
import logging

logger = logging.getLogger(__name__)


def refresh_articles(request):
    """Fetch latest articles from configured RSS feeds."""
    # List of RSS feed URLs
    rss_feeds = [
        "https://rss.cnn.com/rss/edition.rss",
        # Add more RSS feeds as needed
    ]

    new_articles = []
    errors = []

    for feed_url in rss_feeds:
        try:
            logger.debug(f"Fetching articles from feed: {feed_url}")
            articles = fetch_and_process_rss(feed_url)
            new_articles.extend(articles)
            logger.debug(f"Fetched {len(articles)} articles from {feed_url}")
        except Exception as e:
            error_message = f"Error fetching RSS feed {feed_url}: {str(e)}"
            errors.append(error_message)
            logger.error(error_message)

    response_data = {
        "message": (
            "Articles refreshed successfully."
            if not errors
            else "Partial refresh completed with errors."
        ),
        "new_articles_count": len(new_articles),
        "errors": errors,
    }

    return JsonResponse(response_data, status=200 if not errors else 207)
