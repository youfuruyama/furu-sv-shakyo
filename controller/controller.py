import responder

from . import edge_responder

def serve(port, services):
    create_server(services).run(address='0.0.0.0', port=port)

def create_server(services):
    api = responder.API(cors=True)
    edge_resouce.add_route(api, services)

    return api