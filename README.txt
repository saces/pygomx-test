monorepos to have the right versions together

libmxclient - golang matrix client library
pygomx - python binding
smal - python matrix lib
echobot - simple bot


docker compose build
docker compose run --rm dev /bin/bash


pip install -e .
discoverhs <mxid>


---
screenshot:
~/p/m/pygomx (main|✚4) $ docker compose run --rm dev /bin/bash
Container pygomx-dev-run-401f3ed5da9c Creating 
Container pygomx-dev-run-401f3ed5da9c Created 
root@7c2a56098d3c:/smal# pip install -e .
Obtaining file:///smal
  Installing build dependencies ... done
  Checking if build backend supports build_editable ... done
  Getting requirements to build editable ... done
  Preparing editable metadata (pyproject.toml) ... done
Building wheels for collected packages: smal
  Building editable for smal (pyproject.toml) ... done
  Created wheel for smal: filename=smal-0.0.1-0.editable-py3-none-any.whl size=3038 sha256=11291c3389b4044f1f12f47c2b3885f58139c5665279cab81f3a7488e5a84aeb
  Stored in directory: /tmp/pip-ephem-wheel-cache-v8951o8c/wheels/1f/23/eb/fa46f9ff6c1c46feaa27e5ffad7cb966e7aee46d5794e2d15f
Successfully built smal
Installing collected packages: smal
Successfully installed smal-0.0.1
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
root@7c2a56098d3c:/smal# discoverhs @saces:matrix.org
try to discover mxid:  b'@saces:matrix.org'
Attempt to discover 'matrix.org'
b'{"m.homeserver":{"base_url":"https://matrix-client.matrix.org"},"m.identity_server":{"base_url":"https://vector.im"}}'
root@7c2a56098d3c:/smal#
