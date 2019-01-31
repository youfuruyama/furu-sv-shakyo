from .aws_common import AwsCommon
from repository.aws import AwsGreengrass

class AwsGreengrassImpl(AwsCommon, AwsGreengrass):
    def __init__(self, aws_client):
        super().__init__(aws_client)

    def create_core_definition(self, **kwargs):
        return self.call('create_core_definition', kwargs)

    def create_device_definition(self, **kwargs):
        return self.call('create_device_definition', kwargs)

    def create_group(self, **kwargs):
        return self.call('create_group', kwargs)

    def get_core_definition_version(self, **kwargs):
        return self.call('get_core_definition_version', kwargs)

    def get_device_definition_version(self, **kwargs):
        return self.call('get_device_definition_version', kwargs)

    def get_group(self, **kwargs):
        return self.call('get_group', kwargs)

    def get_group_version(self, **kwargs):
        return self.call('get_group_version', kwargs)

    def list_groups(self, **kwargs):
        return self.call('list_groups', kwargs)