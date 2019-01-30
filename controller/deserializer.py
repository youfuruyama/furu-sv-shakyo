from cerberus import schema_registry, Validator

import entity

schema_registry.extend((
    # -------------------------------------------------------------------------
    # モノ
    # -------------------------------------------------------------------------

    ('Thing', {
        'name': {
            'required': True,
            'type': 'string',
            'empty': False,
        },
        'type': {
            'type': 'string',
            'empty': False,
        },
        'attributes': {
            'required': True,
            'type': 'dict',
            'keyschema': {
                'type': 'string',
                'empty': False,
            },
            'valueschema': {
                'type': 'string',
                'empty': False,
            },
        },
    }),

    # -------------------------------------------------------------------------
    # エッジ
    # -------------------------------------------------------------------------

    ('Edge', {
        'name': {
            'required': True,
            'type': 'string',
            'empty': False,
        },
        'core': {
            'required': True,
            'type': 'dict',
            'schema': {
                'thing': {
                    'required': True,
                    'type': 'dict',
                    'schema': 'Thing',
                },
            },
        },
        'devices': {
            'required': True,
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'thing': {
                        'required': True,
                        'type': 'dict',
                        'schema': 'Thing',
                    },
                },
            },
        },
    }),
))

_edge_validator = Validator('Edge')

def _validate(v, data):
    if not v.validate(data):
        raise entity.ValidationError(str(v.errors))
    return v.document

def deserialize_edge(data):
    edge = _validate(_edge_validator, data)

    core_e = entity.Core(
        id=None,
        thing=_deserialize_thing(edge['core']['thing']),
    )

    core_def_e = entity.CoreDefinition(
        id=None,
        version_arn=None,
        core=core_e,
    )

    devices_e = [entity.Device(
        id=None,
        thing=_deserialize_thing(x['thing']),
    ) for x in edge['devices']]

    dev_def_e = entity.DeviceDefinition(
        id=None,
        version_arn=None,
        devices=devices_e,
    )

    return entity.Edge(
        id=None,
        name=edge['name'],
        core=core_def_e,
        device=dev_def_e,
    )

def _deserialize_thing(thing):
    return entity.Thing(
        id=None,
        arn=None,
        name=thing['name'],
        type=thing.get('type', ''),
        attributes=thing['attributes'],
    )