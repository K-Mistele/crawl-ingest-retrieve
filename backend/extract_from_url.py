import asyncio
import time

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, DefaultMarkdownGenerator, PruningContentFilter
from typing import List, Dict
from dotenv import load_dotenv
import os
import requests

load_dotenv()
api_url = os.getenv('CRAWLER_URL')
token = os.getenv('CRAWLER_API_TOKEN')


browser_config = BrowserConfig(
    browser_type='chromium',
    headless=True,
    extra_args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"], # better args for docker
)

content_filter = PruningContentFilter(
    threshold=0.1,
    threshold_type='dynamic',
    min_word_threshold=5,
)

markdown_generator_config = DefaultMarkdownGenerator(
    content_filter=content_filter,
)

crawler_config = CrawlerRunConfig(
    markdown_generator=markdown_generator_config,
    content_filter=content_filter,
    exclude_external_links=True,
    exclude_social_media_links=True,
    exclude_external_images=False, # images may be loaded from CDN
    verbose=True,
    word_count_threshold=5,
    excluded_tags=['script', 'style', 'footer', 'nav']
)

async def crawl_urls(domain: str, urls: List[str], existing_crawler: AsyncWebCrawler | None=None):

    crawler = existing_crawler if existing_crawler else AsyncWebCrawler(config=browser_config)


    # TODO crawl all the URLs; check for new ones.

    # recurse if true

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url='https://letterstream.com',
            config=crawler_config,
        )
        with open('raw_markdown.md', 'w') as f:
            f.write(result.markdown)
        with open('fit_markdown.md', 'w') as f:
            f.write(result.markdown_v2.fit_markdown)

        for link in result.links['internal']:
            print(link['href'])