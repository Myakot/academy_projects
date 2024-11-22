import redis
import functools

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def single(max_processing_time):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            lock_name = f"lock:{func.__name__}"
            lock_timeout = max_processing_time.total_seconds()

            if not redis_client.set(lock_name, "locked", ex=lock_timeout, nx=True):
                raise Exception(f"Функция {func.__name__} уже выполняется")

            try:
                result = func(*args, **kwargs)
            finally:
                redis_client.delete(lock_name)

            return result
        return wrapper
    return decorator
