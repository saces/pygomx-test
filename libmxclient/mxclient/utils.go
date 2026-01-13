// Copyright (C) 2026 saces@c-base.org
// SPDX-License-Identifier: AGPL-3.0-only
package mxclient

import (
	"context"
	"encoding/json"
	"fmt"
	"time"

	"maunium.net/go/mautrix"
	"maunium.net/go/mautrix/id"
)

func DiscoverHS(ids string) string {

	var domainname string

	// probe for mxid
	_mxid := id.UserID(ids)

	_, _hs, err := _mxid.Parse()

	if err != nil {
		// not a mxid
		domainname = ids
	} else {
		domainname = _hs
	}

	fmt.Printf("Attempt to discover '%s'\n", domainname)

	wk, err := mautrix.DiscoverClientAPI(context.Background(), domainname)
	if err != nil {
		return fmt.Sprintf("ERR: %v", err)
	}
	if wk == nil {
		return fmt.Sprintf("No well-known. hs from input: %s", domainname)
	}

	j, err := json.Marshal(wk)
	if err != nil {
		return fmt.Sprintf("ERR: %v", err)
	}
	return string(j)
}

func MkToken(ids string, pw string) string {

	mxid := id.UserID(ids)

	_, hs, err := mxid.Parse()
	if err != nil {
		return fmt.Sprintf("ERR: %v", err)
	}

	wk, err := mautrix.DiscoverClientAPI(context.Background(), hs)
	if err != nil {
		return fmt.Sprintf("ERR: %v", err)
	}

	if wk != nil {
		hs = wk.Homeserver.BaseURL
	}

	mauclient, err := mautrix.NewClient(hs, mxid, "")
	if err != nil {
		return fmt.Sprintf("ERR: %v", err)
	}

	deviceName := fmt.Sprintf("mxtokenizer-%d", time.Now().Unix())

	resp, err := mauclient.Login(context.Background(), &mautrix.ReqLogin{
		Type: "m.login.password",
		Identifier: mautrix.UserIdentifier{
			Type: "m.id.user",
			User: mxid.Localpart(),
		},
		Password:                 pw,
		DeviceID:                 id.DeviceID(deviceName),
		InitialDeviceDisplayName: deviceName,
		StoreCredentials:         false,
		StoreHomeserverURL:       false,
		RefreshToken:             false,
	})
	if err != nil {
		return fmt.Sprintf("ERR: %v", err)
	}

	return resp.AccessToken
}

func Whoami(hs string, accessToken string) string {
	return "nope. whoami"
}

func AccountInfo(hs string, accessToken string) string {
	return "nope. accountinfo"
}

func ClearAccount(hs string, accessToken string) string {
	return "nope. clearaccount"
}

func ServerInfo(url string) string {
	return "nope. serverinfo"
}
