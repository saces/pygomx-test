// Copyright (C) 2026 saces@c-base.org
// SPDX-License-Identifier: AGPL-3.0-only
package main

import (
	"mxclientlib/mxclient"
	"unsafe"
)

/*
#include <stdlib.h>
*/
import "C"

//export FreeCString
func FreeCString(s *C.char) {
	C.free(unsafe.Pointer(s))
}

/*
cli tools
*/
//export cli_discoverhs
func cli_discoverhs(id *C.char) *C.char {
	mxid := C.GoString(id)
	result := mxclient.DiscoverHS(mxid)
	return C.CString(result)
}

//export cli_mkmxtoken
func cli_mkmxtoken(id *C.char, pw *C.char) *C.char {
	mxid := C.GoString(id)
	mxpw := C.GoString(pw)
	result := mxclient.MkToken(mxid, mxpw)
	return C.CString(result)
}

//export cli_whoami
func cli_whoami(hs *C.char, tk *C.char) *C.char {
	_hs := C.GoString(hs)
	_tk := C.GoString(tk)
	result := mxclient.Whoami(_hs, _tk)
	return C.CString(result)
}

//export cli_accountinfo
func cli_accountinfo(hs *C.char, tk *C.char) *C.char {
	_hs := C.GoString(hs)
	_tk := C.GoString(tk)
	result := mxclient.AccountInfo(_hs, _tk)
	return C.CString(result)
}

//export cli_clearaccount
func cli_clearaccount(hs *C.char, tk *C.char) *C.char {
	_hs := C.GoString(hs)
	_tk := C.GoString(tk)
	result := mxclient.ClearAccount(_hs, _tk)
	return C.CString(result)
}

//export cli_serverinfo
func cli_serverinfo(url *C.char) *C.char {
	_url := C.GoString(url)
	result := mxclient.ServerInfo(_url)
	return C.CString(result)
}

/*
high api
*/
//export createclient
func createclient(url *C.char, userID *C.char, accessToken *C.char) C.int {
	return 0
}

//export shutdown
func shutdown() C.int {
	return 0
}

func main() {}
