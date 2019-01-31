from abc import ABC, abstractmethod

class Awslot(ABC):
    @abstractmethod
    def attach_thing_principal(self, **kwargs):
        pass

    @abstractmethod
    def create_keys_and_certificate(self, **kwargs):
        pass

    @abstractmethod
    def create_thing(self, **kwargs):
        pass

    @abstractmethod
    def describe_thing(self, **kwargs):
        pass

    @abstractmethod
    def list_thing_types(self, **kwargs):
        pass