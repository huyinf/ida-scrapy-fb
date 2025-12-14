# Facebook Comments Crawler

A web scraping project using Scrapy framework to extract comments from Facebook fan pages. This tool crawls Facebook timeline posts and extracts structured comment data including author names, content, and timestamps.

## Features

- Facebook authentication via mbasic interface
- Timeline crawling to collect post links
- Comment extraction with pagination support
- Structured JSON data export
- Configurable rate limiting

## Installation

```bash
pip install scrapy lxml parsel w3lib twisted cryptography pyOpenSSL numpy
```

## Quick Start

### Crawl Comments from a Single Post

```bash
cd fb_comments_crawler
scrapy crawl comments
```

### Crawl Timeline and Multiple Posts

```bash
cd fb_comments_crawler
scrapy crawl timeline
```

## Configuration

Before running, update credentials and URLs in the spider files:
- `email` and `password` in spider classes
- `target_url` or `post_urls` for target pages
- `max_comment` and `DOWNLOAD_DELAY` for rate limiting

## Output

Data is exported to `output.json` with structure:
```json
{
  "name": "User Name",
  "cmt": "Comment content",
  "time": "Timestamp"
}
```

## Project Structure

```
fb_comments_crawler/
├── fb_comments_crawler/
│   ├── spiders/
│   │   ├── comments.py      # Single post comment extraction
│   │   └── timeline.py      # Timeline crawling and multi-post extraction
│   ├── items.py             # Data structure definitions
│   ├── pipelines.py         # Data processing pipeline
│   ├── middlewares.py       # Request/response middleware
│   └── settings.py          # Scrapy configuration
├── output.json              # Scraped data output
└── scrapy.cfg               # Project configuration
```

## Limitations

- Requires valid Facebook credentials
- Subject to Facebook's rate limiting and anti-scraping measures
- May need adjustments if Facebook changes their HTML structure
- Video posts are excluded (mbasic view doesn't display comments)

For detailed technical documentation, see [fb_comments_crawler/README.md](fb_comments_crawler/README.md).

---

## Collaboration Credits

This project was originally developed as a group project for CSC17001 - Intelligent Data Analysis course. The following contributors participated during the collaboration period (April-May 2024):

- **huyinf**: Initial project setup, core comments.py spider implementation, initial timeline.py spider, project documentation
- **Nguyễn Chí Cường**: Comments.py refactoring and optimization, timeline.py major updates and enhancements, items.py improvements
- **VongoctriZ** (project maintainer): fb_page.py spider implementation, final code integration, project finalization

The project reached its final collaborative state on May 12, 2024. Subsequent improvements and maintenance have been done independently by VongoctriZ.
