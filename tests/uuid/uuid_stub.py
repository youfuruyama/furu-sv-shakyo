from service.uuid import Uuid

class UuidStub(Uuid):
    def __init__(self):
        self.id = 0

    def uuid4(self):
        self.id += 1
        return '00000000-0000-0000-0000-{:012x}'.format(self.id)