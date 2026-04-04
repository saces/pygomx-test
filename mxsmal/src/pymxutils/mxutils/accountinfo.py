# Copyright (C) 2026 saces@c-base.org
# SPDX-License-Identifier: AGPL-3.0-only
import click
import json
from _pygomx import lib, ffi


@click.command()
@click.option("-u", "--url", "hs_url", metavar="url", help="homeserver url")
@click.option("-t", "--token", "token", metavar="token", help="access token")
def accountinfo(hs_url, token):
    """print info about this account devices"""

    if hs_url is None and token is None:
        r = lib.cliv0_mxpassitem(b".mxpass", b"*", b"*", b"*")

        result = ffi.string(r).decode("utf-8")
        lib.FreeCString(r)

        result_dict = json.loads(result)
        hs_url = result_dict["Matrixhost"]
        token = result_dict["Token"]

    r = lib.cliv0_accountinfo(
        hs_url.encode(encoding="utf-8"), token.encode(encoding="utf-8")
    )
    result = ffi.string(r)
    lib.FreeCString(r)
    print(result.decode("utf-8"))
