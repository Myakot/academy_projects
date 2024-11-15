import aiohttp
import asyncio
import json
from asyncio import Queue

semaphore = asyncio.Semaphore(99)

urls = [
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url"
]

queue = Queue()
results_queue = Queue()

async def queue_worker(session):
    while True:
        url = await queue.get()
        result = await fetch_url(session, url)
        await results_queue.put(result)
        queue.task_done()

async def fetch_url(session, url):
    async with semaphore:
        try:
            async with session.get(url) as response:
                return url, response.status
        except aiohttp.ClientError:
            return url, 0

async def fetch_urls(urls, file_path):
    async with aiohttp.ClientSession() as session:
        queue_workers = [queue_worker(session) for _ in range(99)]
        await asyncio.gather(*queue_workers)

        for url in urls:
            await queue.put(url)

        await queue.join()

        results = []
        while not results_queue.empty():
            results.append(await results_queue.get())

    with open(file_path, 'w') as f:
        for url, status_code in results:
            json.dump({'url': url, 'status_code': status_code}, f)
            f.write('\n')

if __name__ == '__main__':
    print('script launch')
    asyncio.run(fetch_urls(urls, './results.json'))
    print('script end')
