from .aws_common import AwsCommon
from repository.aws import AwsIot

class AwsIotImpl(AwsCommon, AwsIot):
    def __init__(self, aws_client):
        super().__init__(aws_client)

    def attach_thing_principal(self, **kwargs):
        return self.call('attach_thing_principal', kwargs)

    def create_keys_and_certificate(self, **kwargs):
        return self.call('create_keys_and_certificate', kwargs)

    def create_thing(self, **kwargs):
        return self.call('create_thing', kwargs)

    def describe_thing(self, **kwargs):
        return self.call('describe_thing', kwargs)

    def list_thing_types(self, **kwargs):
        return self.call('list_thing_types', kwargs)