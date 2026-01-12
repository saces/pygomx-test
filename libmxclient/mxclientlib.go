package main

import (
	"mxclientlib/mxclient"
)

import "C"

//export discoverhs
func discoverhs(id *C.char) *C.char {
	mxid := C.GoString(id)
	result := mxclient.DiscoverHS(mxid)
	return C.CString(result)
}

//export hello
func hello(name *C.char) *C.char {
	goName := C.GoString(name)
	result := "Hello " + goName
	return C.CString(result)
}

func main() {}
