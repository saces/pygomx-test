# Copyright (C) 2026 saces@c-base.org
# SPDX-License-Identifier: AGPL-3.0-only
from _pygomx import lib, ffi
import click
import json


@click.command()
@click.option(
    "-s", "--secret", "show_secret", is_flag=True, help="print only the secret"
)
@click.option("-u", "--url", "hs_url", metavar="url", help="url selector")
@click.option(
    "-l", "--localpart", "localpart", metavar="localpart", help="localpart selector"
)
@click.option("-d", "--domain", "domain", metavar="domain", help="domain selector")
@click.argument("mxpassfile", metavar="mxpassfilepath", required=False)
def passitem(mxpassfile, show_secret, hs_url, localpart, domain):
    """utility to get items from mxpasss files"""

    # defaults
    if mxpassfile is None:
        mxpassfile = ".mxpass"
    if hs_url is None:
        hs_url = "*"
    if localpart is None:
        localpart = "*"
    if domain is None:
        domain = "*"

    r = lib.cliv0_mxpassitem(
        mxpassfile.encode(encoding="utf-8"),
        hs_url.encode(encoding="utf-8"),
        localpart.encode(encoding="utf-8"),
        domain.encode(encoding="utf-8"),
    )
    result = ffi.string(r).decode("utf-8")
    lib.FreeCString(r)

    result_dict = json.loads(result)

    if show_secret:
        print(result_dict["Token"])
    else:
        result_dict["Token"] = "***"
        print(json.dumps(result_dict))
