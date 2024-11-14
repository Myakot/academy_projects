import aiohttp
import asyncio
import json

semaphore = asyncio.Semaphore(5)

urls = [
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url"
]


async def fetch_url(session, url):
    async with semaphore:
        try:
            async with session.get(url) as response:
                return url, response.status
        except aiohttp.ClientError:
            return url, 0

async def fetch_urls(urls, file_path):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

    # Save results to a file
    with open(file_path, 'w') as f:
        for url, status_code in results:
            json.dump({'url': url, 'status_code': status_code}, f)
            f.write('\n')

if __name__ == '__main__':
    print('script launch')
    asyncio.run(fetch_urls(urls, './results.json'))
    print('script end')
