import asyncio
from functools import wraps
import logging
import responder.status_codes as status_codes

import entity

_log = logging.getLogger(__name__)

async def decode_body(req):
    try:
        return await req.media()
    except Exception as exc:
        raise entity.ValidationError(str(exc))

def respond(func):
    """HTTPリクエストハンドラの共通的なデコレータ"""

    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 第3引数が、responderのResponseオブジェクト
            resp = args[2]

            try:
                result = await func(*args, **kwargs)
            except Exception as exc:
                _handle_error(resp, exc)
            else:
                _set_content(resp, result)
    else:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 第3引数が、responderのResponseオブジェクト
            resp = args[2]

            try:
                result = func(*args, **kwargs)
            except Exception as exc:
                _handle_error(resp, exc)
            else:
                _set_content(resp, result)

    return wrapper

def _handle_error(resp, exc):
    """ドメインのエラーを、HTTPのステータスコードに対応づける"""

    if isinstance(exc, entity.ValidationError):
        resp.status_code = status_codes.HTTP_400
    elif isinstance(exc, entity.NotFound):
        resp.status_code = status_codes.HTTP_404
    else:
        raise exc

    # [TODO] エラーメッセージをレスポンスボディに入れる
    _log.error('Exception caught: %s', exc)

def _set_content(resp, result):
    if isinstance(result, tuple):
        resp.status_code = result[0]
        resp.media = result[1]
    else:
        resp.status_code = result