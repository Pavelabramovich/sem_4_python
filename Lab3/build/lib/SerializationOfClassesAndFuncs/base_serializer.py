from abc import ABC, abstractmethod


class BaseSerializer(ABC):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)

        return cls.instance

    @abstractmethod
    def dumps(self, obj) -> str:
        pass

    @abstractmethod
    def loads(self, string: str):
        pass

    def dump(self, obj, file):
        file.write(self.dumps(obj))

    def load(self, file):
        return self.loads(file.read())


