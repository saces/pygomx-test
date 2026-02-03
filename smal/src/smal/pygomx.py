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
        # ffi_selfhandle = ffi.new_handle(self)
        # self._ffi_selfhandle = ffi_selfhandle
        self._ffi_selfhandle = ffi.new_handle(self)
        # self._ffi_selfhandle = ffi_selfhandle

        r = lib.apiv0_set_on_event_handler(
            self.client_id, on_event_callback, self._ffi_selfhandle
        )
        result = ffi.string(r)
        lib.FreeCString(r)
        if result.startswith(b"ERR:"):
            raise APIError(result)

        r = lib.apiv0_set_on_message_handler(
            self.client_id, on_message_callback, self._ffi_selfhandle
        )
        result = ffi.string(r)
        lib.FreeCString(r)
        if result.startswith(b"ERR:"):
            raise APIError(result)

    def _createMXClient(self):
        r = lib.apiv0_createclient_pass(b".mxpass", b".", b"*", b"*", b"*")

        result = ffi.string(r)
        lib.FreeCString(r)
        if result.startswith(b"ERR:"):
            raise APIError(result)

        result_dict = json.loads(result)
        self.client_id = result_dict["id"]

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

    def process_event(self, evt):
        if hasattr(self, "on_event") and callable(self.on_event):
            self.on_event(evt)
        else:
            logger.warn(f"got event but on_event not declared: {evt}")

    def process_message(self, msg):
        if hasattr(self, "on_message") and callable(self.on_message):
            self.on_message(msg)
        else:
            logger.warn(f"got message but on_message not declared: {msg}")
            self._stopsync()


@ffi.callback("void(char*, void*)")
def on_event_callback(evt, pobj):
    cli = ffi.from_handle(pobj)
    e = ffi.string(evt).decode("utf-8")
    evt = json.loads(e)
    cli.process_event(evt)


@ffi.callback("void(char*, void*)")
def on_message_callback(msg, pobj):
    cli = ffi.from_handle(pobj)
    m = ffi.string(msg).decode("utf-8")
    msg = json.loads(m)
    cli.process_message(msg)
