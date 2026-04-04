# Copyright (C) 2026 saces@c-base.org
# SPDX-License-Identifier: AGPL-3.0-only
import sys

import click
from _pygomx import ffi, lib


@click.command()
@click.option(
    "--json", "show_json", is_flag=True, help="show json as returned from server."
)
@click.argument("domain", metavar="string")
def serverinfo(domain, show_json):
    """show server info for given server (federationstester light)"""

    mxdomain = sys.argv[1].encode(encoding="utf-8")

    r = lib.cliv0_serverinfo(mxdomain)
    result = ffi.string(r).decode("utf-8")
    lib.FreeCString(r)
    print(result)
