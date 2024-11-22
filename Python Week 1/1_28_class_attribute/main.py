import datetime

class MetaCreatedAt(type):
    def __new__(cls, name, bases, attrs):
        attrs['created_at'] = datetime.datetime.now()
        return super().__new__(cls, name, bases, attrs)

class MyClass(metaclass=MetaCreatedAt):
    pass

print(MyClass().created_at)
