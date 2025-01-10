import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, DefaultMarkdownGenerator, PruningContentFilter

async def main():
    print('running')

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

    crawler = AsyncWebCrawler(config=browser_config)
    await crawler.start()
    result = await crawler.arun(
        url='https://constellate.ai',
        config=crawler_config,
        bypass_cache=True,
        disable_cache=True,
    )
    await crawler.close()
    with open('output.md', 'w') as f:
        f.write(result.markdown_v2.raw_markdown)
    print(result.markdown_v2.fit_markdown)


if __name__ == '__main__':
    asyncio.run(main())