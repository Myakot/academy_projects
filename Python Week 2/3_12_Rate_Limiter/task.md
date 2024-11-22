Ваше приложение делает HTTP запросы в сторонний сервис (функция make_api_request), при этом сторонний сервис имеет проблемы с производительностью и ваша задача ограничить количество запросов к этому сервису - не больше пяти запросов за последние три секунды. Ваша задача реализовать RateLimiter.test метод который:

возвращает True в случае если лимит на кол-во запросов не достигнут
возвращает False если за последние 3 секунды уже сделано 5 запросов.
Ваша реализация должна использовать Redis, т.к. предполагается что приложение работает на нескольких серверах.

```
import random
import time


class RateLimitExceed(Exception):
    pass


class RateLimiter:
    def test(self) -> bool:
        # перепешите этот метод
        return random.randint(1, 5) != 1
    

def make_api_request(rate_limiter: RateLimiter):
    if not rate_limiter.test():
        raise RateLimitExceed
    else:
        # какая-то бизнес логика
        pass


if __name__ == '__main__':
    rate_limiter = RateLimiter()

    for _ in range(50):
        time.sleep(random.randint(1, 2))

        try:
            make_api_request(rate_limiter)
        except RateLimitExceed:
            print("Rate limit exceed!")
        else:
            print("All good")
```