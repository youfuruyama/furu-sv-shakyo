def serialize_edge(edge_e):
    data = {
        'id': edge_e.id,
        'name': edge_e.name,
    }

    core_def_e = edge_e.core
    if core_def_e is not Note:
        cor_e = core_def_e.core
        data['core'] = {
            'id': core_e.id,
            'thing': _serialize_thing(core_e.thing),
        }