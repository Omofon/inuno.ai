import os
import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from django.utils.text import slugify
from urllib.parse import urljoin
from ..models import Article, Category
import logging
import shortuuid

logger = logging.getLogger(__name__)

# Set your Hugging Face API key
HUGGING_FACE_API_KEY = os.getenv("HUGGING_FACE_API_KEY")
HUGGING_FACE_SUMMARIZATION_URL = (
    "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
)

headers = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}


def summarize_text(text):
    try:
        response = requests.post(
            HUGGING_FACE_SUMMARIZATION_URL,
            headers=headers,
            json={
                "inputs": text,
                "parameters": {"max_length": 150, "min_length": 50, "do_sample": False},
            },
        )
        response.raise_for_status()
        summary = response.json()[0].get("summary_text", text)
        return summary
    except Exception as e:
        logger.error(f"Error during summarization: {e}")
        return text  # Return original text if summarization fails


def fetch_full_content_and_image(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract main content
        content = soup.find("article") or soup.find("div", class_="content")
        full_content = content.get_text(separator="\n").strip() if content else None

        # Extract main image
        image_url = None
        if content:
            image_tag = content.find("img")
            if image_tag and "src" in image_tag.attrs:
                image_url = image_tag["src"]

        if not image_url:
            og_image = soup.find("meta", property="og:image")
            if og_image and og_image.get("content"):
                image_url = og_image["content"]

        if not image_url:
            image_tag = soup.find("figure img") or soup.find("img")
            if image_tag and "src" in image_tag.attrs:
                image_url = image_tag["src"]

        if image_url:
            image_url = urljoin(response.url, image_url)

        return full_content, image_url
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed for {url}: {e}")
        return None, None
    except Exception as e:
        logger.error(f"Error processing content or image for {url}: {e}")
        return None, None


def fetch_and_process_rss(feed_url):
    feed = feedparser.parse(feed_url)
    articles = []

    logger.debug(f"Parsing feed: {feed_url}")
    logger.debug(f"Found {len(feed.entries)} entries in feed.")

    for entry in feed.entries[:10]:  # Limit entries to avoid processing overload
        try:
            logger.debug(f"Processing entry: {entry.title}")

            full_content, image_url = fetch_full_content_and_image(entry.link)
            logger.debug(f"Full content fetched for: {entry.title}")

            content_to_process = (
                full_content or entry.get("summary") or entry.get("description")
            )

            # Use the Hugging Face API to summarize the content
            summary = summarize_text(content_to_process)
            logger.debug(f"Generated summary for: {entry.title}")

            title = entry.title
            source_url = entry.link
            published_date = (
                datetime(*entry.published_parsed[:6])
                if entry.get("published_parsed")
                else datetime.now()
            )
            category_name = entry.get("category", "Uncategorized")
            category, _ = Category.objects.get_or_create(name=category_name)

            slug = slugify(title) + "-" + shortuuid.uuid()[:8]

            article, created = Article.objects.update_or_create(
                title=title,
                defaults={
                    "slug": slug,
                    "content": summary,
                    "source_url": source_url,
                    "image_url": image_url,
                    "published_date": published_date,
                    "category": category,
                },
            )
            articles.append(article)
            logger.debug(
                f"{'Created' if created else 'Updated'} article: {article.title}"
            )
        except Exception as e:
            logger.error(f"Error processing article from {feed_url}: {e}")

    return articles
