import asyncio
import time
import xmltodict
import psutil
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, DefaultMarkdownGenerator, PruningContentFilter
from typing import List, Dict, Mapping
from dotenv import load_dotenv
import os
import requests
from urllib.parse import urlparse

load_dotenv()
api_url = os.getenv('CRAWLER_URL')
token = os.getenv('CRAWLER_API_TOKEN')

def extract_sitemap(domain: str) -> List[str] | None:
    try:
        url = f'https://{domain}/sitemap.xml'
        response = requests.get(url)
        if response.status_code != 200:
            print(f'No sitemap available for {domain}')
            return None

        data = response.text

        sitemap = xmltodict.parse(data)['urlset'] # the top-level element is <urlset>
        urls = [url['loc'] for url in sitemap['url']]
        return urls
    except requests.exceptions.RequestException as e:
        print(f'Unable to get sitemap for domain {domain}:', e)
    except requests.exceptions.ConnectTimeout as e:
        print(f'Unable to reach {domain} in time', e)
    return None

browser_config = BrowserConfig(
    browser_type='chromium',
    headless=True,
    extra_args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"],  # better args for docker
)

content_filter = PruningContentFilter(
    threshold=0.2,
    threshold_type='dynamic',
    #min_word_threshold=10,
)

markdown_generator_config = DefaultMarkdownGenerator(
    content_filter=content_filter,
    options={
        "ignore_links": True,
        "body_width": 120,
        "ignore_images": True,
        "skip_internal_links": True,
        "include_sup_sub": True
    }
)

crawler_config = CrawlerRunConfig(
    word_count_threshold=10,
    only_text=True,
    markdown_generator=markdown_generator_config,
    exclude_external_links=True,
    exclude_social_media_links=True,
    exclude_external_images=False,  # images may be loaded from CDN
    excluded_tags=['script', 'style', 'footer', 'nav'],
)


def log_memory(prefix: str=''):
    process = psutil.Process(os.getpid())
    current_mem = process.memory_info().rss  # in bytes
    print(f'{"["+prefix+"] " if prefix else ''}Current memory: {current_mem // (1024 * 1024)} MB')


async def scrape_domain(domain: str, max_concurrent: int = None):
    sitemap_urls = extract_sitemap(domain)

    crawler = AsyncWebCrawler(config=browser_config)
    await crawler.start()

    # mock up a memory cache
    crawled_urls = []
    try:
        if sitemap_urls:
            print(f'Got {len(sitemap_urls)} URLs from sitemap')
            results, new_links = await crawl_urls(domain, sitemap_urls, crawler, max_concurrent=20)
            print('(ignored): new links', new_links)
        else:
            print("trying to get regular domain")
    finally:
        print('Closing crawler...')
        await crawler.close()


async def crawl_urls(domain: str, urls: List[str], crawler: AsyncWebCrawler, max_concurrent=None) -> (Dict[str, str], List[str]):
    """

    :param domain: the domain we should limit results to
    :param urls: the list of URLs to crawl
    :param crawler:  the crawler instance
    :param max_concurrent: the number of URLs we can crawl concurrently
    :return: a map of URLs to their page content in markdown, AND a list of newly discovered URLs
    """

    batch_size = max_concurrent if max_concurrent else len(urls)
    url_result_mappings: Dict[str, str] = {}
    unique_links = set()
    final_links_same_domain = []

    try:
        print(f'Crawling {len(urls)} URLs')
        success_count = 0
        fail_count = 0

        for i in range(0, len(urls), batch_size):
            batch = urls[i: i + batch_size]
            tasks = []

            # create a batch
            for j, url in enumerate(batch):
                session_id = f'parallel_session_{i + j}'
                task = crawler.arun(
                    url=url,
                    config=crawler_config,
                    session_id=session_id,
                    bypass_cache=True,
                    disable_cache=True,
                )
                tasks.append(task)


            log_memory(prefix=f'Before batch {i//batch_size + 1}')
            results = await asyncio.gather(*tasks, return_exceptions=True)
            log_memory(prefix=f'After batch {i//batch_size + 1}')

            # evaluate results
            for url, result in zip(batch, results):
                if isinstance(result, Exception):
                    print(f'Error crawling URL {url}: {result}')
                    fail_count += 1
                elif result.success:
                    success_count += 1
                    internal_links = [item['href'].split('#')[0].split('?')[0] for item in result.links['internal']] # each has href, title, text, base_domain
                    url_result_mappings[url] = result.markdown
                    unique_links.update(set(internal_links))

                else:
                    fail_count += 1

            print(f'Successfully crawled {success_count}')
            print(f'Failed: {fail_count}')
            unique_links = unique_links.difference(set(urls))
            for link in unique_links:
                link_domain = urlparse(link).netloc
                if domain == link_domain or domain == 'www.' + link_domain:
                    final_links_same_domain.append(link)

    finally:
        print('crawling done')
        return url_result_mappings, final_links_same_domain

if __name__ == '__main__':

    asyncio.run(scrape_domain('help.letterstream.com'))