import unittest

import controller
from service.edge import EdgeService
from . import aws as aws_stub
from .pact_player import PactPlayer
from .uuid import UuidStub

class TestPact(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_edge(self):
        aws_clients = {
            'greengrass': aws_stub.AwsGreengrassStub(),
            'lot': aws_stub.AwsIotStub(),
        }

        uuid_svc = UuidStub()
        services = {
            'uuid': uuid_svc,
            'edge': EdgeService(aws_clients, uuid_svc),
        }
        api = controller.create_server(services)
        PactPlayer('edge.json').run(self,api)