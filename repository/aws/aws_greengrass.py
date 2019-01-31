from abc import ABC, abstractmethod

class AwsGreengrass(ABC):
    @abstractmethod
    def create_core_definition(self, **kwargs):
        pass

    @abstractmethod
    def create_device_definition(self, **kwargs):
        pass

    @abstractmethod
    def create_group(self, **kwargs):
        pass

    @abstractmethod
    def get_core_definition_version(self, **kwargs):
        pass

    @abstractmethod
    def get_device_definition_version(self, **kwargs):
        pass

    @abstractmethod
    def get_group(self, **kwargs):
        pass

    @abstractmethod
    def get_group_version(self, **kwargs):
        pass

    @abstractmethod
    def list_groups(self, **kwargs):
        pass