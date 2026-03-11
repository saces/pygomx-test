# Copyright (C) 2026 saces@c-base.org
# SPDX-License-Identifier: AGPL-3.0-only
import sys
from _pygomx import lib, ffi


def serverinfo():
    if len(sys.argv) != 2:
        print("usage: ", sys.argv[0], "  url|domainname")
        return 1

    mxdomain = sys.argv[1].encode(encoding="utf-8")

    r = lib.cli_serverinfo(mxdomain)
    result = ffi.string(r)
    lib.FreeCString(r)
    print(result)
