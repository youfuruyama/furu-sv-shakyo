import collections
import logging

import entity

_log = logging.getLogger(__name__)

class EdgeService:
    # モノの属性の個数の最大値（タイプありの場合）
    MAX_ATTRIBUTES_FOR_TYPED_THING = 50
    # モノの属性の個数の最大値（タイプなしの場合）
    MAX_ATTRIBUTES_FOR_NON_TYPED_THING = 3

    def __init__(self, aws_clients, uuid_svc):
        self.greengrass = aws_clients['greengrass']
        self.iot = aws_clients['iot']
        self.uuid = uuid_svc

    def list_edges(self):
        # グループの一覧を取得する
        groups = self.greengrass.list_groups().get('Groups', ())

        return [entity.Edge(
            id=x.get('Id', ''),
            name=x.get('Name', ''),
            core=None,
            device=None,
        ) for x in groups]

    def get_edge(self, edge_id):
        # グループを取得する
        group = self.greengrass.get_group(GroupId=edge_id)

        # 最新のグループバージョンのARNから、グループバージョンIDを抽出する
        group_ver_id = self._extract_last_token(
            group.get('LatestVersionArn', ''))

        # グループバージョンを取得する
        group_ver = self.greengrass.get_group_version(GroupId=edge_id,
            GroupVersionId=group_ver_id)

        group_def = group_ver.get('Definition', {})

        # コア定義とコア、それに紐付くモノを取得する
        core_def_e = self._get_core(
            group_def.get('CoreDefinitionVersionArn', ''))

        # デバイス定義とデバイス、それに紐付くモノを取得する
        dev_ver_arn = group_def.get('DeviceDefinitionVersionArn')
        if dev_ver_arn is not None:
            dev_def_e = self._get_device(dev_ver_arn)

        return entity.Edge(
            id=edge_id,
            name=group.get('Name', ''),
            core=core_def_e,
            device=dev_def_e,
        )

    def create_edge(self, edge_e):
        # デバイスに紐付くモノを集める
        dev_def_e = edge_e.device
        things_e = ([x.thing for x in dev_def_e.devices]
            if dev_def_e is not None else [])

        # コアに紐付くモノを集める
        core_def_e = edge_e.core
        things_e.append(core_def_e.core.thing)

        # 作成しようとしているモノを事前検証する
        self._validate_things(things_e)

        # コア定義とコア、それに紐付くモノを作成する
        core_def_e = self._create_core(core_def_e)

        initial_version = {
            'CoreDefinitionVersionArn': core_def_e.version_arn,
        }

        if dev_def_e is not None:
            # デバイス定義とデバイス、それに紐付くモノを作成する
            dev_def_e = self._create_device(dev_def_e)

            initial_version['DeviceDefinitionVersionArn'] = (
                dev_def_e.version_arn)

        # グループを作成する
        resp = self.greengrass.create_group(Name=edge_e.name,
            InitialVersion=initial_version)

        return edge_e._replace(
            id=resp.get('Id', ''),
            core=core_def_e,
            device=dev_def_e,
        )

    @staticmethod
    def _extract_last_token(s):
        tokens = s.rsplit('/', 1)
        if len(tokens) != 2:
            raise entity.NotFound('No tokens found')
        return tokens[1]

    @staticmethod
    def _extract_version_arn(s):
        tokens = s.rsplit('/', 3)
        if len(tokens) != 4 or tokens[2] != 'versions':
            raise entity.NotFound('Invalid ARN format')
        return (tokens[1], tokens[3])

    def _get_core(self, ver_arn):
        # コア定義バージョンのARNから、
        # コア定義IDとコア定義バージョンIDを抽出する
        def_id, ver_id = self._extract_version_arn(ver_arn)

        # コア定義バージョンを取得する
        core_ver = self.greengrass.get_core_definition_version(
            CoreDefinitionId=def_id, CoreDefinitionVersionId=ver_id)

        # コアは配列だが、最初の要素のみを参照する
        cores = core_ver.get('Definition', {}).get('Cores', ())
        if len(cores) == 0:
            raise entity.NotFound('Missing core')
        core = cores[0]

        # コアに紐付くモノのARNから、モノの名前を抽出する
        thing_name = self._extract_last_token(core.get('ThingArn', ''))

        # コアに紐付くモノを取得する
        thing_e = self._get_thing(thing_name)

        core_e = entity.Core(
            id=core.get('Id', ''),
            thing=thing_e,
        )

        return entity.CoreDefinition(
            id=def_id,
            version_arn=ver_arn,
            core=core_e,
        )

    def _get_device(self, ver_arn):
        # デバイス定義バージョンのARNから、
        # デバイス定義IDとデバイス定義バージョンIDを抽出する
        def_id, ver_id = self._extract_version_arn(ver_arn)

        # デバイス定義バージョンを取得する
        dev_ver = self.greengrass.get_device_definition_version(
            DeviceDefinitionId=def_id, DeviceDefinitionVersionId=ver_id)

        devices_e = []
        devices = dev_ver.get('Definition', {}).get('Devices', ())
        for dev in devices:
            # デバイスに紐付くモノのARNから、モノの名前を抽出する
            thing_name = self._extract_last_token(dev.get('ThingArn', ''))

            # デバイスに紐付くモノを取得する
            thing_e = self._get_thing(thing_name)

            devices_e.append(entity.Device(
                id=dev.get('Id', ''),
                thing=thing_e,
            ))

        return entity.DeviceDefinition(
            id=def_id,
            version_arn=ver_arn,
            devices=devices_e,
        )

    def _get_thing(self, thing_name):
        thing = self.iot.describe_thing(thingName=thing_name)

        return entity.Thing(
            id=thing.get('thingId', ''),
            arn=thing.get('thingArn', ''),
            name=thing_name,
            type=thing.get('thingTypeName', ''),
            attributes=thing.get('attributes', {}),
        )

    def _validate_things(self, things_e):
        # モノの名前が重複していないことを確認する
        thing_names = collections.Counter(map(lambda x: x.name, things_e))
        for name, count in thing_names.items():
            # 同一の名前を持つモノの存在を判定する
            try:
                self._get_thing(name)
            except entity.NotFound:
                pass
            else:
                count += 1

            if count != 1:
                raise entity.ValidationError(
                    f'The thing "{name}" already exists.')

        # モノのタイプの一覧を取得する
        thing_types = self.iot.list_thing_types()

        # モノのタイプの名前の集合を作る
        type_names = { x.get('thingTypeName')
            for x in thing_types.get('thingTypes', ()) }

        for thing_e in things_e:
            # モノのタイプの存在を確認する
            type_name = thing_e.type
            if type_name and type_name not in type_names:
                raise entity.ValidationError(
                    f'The type "{type_name}" of the thing "{thing_e.name}" is not registered.')

            # モノの属性の個数が上限を超えていないことを確認する
            limit = (self.MAX_ATTRIBUTES_FOR_TYPED_THING if thing_e.type else
                self.MAX_ATTRIBUTES_FOR_NON_TYPED_THING)
            if len(thing_e.attributes) > limit:
                raise entity.ValidationError(
                    f'The number of attributes in the thing "{thing_e.name}" exceeds {limit}.')

    def _create_core(self, core_def_e):
        # コアに紐付くモノの証明書を作成する
        cert_arn = self._create_thing_certificate()

        # コアに紐付くモノを作成し、それにプリンシパルをアタッチする
        core_e = core_def_e.core
        thing_e = self._create_thing(core_e.thing, cert_arn)

        # コアIDを生成する
        core_id = self.uuid.uuid4()

        # コア定義を作成する
        resp = self.greengrass.create_core_definition(
            InitialVersion={
                'Cores': [
                    {
                        'CertificateArn': cert_arn,
                        'Id': core_id,
                        'ThingArn': thing_e.arn,
                    },
                ],
            },
        )

        core_e = core_e._replace(
            id=core_id,
            thing=thing_e,
        )

        return core_def_e._replace(
            id=resp.get('Id', ''),
            version_arn=resp.get('LatestVersionArn', ''),
            core=core_e,
        )

    def _create_device(self, dev_def_e):
        devices = []
        devices_e = []
        for dev_e in dev_def_e.devices:
            # デバイスに紐付くモノの証明書を作成する
            cert_arn = self._create_thing_certificate()

            # デバイスに紐付くモノを作成し、それにプリンシパルをアタッチする
            thing_e = self._create_thing(dev_e.thing, cert_arn)

            # デバイスIDを生成する
            dev_id = self.uuid.uuid4()

            devices.append({
                'CertificateArn': cert_arn,
                'Id': dev_id,
                'ThingArn': thing_e.arn,
            })

            devices_e.append(dev_e._replace(
                id=dev_id,
                thing=thing_e,
            ))

        # デバイス定義を作成する
        resp = self.greengrass.create_device_definition(
            InitialVersion={
                'Devices': devices,
            },
        )

        return dev_def_e._replace(
            id=resp.get('Id', ''),
            version_arn=resp.get('LatestVersionArn', ''),
            devices=devices_e,
        )

    def _create_thing_certificate(self, active=True):
        # モノの証明書と鍵ペアを作成する
        cert = self.iot.create_keys_and_certificate(setAsActive=active)

        # [TODO] 証明書と鍵ペアを保管する
        _log.info('Certificate created: %s', cert)

        return cert.get('certificateArn', '')

    def _create_thing(self, thing_e, cert_arn):
        kwargs = {
            'thingName': thing_e.name,
            'attributePayload': {
                'attributes': thing_e.attributes,
            },
        }

        v = thing_e.type
        if v:
            kwargs['thingTypeName'] = v

        # モノを作成する
        resp = self.iot.create_thing(**kwargs)

        # モノにプリンシパルをアタッチする
        self.iot.attach_thing_principal(thingName=thing_e.name,
            principal=cert_arn)

        return thing_e._replace(
            id=resp.get('thingId', ''),
            arn=resp.get('thingArn', ''),
        )