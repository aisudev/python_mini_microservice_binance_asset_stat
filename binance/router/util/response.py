from typing import Optional


STATUS_MODIFIED = 202
STATUS_OK = 200
STATUS_ERR_NOTFOUND = 404
STATUS_ERR_EXIST = 455


def rpc_response(status_code: int = STATUS_OK, data: Optional[list] = None, msg: str = None) -> dict:
    result = dict(status_code=status_code, data=data)
    if data:
        result["data"] = data

    if msg:
        result["msg"] = msg

    return result
