## Hacker News Crawler

### Description

A Python-based asynchronous web crawler to fetch and save the top stories and comments from Hacker News. This script periodically scans the Hacker News website to download the latest top stories and their associated comments, saving the data to disk for further analysis or archival purposes.

### Features
- Asynchronous Fetching: Utilizes aiohttp for efficient asynchronous HTTP requests.
- Periodic Scanning: Periodically scans Hacker News for new top stories every 5 minutes.
- HTML Parsing: Uses BeautifulSoup to parse HTML and extract relevant links.
- Robust Error Handling: Includes retries and delays to handle network issues and server disconnections.
- Data Storage: Saves fetched HTML pages to disk for offline access and further processing.

### Prerequisites

- Python 3.10+
- aiohttp 3.9.3+
- beautifulsoup4 4.12.3+
- aiofiles 23.2.1+