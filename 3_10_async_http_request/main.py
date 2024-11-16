import aiohttp
import asyncio
import json
import time


urls = [
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url"
]

async def fetch_url(session, url):
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


async def result_writer(result_queue, file_path):
    with open(file_path, 'w') as f:
        while True:
            result, execution_time = await result_queue.get()
            if result is None:
                break
            json.dump({'url': result[0], 'status_code': result[1], 'execution_time': execution_time}, f)
            f.write('\n')
            result_queue.task_done()


async def fetch_urls(urls, file_path):
    queue = asyncio.Queue()
    result_queue = asyncio.Queue()

    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(5):
            task = asyncio.create_task(worker(queue, session, result_queue))
            tasks.append(task)

        result_writer_task = asyncio.create_task(result_writer(result_queue, file_path))

        for url in urls:
            await queue.put(url)

        await queue.join()

        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

        await result_queue.put((None, None))
        await result_writer_task

if __name__ == '__main__':
    print('script launch')
    start_time = time.time()
    asyncio.run(fetch_urls(urls, './results.json'))
    end_time = time.time()
    print(f'''{'----'*7}\nscript finished in {end_time - start_time:.2f}\n{'----'*7}''')
    print('script end')
