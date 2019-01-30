import uuid

from service.uuid import Uuid

class uidImpl(Uuid):
    def uuid4(self):
        return str(uuid.uuid4())