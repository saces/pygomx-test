// Copyright (C) 2026 saces@c-base.org
// SPDX-License-Identifier: AGPL-3.0-only
package mxapi

import (
	"context"
	"encoding/json"

	"maunium.net/go/mautrix"
	"maunium.net/go/mautrix/id"
)

func Discover(mxid string) (string, error) {

	localpart, hs, err := id.UserID(mxid).ParseAndValidateRelaxed()
	if err != nil {
		return "", err
	}

	wk, err := mautrix.DiscoverClientAPI(context.Background(), hs)
	if err != nil {
		return "", err
	}
	if wk != nil {
		hs = wk.Homeserver.BaseURL
	}

	out, err := json.Marshal(map[string]string{"mxid": mxid, "homeserver": hs, "loginname": localpart})
	if err != nil {
		return "", err
	}

	return string(out), nil
}
