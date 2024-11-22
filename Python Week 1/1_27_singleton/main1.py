class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Singleton(metaclass=SingletonMeta):
    def some_method(self):
        return "This is a singleton method."

singleton1 = Singleton()
singleton2 = Singleton()

print(singleton1 is singleton2)
