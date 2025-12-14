# Facebook Comments Crawler - Technical Documentation

## Overview

This project implements two spiders for Facebook data extraction:
- **comments.py**: Extracts comments from a single Facebook post
- **timeline.py**: Crawls fan page timeline and extracts comments from multiple posts

## Spiders

### comments.py

**Purpose**: Extract comments from a single Facebook post

**Key Features**:
- Facebook authentication via mbasic interface
- CSRF token extraction and handling
- XPath-based comment extraction
- Pagination support through "see_next" links
- Configurable download delays

**Usage**:
```bash
cd fb_comments_crawler
scrapy crawl comments
```

**Configuration**:
- Update `login_url`, `email`, `password` in spider class
- Set `post_urls` list with target post URLs
- Adjust `DOWNLOAD_DELAY` in custom_settings

### timeline.py

**Purpose**: Crawl fan page timeline and extract comments from multiple posts

**Key Features**:
- Timeline navigation and post link extraction
- Iterates through multiple posts
- Comment extraction with per-post limits
- Random delays between requests (2-10 seconds)
- Configurable maximum comments per post and pages to crawl

**Usage**:
```bash
cd fb_comments_crawler
scrapy crawl timeline
```

**Configuration**:
- Update `target_url` with fan page URL
- Set `max_comment` for comments per post limit
- Adjust `visit_count` limit for timeline pages

## Data Structure

### FbCommentsCrawlerItem

```python
{
    'name': str,    # Comment author name
    'cmt': str,     # Comment content
    'time': str     # Comment timestamp
}
```

## Implementation Details

### Authentication

The spiders use Facebook's mbasic interface for easier HTML parsing:
- Extract CSRF token (`fb_dtsg`) from login form
- Submit credentials via FormRequest
- Verify login success before proceeding

### HTML Parsing

**Comment Extraction Strategy**:
1. Locate comment container using ID pattern: `//*[@id[starts-with(., "ufi")]]`
2. Identify comment section by finding div without ID attribute
3. Extract individual comments using XPath selectors
4. Handle pagination through "see_prev" and "see_next" elements

**XPath Selectors Used**:
- Comment author: `div/h3/a/text()`
- Comment content: `div/div/text()`
- Comment timestamp: `div/div[@class="_52jc _52j9 _52jg"]/abbr/text()`

### Rate Limiting

To respect Facebook's community standards:
- Fixed delays: `DOWNLOAD_DELAY = 2` seconds
- Random delays: `np.random.randint(2, 10)` seconds
- Comment limits per post to avoid excessive requests

## Configuration

### settings.py

Key settings:
- `ROBOTSTXT_OBEY = False`: Disable robots.txt compliance (required for Facebook)
- `FEED_FORMAT = 'json'`: Output format
- `FEED_URI = 'output.json'`: Output file path
- `DOWNLOAD_DELAY`: Delay between requests (set in spider custom_settings)

### Spider Custom Settings

Each spider can override global settings:
```python
custom_settings = {
    'DOWNLOAD_DELAY': 2  # 2 second delay between requests
}
```

## Troubleshooting

**Login Fails**:
- Verify credentials are correct
- Check if Facebook requires 2FA or additional verification
- Ensure CSRF token extraction is working

**No Comments Extracted**:
- Verify XPath selectors match current Facebook HTML structure
- Check if post actually has comments
- Inspect page source to verify element structure

**Rate Limiting**:
- Increase `DOWNLOAD_DELAY`
- Reduce number of posts/comments to crawl
- Add longer random delays

---

## Collaboration Credits

This project was originally developed as a group project for CSC17001 - Intelligent Data Analysis course (April-May 2024). Contributors during the collaboration period:

- **huyinf**: Initial project setup, core comments.py spider implementation, initial timeline.py spider, project documentation
- **Nguyễn Chí Cường**: Comments.py refactoring and optimization, timeline.py major updates and enhancements, items.py improvements  
- **VongoctriZ** (project maintainer): fb_page.py spider implementation, final code integration, project finalization

The project reached its final collaborative state on May 12, 2024. Subsequent improvements and maintenance have been done independently by VongoctriZ.
