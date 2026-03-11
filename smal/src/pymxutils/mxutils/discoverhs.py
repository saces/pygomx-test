# Copyright (C) 2026 saces@c-base.org
# SPDX-License-Identifier: AGPL-3.0-only
import sys
from _pygomx import lib, ffi
import click
import json


@click.command()
@click.argument("domain", metavar="string")
def discoverhs(domain):
    """Attempts to discover the homeserver from the given string"""
    mxid = domain.encode(encoding="utf-8")

    r = lib.cli_discoverhs(mxid)
    result = ffi.string(r).decode("utf-8")
    lib.FreeCString(r)
    if result.startswith("ERR:"):
        print(result)
        sys.exit(1)
    result_dict = json.loads(result)
    print(result_dict["m.homeserver"]["base_url"])
