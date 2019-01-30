import entity
from repository.aws import AwsGreengrass

class AwsGreengrassStub(AwsGreengrass):
    def __init__(self):
        self.groups = {}
        self.group_versions = {}
        self.core_versions = {}
        self.device_versions = {}
        self.group_id = 0
        self.group_ver_id = 0
        self.core_def_id = 0
        self.core_ver_id = 0
        self.dev_def_id = 0
        self.dev_ver_id = 0

    def create_core_definition(self, **kwargs):
        self.core_def_id += 1
        def_id = 'cccccccc-cccc-cccc-cccc-{:012x}'.format(self.core_def_id)
        def_arn = f'arn:greengrass:/greengrass/definition/cores/{def_id}'

        self.core_ver_id += 1
        ver_id = 'cccccccc-7777-7777-7777-{:012x}'.format(self.core_ver_id)
        ver_arn = f'{def_arn}/versions/{ver_id}'

        self.core_versions[def_id + ':' + ver_id] = {
            'Arn': ver_arn,
            'Definition': kwargs['InitialVersion'],
            'Id': def_id,
            'Version': ver_id,
        }

        return {
            'Arn': def_arn,
            'Id': def_id,
            'LatestVersion': ver_id,
            'LatestVersionArn': ver_arn,
        }

    def create_device_definition(self, **kwargs):
        self.dev_def_id += 1
        def_id = 'dddddddd-dddd-dddd-dddd-{:012x}'.format(self.dev_def_id)
        def_arn = f'arn:greengrass:/greengrass/definition/devices/{def_id}'

        self.dev_ver_id += 1
        ver_id = 'dddddddd-7777-7777-7777-{:012x}'.format(self.dev_ver_id)
        ver_arn = f'{def_arn}/versions/{ver_id}'

        self.device_versions[def_id + ':' + ver_id] = {
            'Arn': ver_arn,
            'Definition': kwargs['InitialVersion'],
            'Id': def_id,
            'Version': ver_id,
        }

        return {
            'Arn': def_arn,
            'Id': def_id,
            'LatestVersion': ver_id,
            'LatestVersionArn': ver_arn,
        }

    def create_group(self, **kwargs):
        self.group_id += 1
        group_id = 'eeeeeeee-eeee-eeee-eeee-{:012x}'.format(self.group_id)
        group_arn = f'arn:greengrass:/greengrass/groups/{group_id}'

        self.group_ver_id += 1
        ver_id = 'eeeeeeee-7777-7777-7777-{:012x}'.format(self.group_ver_id)
        ver_arn = f'{group_arn}/versions/{ver_id}'

        self.groups[group_id] = group = {
            'Arn': group_arn,
            'Id': group_id,
            'LatestVersion': ver_id,
            'LatestVersionArn': ver_arn,
        }

        v = kwargs.get('Name')
        if v:
            group['Name'] = v

        self.group_versions[group_id + ':' + ver_id] = {
            'Arn': ver_arn,
            'Definition': kwargs['InitialVersion'],
            'Id': group_id,
            'Version': ver_id,
        }

        return group

    def get_core_definition_version(self, **kwargs):
        core_ver = self.core_versions.get(kwargs['CoreDefinitionId'] + ':' +
            kwargs['CoreDefinitionVersionId'])
        if core_ver is None:
            raise entity.NotFound('get_core_definition_version')
        return core_ver

    def get_device_definition_version(self, **kwargs):
        dev_ver = self.device_versions.get(kwargs['DeviceDefinitionId'] + ':' +
            kwargs['DeviceDefinitionVersionId'])
        if dev_ver is None:
            raise entity.NotFound('get_device_definition_version')
        return dev_ver

    def get_group(self, **kwargs):
        group = self.groups.get(kwargs['GroupId'])
        if group is None:
            raise entity.NotFound('get_group')
        return group

    def get_group_version(self, **kwargs):
        group_ver = self.group_versions.get(kwargs['GroupId'] + ':' +
            kwargs['GroupVersionId'])
        if group_ver is None:
            raise entity.NotFound('get_group_version')
        return group_ver

    def list_groups(self, **kwargs):
        return {
            'Groups': list(self.groups.values()),
        }