import redis
import json

class RedisQueue:
    def __init__(self, host='localhost', port=6380, db=0, queue_name='my_queue'):
        self.redis = redis.Redis(host=host, port=port, db=db)
        self.queue_name = queue_name

    def publish(self, msg: dict):
        self.redis.rpush(self.queue_name, json.dumps(msg))

    def consume(self) -> dict:
        msg = self.redis.lpop(self.queue_name)
        if msg is None:
            return None
        return json.loads(msg)

if __name__ == '__main__':
    q = RedisQueue()
    q.publish({'a': 1})
    q.publish({'b': 2})
    q.publish({'c': 3})

    print("Опубликованные сообщения:")
    print(q.consume())  # {'a': 1}
    print(q.consume())  # {'b': 2}
    print(q.consume())  # {'c': 3}

# redis-server --port 6380
# python main.py
