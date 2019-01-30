import collections

# =============================================================================
# ドメインのエラー
# =============================================================================

class NotFound(Exception):
    pass

class ValidationError(Exception):
    pass

# =============================================================================
# ドメインのオブジェクト
# =============================================================================

# エッジ
# * id ... エッジID（GreengrassグループID）
# * name ... エッジ名
# * core ... コア定義（CoreDefinition）
# * device ... デバイス定義（DeviceDefinition）。Noneも可
Edge = collections.namedtuple('Edge', 'id, name, core, device')

# コア定義
# * id ... コア定義ID
# * version_arn ... 最新のコア定義バージョンのARN
# * core ... コア（Core）
CoreDefinition = collections.namedtuple('CoreDefinition',
    'id, version_arn, core')

# コア
# * id ... コアID
# * thing ... コアに紐付くモノ（Thing）
Core = collections.namedtuple('Core', 'id, thing')

# デバイス定義
# * id ... デバイス定義ID
# * version_arn ... 最新のデバイス定義バージョンのARN
# * devices ... デバイス（Device）のリスト。空も可
DeviceDefinition = collections.namedtuple('DeviceDefinition',
    'id, version_arn, devices')

# デバイス
# * id ... デバイスID
# * thing ... デバイスに紐付くモノ（Thing）
Device = collections.namedtuple('Device', 'id, thing')

# モノ
# * id ... モノID
# * arn ... モノのARN
# * name ... モノの名前
# * type ... モノのタイプ。空文字列も可
# * attributes ... モノの属性を表す辞書。空の辞書も可。
#                  キーと値は、ともに空でない文字列
Thing = collections.namedtuple('Thing', 'id, arn, name, type, attributes')