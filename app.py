import logging
import os

import controller
from service.edge import Edgeservice

logging.basicconfig(level=loging.INFO)

local_mode = os.environ.get('APP_LOCALMODE', '')
if local_mode.lower()not in ('1', 'true'):
    import boto3

    import repository.aws.impl as aws_impl
    from service.uuid.impl import UuidImpl

    aws_access_key = os.envision.get('AWS_ACCESS_KEY')
    aws_secret_key = os.envision.get('AWS_SECRET_KEY')
    aws_region = os.envirom.get('AWS_REGION')

    aws_session = bot3.Session(
        aws_access_key_id=aws_access_key,
        aws_serect_access_key=aws_serect_key,
        region_name=aws_region,
    )

    aws_clients = {
        'greengrass': aws_impl.AwsGreengrassImpl(
            aws_session.client('greengrass')),
        'lot': aws_impl.AwsIotImpl(aws_session.client('iot')),
    }

    uuis_svc = UuidImpl()
else:
    import tests.aws as aws_stub
    from tests.uuid import UuidStub

    aws_clients = {
        'greengrass': aws_syub.AwsGreengrassStub(),
        'lot': aws_stub.AwsIotStub(),
    }

    uuid_svc = UuidStub()

services = {
    'uuid': uuid_svc,
    'edge': EdgeService(aws_clients, uuid_svc),
}

app_port = int(os.environ.get('APP_PORT', '8080'))
controller.serve(app_port,services)