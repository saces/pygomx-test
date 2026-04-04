# Copyright (C) 2026 saces@c-base.org
# SPDX-License-Identifier: AGPL-3.0-only
import click
import json
from _pygomx import lib, ffi


@click.group()
@click.option("-u", "--url", "hs_url", metavar="url", help="homeserver url")
@click.option("-t", "--token", "token", metavar="token", help="access token")
def clearaccount(hs_url, token):
    """remove various things from account"""
    global _hs_url
    global _token
    if hs_url is None and token is None:
        r = lib.cliv0_mxpassitem(b".mxpass", b"*", b"*", b"*")

        result = ffi.string(r).decode("utf-8")
        lib.FreeCString(r)

        result_dict = json.loads(result)
        _hs_url = result_dict["Matrixhost"]
        _token = result_dict["Token"]
    else:
        _hs_url = hs_url
        _token = token

    r = lib.cliv0_accountinfo(
        _hs_url.encode(encoding="utf-8"), _token.encode(encoding="utf-8")
    )

    result = ffi.string(r)
    lib.FreeCString(r)
    print(result.decode("utf-8"))

    # r = lib.cliv0_clearaccount(hs_url, token)
    # result = ffi.string(r)
    # lib.FreeCString(r)
    # print(result)


@clearaccount.group()
def logout(ctx):
    """Logout devices"""
    pass


@logout.command("others")
def logout_others():
    """Logout all other devices"""
    pass


@logout.command("all")
def logout_all():
    """Logout all devices"""
    pass


@logout.command("self")
def logout_self():
    """Logout this device"""
    pass


@clearaccount.command()
def sub1():
    """sub1"""
    pass


@clearaccount.command()
def sub2():
    """sub2"""
    pass
