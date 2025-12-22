import asyncio
from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CrawlerRunConfig,
    DefaultMarkdownGenerator,
    PruningContentFilter,
    CrawlResult,
)


def crawl_url(url: str, headless: bool = True, verbose: bool = False) -> str:
    """
    Synchronously crawl a given URL and return the content as Markdown string.

    Args:
        url (str): The URL to crawl.
        headless (bool): Whether to run browser in headless mode. Default is True.
        verbose (bool): Whether to enable verbose logging. Default is False.

    Returns:
        str: The crawled content in Markdown format, or error message.
    """

    async def _async_crawl():
        browser_config = BrowserConfig(
            headless=headless,
            verbose=verbose,
        )
        async with AsyncWebCrawler(config=browser_config) as crawler:
            crawler_config = CrawlerRunConfig(
                markdown_generator=DefaultMarkdownGenerator(
                    content_filter=PruningContentFilter()
                ),
            )
            try:
                result: CrawlResult = await crawler.arun(url=url, config=crawler_config)
                return result.markdown.raw_markdown
            except Exception as e:
                return f"Error: {str(e)}"

    return asyncio.run(_async_crawl())
