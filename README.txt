monorepos to have the right versions together

libmxclient - golang matrix client library
pygomx - python binding
smal - python matrix lib
echobot - simple bot


docker compose build
docker compose run --rm dev /bin/bash


pip install -e .
mxdiscover <mxid>


---
screenshot:
~/p/m/pygomx (main|✚1) $ docker compose run --rm dev /bin/bash
root@7c2a56098d3c:/smal#
Container pygomx-dev-run-121767d34a7a Creating
Container pygomx-dev-run-121767d34a7a Created
root@b2f35adb64b0:/smal# pip install -e .
Obtaining file:///smal
  Installing build dependencies ... done
  Checking if build backend supports build_editable ... done
  Getting requirements to build editable ... done
  Preparing editable metadata (pyproject.toml) ... done
Building wheels for collected packages: smal
  Building editable for smal (pyproject.toml) ... done
  Created wheel for smal: filename=smal-0.0.1-0.editable-py3-none-any.whl size=3096 sha256=9291e8de463dc781d713da5751bd16422769ba30c47760c7b5f27361a3752e77
  Stored in directory: /tmp/pip-ephem-wheel-cache-qjjjkcin/wheels/1f/23/eb/fa46f9ff6c1c46feaa27e5ffad7cb966e7aee46d5794e2d15f
Successfully built smal
Installing collected packages: smal
Successfully installed smal-0.0.1
root@b2f35adb64b0:/smal# mxdiscover matrix.org
try to discover from:  b'matrix.org'
Attempt to discover 'matrix.org'
b'{"m.homeserver":{"base_url":"https://matrix-client.matrix.org"},"m.identity_server":{"base_url":"https://vector.im"}}'
root@b2f35adb64b0:/smal#
