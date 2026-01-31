# -*- coding: utf-8 -*-
import logging
import sys
from typing import Optional

from .app import SMALApp

logger = logging.getLogger(__name__)

"""

"""


class SMALBot(SMALApp):
    """ """

    def __init__(self, sigil: String):
        super().__init__()
        self._sigil = sigil

    def run(self):
        self._sync()

    def stop(self):
        self._stopsync()

    def sendmessage(self, roomid, text):
        data = {}
        data["roomid"] = roomid
        data["content"] = {}
        data["content"]["body"] = text

        self._sendmessage(data)
