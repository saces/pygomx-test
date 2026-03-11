# -*- coding: utf-8 -*-
from _pygomx import ffi, lib
import json


class APIError(Exception):
    """Exception raised for api usage errors.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message[4:]
        super().__init__(self.message)


def apiResult(cstr):
    result = ffi.string(cstr).decode("utf-8")
    lib.FreeCString(cstr)
    return result


def CheckApiError(cstr):
    result = apiResult(cstr)

    if result.startswith("ERR:"):
        raise APIError(result)


def CheckApiResult(cstr):
    result = apiResult(cstr)

    if result.startswith("ERR:"):
        raise APIError(result)

    if result == "SUCCESS.":
        return None

    result_dict = json.loads(result)
    return result_dict
