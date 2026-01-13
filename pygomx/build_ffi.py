#!/usr/bin/python
from cffi import FFI

ffibuilder = FFI()

ffibuilder.set_source(
    module_name="_pygomx",
    source=""" //passed to the real C compiler
        #include "libmxclient.h"
    """,
    libraries=["mxclient"],
)

ffibuilder.cdef(
    csource="""
    extern char* cli_discoverhs(char* mxid);
    extern char* cli_mkmxtoken(char* mxid, char* pw);
    extern char* cli_whoami(char* hs, char* accessToken);
    extern char* cli_accountinfo(char* hs, char* accessToken);
    extern char* cli_clearaccount(char* hs, char* accessToken);
    extern char* cli_serverinfo(char* url);
    extern int createclient(char* url, char* userID, char* accessToken);
    """
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
