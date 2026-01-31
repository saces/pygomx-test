import sys
import os
import getpass
import json
from _pygomx import lib, ffi


def smalsetup():
    if len(sys.argv) != 2:
        print("usage: ", sys.argv[0], " matrixid")
        return 1

    mxid = sys.argv[1].encode(encoding="utf-8")

    r = lib.apiv0_discover(mxid)
    result = ffi.string(r).decode("utf-8")
    lib.FreeCString(r)

    if result.startswith("ERR:"):
        print(result)
        return 1

    result_dict = json.loads(result)
    result_dict["password"] = getpass.getpass(prompt="Password: ")
    data = json.dumps(result_dict).encode(encoding="utf-8")

    r = lib.apiv0_login(data)
    result = ffi.string(r).decode("utf-8")
    lib.FreeCString(r)

    if result.startswith("ERR:"):
        print(result)
        return 1

    # Set restrictive umask (owner only)
    new_umask = 0o077
    old_umask = os.umask(new_umask)

    # Create file with new umask
    with open(".mxpass", "w") as f:
        f.write(result)

    # Restore original umask
    os.umask(old_umask)

    print("login created. start your bot now.")
    return 0
