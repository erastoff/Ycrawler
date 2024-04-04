import os
import time

import aiofiles
import aiohttp
import asyncio

from bs4 import BeautifulSoup

CACHE = dict()
BASE_URL = "https://news.ycombinator.com/"
COMMENT_URL_TEMPLATE = "https://news.ycombinator.com/item?id={}"


async def fetch_page(session, url, aim="top news"):
    async with session.get(url, timeout=60) as response:
        if response.status == 200:
            return await response.text(encoding="latin1")
        else:
            print(f"Failed to fetch {aim}:", response.status, url)
            return None


async def fetch_comment_links(session, id):
    html_comment = await fetch_page(
        session, COMMENT_URL_TEMPLATE.format(id), "comment page"
    )
    soup = BeautifulSoup(html_comment, "html.parser")
    span_tags = soup.find_all("span", class_="commtext c00")
    links = []
    for tag in span_tags:
        a_tag = tag.find("a")
        if a_tag:
            href = a_tag.get("href")
            links.append(href)
    for num, link in enumerate(links):
        html_content = await fetch_page(session, link, "link from comment")
        if html_content:
            filename = f"pages/id{id}/comment_links/link_{num}.html"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            async with aiofiles.open(filename, "w") as f:
                await f.write(html_content)


async def save_links(filename, links):
    async with aiofiles.open(filename, "w") as f:
        for link in links:
            await f.write(f"{link}\n")


async def main():
    async with aiohttp.ClientSession() as session:
        while True:
            print("-->Pages processing started at:", time.strftime("%H:%M:%S"))
            html_content = await fetch_page(session, BASE_URL)
            if html_content:
                soup = BeautifulSoup(html_content, "html.parser")
                athing_tags = soup.find_all("tr", class_="athing")
                ids = []
                for tag in athing_tags:
                    ids.append(tag.get("id"))

                span_tags = soup.find_all("span", class_="titleline")
                links = []
                for span_tag in span_tags:
                    a_tag = span_tag.find("a")
                    if a_tag:
                        href = a_tag.get("href")
                        links.append(href)

                new_map = dict(zip(ids, links))
                new_links = []
                for key in new_map.keys():
                    if key not in CACHE:
                        if new_map[key].startswith("item?"):
                            html_content = await fetch_page(
                                session, BASE_URL + new_map[key]
                            )
                        else:
                            html_content = await fetch_page(session, new_map[key])
                        CACHE[key] = new_map[key]
                        new_links.append(new_map[key])
                        if html_content:
                            filename = f"pages/id{key}/page_id{key}.html"
                            os.makedirs(os.path.dirname(filename), exist_ok=True)
                            async with aiofiles.open(filename, "w") as f:
                                await f.write(html_content)
                        await fetch_comment_links(session, key)

                if len(new_links):
                    print(f"{len(new_links)} pages added!")
                    await save_links("diff_links.txt", new_links)

                print("<--Pages processing finished at:", time.strftime("%H:%M:%S"))
                await asyncio.sleep(300)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server process finished.")
