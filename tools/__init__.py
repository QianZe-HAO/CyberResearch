from .synbolic_math import (
    differentiate,
    integrate_expression,
    solve_equation,
    matrix_operation,
    preprocess_math,
    calculate,
)
from .date_time import (
    get_current_datetime,
    get_current_timestamp,
    convert_timestamp_to_datetime,
)
from .web_search import internet_search
from dotenv import load_dotenv
import os

load_dotenv()
USE_CRAWL4AI = os.getenv("USE_CRAWL4AI", "False").lower() == "true"

if USE_CRAWL4AI:
    from .web_crawler import crawl_url
    print("Using Crawl4AI for web crawling")
else:
    from .web_search import crawl_url
    print("Using Tavily for web crawling")


__all__ = [
    internet_search,
    crawl_url,
    get_current_datetime,
    get_current_timestamp,
    convert_timestamp_to_datetime,
    differentiate,
    integrate_expression,
    solve_equation,
    matrix_operation,
    preprocess_math,
    calculate,
]
