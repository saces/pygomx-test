# -*- coding: utf-8 -*-
import logging
from _pygomx import lib, ffi
import json
from .errors import APIError

logger = logging.getLogger(__name__)


class _MXClient:
    """
    core binding
    """

    def __init__(self):
        super().__init__()
        self._createMXClient()

    def _createMXClient(self):
        r = lib.apiv0_createclient_pass(b".mxpass", b".", b"*", b"*", b"*")

        result = ffi.string(r)
        lib.FreeCString(r)
        if result.startswith(b"ERR:"):
            raise APIError(result)

        result_dict = json.loads(result)
        self.client_id = result_dict["id"]

    def SetOnEventHandler(self, fn):
        r = lib.apiv0_set_on_event_handler(self.client_id, fn)
        result = ffi.string(r)
        lib.FreeCString(r)
        if result.startswith(b"ERR:"):
            raise APIError(result)

    def SetOnMessageHandler(self, fn):
        r = lib.apiv0_set_on_message_handler(self.client_id, fn)
        result = ffi.string(r)
        lib.FreeCString(r)
        if result.startswith(b"ERR:"):
            raise APIError(result)

    def _sync(self):
        r = lib.apiv0_startclient(self.client_id)
        result = ffi.string(r)
        lib.FreeCString(r)
        # if result.startswith(b"ERR:"):
        #    raise APIError(result)
        print("_sync: ", result)

    def _stopsync(self):
        r = lib.apiv0_stopclient(self.client_id)
        result = ffi.string(r)
        lib.FreeCString(r)
        # if result.startswith(b"ERR:"):
        #    raise APIError(result)
        print("_stopsync: ", result)

    def _sendmessage(self, data_dict):
        data = json.dumps(data_dict).encode(encoding="utf-8")
        r = lib.apiv0_sendmessage(self.client_id, data)
        result = ffi.string(r)
        lib.FreeCString(r)
        # if result.startswith(b"ERR:"):
        #    raise APIError(result)
        print("_sendmessage: ", result)
