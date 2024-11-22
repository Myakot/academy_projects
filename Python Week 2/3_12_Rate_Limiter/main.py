import redis
import time
import random
import logging

logging.basicConfig(level=logging.DEBUG)

class RateLimitExceed(Exception):
    pass


class RateLimiter:
    def __init__(self, redis_client, key, max_requests, period):
        self.redis_client = redis_client
        self.key = key
        self.max_requests = max_requests
        self.period = period

    def test(self) -> bool:
        logging.debug("Тестирование rate limiter")
        current_time = int(time.time())
        logging.debug(f"Текущее время: {current_time}")
        count = self.redis_client.zcard(self.key)
        logging.debug(f"Количество записей в Redis: {count}")
        if count >= self.max_requests:
            self.redis_client.zremrangebyscore(self.key, 0, current_time - self.period)
            logging.debug("Rate limit превышен!")
            return False
        self.redis_client.zremrangebyscore(self.key, 0, current_time - self.period)
        self.redis_client.zadd(self.key, {str(current_time): current_time})
        logging.debug("Добавление новой записи в Redis")
        return True


def make_api_request(rate_limiter: RateLimiter):
    logging.debug("Отправка API-запроса")
    if not rate_limiter.test():
        logging.debug("Rate limit превышен! Вызов исключения")
        raise RateLimitExceed
    else:
        logging.debug("Rate limit не превышен. Запрос прошел успешно")
        # здесь что-то должно происходить, наверное
        pass


if __name__ == '__main__':
    logging.debug("Запуск программы")
    redis_client = redis.Redis(host='localhost', port=6380, db=0)
    logging.debug("Подключение к Redis")
    rate_limiter = RateLimiter(redis_client, 'rate_limit', 5, 10)
    logging.debug("Создание rate limiter")

    for _ in range(50):
        logging.debug("Начало итерации")
        time.sleep(random.randint(1, 2))
        logging.debug("Ожидание случайного времени")

        try:
            make_api_request(rate_limiter)
        except RateLimitExceed:
            logging.debug("Перехват исключения RateLimitExceed")
            print("Rate limit exceed!")
        else:
            logging.debug("Запрос прошел успешно")
            print("All good")
        logging.debug("Конец итерации")
