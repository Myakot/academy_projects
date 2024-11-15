import aiohttp
import asyncio
import json
import time

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
                print(f"Fetched {url} with code {response.status}")
                return url, response.status
        except aiohttp.ClientError as e:
            print(f"Error {url}: {e}")
            return url, 0

async def worker(queue, session, result_queue):
    worker_id = id(asyncio.current_task())
    print(f"Worker {worker_id} start")
    while True:
        url = await queue.get()
        print(f"Worker {worker_id} fetching url: {url}")
        start_t = time.time()
        result = await fetch_url(session, url)
        end_t = time.time()
        execution_time = end_t - start_t
        print(f"Worker {worker_id} finished fetching url: {url} in {execution_time}")
        await result_queue.put((result, execution_time))
        queue.task_done()

async def fetch_urls(urls, file_path):
    queue = asyncio.Queue()
    result_queue = asyncio.Queue()

    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(5):
            task = asyncio.create_task(worker(queue, session, result_queue))
            tasks.append(task)

        for url in urls:
            await queue.put(url)

        await queue.join()

        results = []
        while not result_queue.empty():
            result, execution_time = await result_queue.get()
            results.append((result, execution_time))

    with open(file_path, 'w') as f:
        for (url, status_code), execution_time in results:
            json.dump({'url': url, 'status_code': status_code, 'execution_time': execution_time}, f)
            f.write('\n')

    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)

if __name__ == '__main__':
    print('script launch')
    start_time = time.time()
    asyncio.run(fetch_urls(urls, './results.json'))
    end_time = time.time()
    print(f'''{'----'*7}\nscript finished in {end_time - start_time:.2f}\n{'----'*7}''')
    print('script end')
