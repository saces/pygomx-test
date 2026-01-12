package mxclient

import (
	"context"
	"encoding/json"
	"fmt"

	"maunium.net/go/mautrix"
	"maunium.net/go/mautrix/id"
)

func DiscoverHS(ids string) string {
	mxid := id.UserID(ids)

	_, hs, err := mxid.Parse()

	if err != nil {
		return fmt.Sprintf("ERR: %v", err)
	}

	fmt.Printf("Attempt to discover '%s'\n", hs)

	wk, err := mautrix.DiscoverClientAPI(context.Background(), hs)
	if err != nil {
		return fmt.Sprintf("ERR: %v", err)
	}
	if wk == nil {
		return fmt.Sprintf("No well-known. hs from input: %s", hs)
	}

	j, err := json.Marshal(wk)
	if err != nil {
		return fmt.Sprintf("ERR: %v", err)
	}
	return string(j)
}
