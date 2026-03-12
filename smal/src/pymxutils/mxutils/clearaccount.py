# Copyright (C) 2026 saces@c-base.org
# SPDX-License-Identifier: AGPL-3.0-only
import sys
from _pygomx import lib, ffi


def clearaccount():
    if len(sys.argv) != 3:
        print("usage: ", sys.argv[0], " url accesstoken")
        return 1

    url = sys.argv[1].encode(encoding="utf-8")
    tk = sys.argv[2].encode(encoding="utf-8")

    r = lib.cliv0_clearaccount(url, tk)
    result = ffi.string(r)
    lib.FreeCString(r)
    print(result)
