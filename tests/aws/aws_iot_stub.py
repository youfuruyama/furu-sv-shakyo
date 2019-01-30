import entity
from repository.aws import AwsIot

class AwsIotStub(AwsIot):
    def __init__(self):
        self.things = {}
        self.thing_id = 0
        self.cert_id = 0

    def attach_thing_principal(self, **kwargs):
        if kwargs['thingName'] not in self.things:
            raise entity.NotFound('attach_thing_principal')

    def create_keys_and_certificate(self, **kwargs):
        self.cert_id += 1

        return {
            'certificateArn': f'arn:iot:cert/{self.cert_id}',
        }

    def create_thing(self, **kwargs):
        thing_name = kwargs['thingName']
        thing_arn = f'arn:iot:thing/{thing_name}'

        self.thing_id += 1
        thing_id = '33333333-3333-3333-3333-{:012x}'.format(self.thing_id)

        self.things[thing_name] = thing = {
            'thingId': thing_id,
            'thingArn': thing_arn,
            'thingName': thing_name,
            'attributes': kwargs['attributePayload']['attributes'],
        }

        v = kwargs.get('thingTypeName')
        if v:
            thing['thingTypeName'] = v

        return {
            'thingName': thing_name,
            'thingArn': thing_arn,
            'thingId': thing_id,
        }

    def describe_thing(self, **kwargs):
        thing = self.things.get(kwargs['thingName'])
        if thing is None:
            raise entity.NotFound('describe_thing')
        return thing

    def list_thing_types(self, **kwargs):
        return {
            'thingTypes': [
                {
                    'thingTypeName': 'thing-type-001',
                },
            ],
        }