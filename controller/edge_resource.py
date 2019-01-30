import responder.status_codes as status_codes

from . import deserializer as des, serializer as ser
from .view import decode_body, respond

def add_route(api, services):
    edge_svc = services.get('edge')
    if edge_svc is None:
        return

    api.add_route('/api/edges', _EdgeRootView(edge_svc))
    api.add_route('/api/edges/{edge_id}', _EdgeView(edge_svc))

# -----------------------------------------------------------------------------
# ビュー
# -----------------------------------------------------------------------------

class _EdgeRootView:
    def __init__(self, edge_svc):
        self.edge_svc = edge_svc

    @respond
    def on_get(self, req, resp):
        edges_e = self.edge_svc.list_edges()
        content = [ser.serialize_edge(x) for x in edges_e]
        return (status_codes.HTTP_200, content)

    @respond
    async def on_post(self, req, resp):
        data = await decode_body(req)
        edge_e = des.deserialize_edge(data)
        new_edge_e = self.edge_svc.create_edge(edge_e)
        content = ser.serialize_edge(new_edge_e)
        return (status_codes.HTTP_201, content)

class _EdgeView:
    def __init__(self, edge_svc):
        self.edge_svc = edge_svc

    @respond
    def on_get(self, req, resp, *, edge_id):
        edge_e = self.edge_svc.get_edge(edge_id)
        content = ser.serialize_edge(edge_e)
        return (status_codes.HTTP_200, content)