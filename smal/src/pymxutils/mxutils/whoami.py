# Copyright (C) 2026 saces@c-base.org
# SPDX-License-Identifier: AGPL-3.0-only
import json

import click
from _pygomx import ffi, lib


@click.command()
@click.option("-u", "--url", "hs_url", metavar="url", help="homeserver url")
@click.option("-t", "--token", "token", metavar="token", help="access token")
def whoami(hs_url, token):
    """this token belongs to?"""

    if hs_url is None and token is None:
        r = lib.cliv0_mxpassitem(b".mxpass", b"*", b"*", b"*")

        result = ffi.string(r).decode("utf-8")
        lib.FreeCString(r)

        result_dict = json.loads(result)
        hs_url = result_dict["Matrixhost"]
        token = result_dict["Token"]

    r = lib.cliv0_whoami(
        hs_url.encode(encoding="utf-8"), token.encode(encoding="utf-8")
    )
    result = ffi.string(r)
    lib.FreeCString(r)
    print(result.decode("utf-8"))
