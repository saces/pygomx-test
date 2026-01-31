//go:build windows
// +build windows

package mxpassfile

// ReadPassfile reads the file at path and parses it into a Passfile.
func ReadPassfile(path string) (*Passfile, error) {
	return readPassfile(path)
}
