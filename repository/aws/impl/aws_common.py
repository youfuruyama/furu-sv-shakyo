import botocore.exceptions as boto_exc

import entity

class AwsCommon:
    def __init__(self, aws_client):
        self.__client = aws_client

    def call(self, method, kwargs):
        try:
            return getattr(self.__client, method)(**kwargs)
        except boto_exc.ClientError as exc:
            code = exc.response.get('Error', {}).get('Code', '')
            if code.endswith('NotFoundException'):
                raise entity.NotFound from exc
            else:
                raise