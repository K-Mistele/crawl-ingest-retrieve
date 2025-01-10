import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, DefaultMarkdownGenerator, PruningContentFilter

async def main():
    print('running')

    browser_config = BrowserConfig(
        browser_type='chromium',
        headless=True,
        extra_args=["--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox"],  # better args for docker
    )

    markdown_generator_config = DefaultMarkdownGenerator(
        content_filter=None,
        options={
            "ignore_links": True,
            "body_width": 40,
            "ignore_images": True,
            "skip_internal_links": True,
            "include_sup_sub": True
        }
    )

    crawler_config = CrawlerRunConfig(
        word_count_threshold=10,
        only_text=True,
        markdown_generator=markdown_generator_config,
        content_filter=None,
        exclude_external_links=True,
        exclude_social_media_links=True,
        exclude_external_images=False,  # images may be loaded from CDN
        excluded_tags=['script', 'style', 'footer', 'nav'],
        disable_cache=True,  # don't cache to prevent memory leaks
        bypass_cache=True
    )

    crawler = AsyncWebCrawler(config=browser_config)
    await crawler.start()
    result = await crawler.arun(
        url='https://help.letterstream.com/article/464-why-do-i-get-charged-for-deleting-a-job',

    )
    await crawler.close()
    with open('output.md', 'w') as f:
        f.write(result.markdown_v2.raw_markdown)
    print(result.markdown_v2.fit_markdown)


if __name__ == '__main__':
    asyncio.run(main())