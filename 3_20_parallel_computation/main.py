import random
import time
import concurrent.futures
import multiprocessing
import json

def generate_data(n):
    return [random.randint(1, 1000) for _ in range(n)]

def process_number(number):
    result = 1
    for i in range(1, number + 1):
        result *= i
    return result

def variant_a(data):
    # concurrent.futures
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(process_number, data))
    return results

def variant_b(data):
    # multiprocessing.Pool
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(process_number, data)
    return results

def variant_c(data):
    # multiprocessing.Process // multiprocessing.Queue
    def worker(queue, number):
        result = process_number(number)
        queue.put(result)

    queues = []
    processes = []
    for number in data:
        queue = multiprocessing.Queue()
        process = multiprocessing.Process(target=worker, args=(queue, number))
        processes.append(process)
        queues.append(queue)
        process.start()

    results = []
    for process, queue in zip(processes, queues):
        process.join()
        results.append(queue.get())

    return results

def variant_d(data):
    # singlethread
    results = []
    for number in data:
        results.append(process_number(number))
    return results

def main():
    n = 1000
    data = generate_data(n)

    start_time = time.time()
    results_single_thread = variant_d(data)
    end_time = time.time()
    print(f"Время выполнения однопоточного варианта: {end_time - start_time} секунд")

    start_time = time.time()
    results_variant_a = variant_a(data)
    end_time = time.time()
    print(f"Время выполнения варианта А: {end_time - start_time} секунд")

    start_time = time.time()
    results_variant_b = variant_b(data)
    end_time = time.time()
    print(f"Время выполнения варианта Б: {end_time - start_time} секунд")

    start_time = time.time()
    results_variant_c = variant_c(data)
    end_time = time.time()
    print(f"Время выполнения варианта В: {end_time - start_time} секунд")

    with open('results.json', 'w') as f:
        json.dump({
            'single_thread': results_single_thread,
            'variant_a': results_variant_a,
            'variant_b': results_variant_b,
            'variant_c': results_variant_c,
        }, f)

if __name__ == '__main__':
    main()
