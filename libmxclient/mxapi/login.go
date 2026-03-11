// Copyright (C) 2026 saces@c-base.org
// SPDX-License-Identifier: AGPL-3.0-only
package mxapi

import (
	"context"
	"crypto/sha256"
	"encoding/json"
	"fmt"
	"time"

	"maunium.net/go/mautrix"
	"maunium.net/go/mautrix/id"
)

type login_data struct {
	Homeserver string `json:"homeserver"`
	Mxid       string `json:"mxid"`
	Loginname  string `json:"loginname"`
	Password   string `json:"password"`
}

func Login(data string) (string, error) {
	var ld login_data
	err := json.Unmarshal([]byte(data), &ld)
	if err != nil {
		return "", err
	}

	mauclient, err := mautrix.NewClient(ld.Homeserver, id.UserID(ld.Mxid), "")
	if err != nil {
		return "", err
	}

	deviceName := fmt.Sprintf("smalbot-%d", time.Now().Unix())

	resp, err := mauclient.Login(context.Background(), &mautrix.ReqLogin{
		Type: "m.login.password",
		Identifier: mautrix.UserIdentifier{
			Type: "m.id.user",
			User: ld.Loginname,
		},
		Password:                 ld.Password,
		DeviceID:                 id.DeviceID(deviceName),
		InitialDeviceDisplayName: deviceName,
		StoreCredentials:         false,
		StoreHomeserverURL:       false,
		RefreshToken:             false,
	})
	if err != nil {
		return "", err
	}

	tpl := "%s | %s | %s | %s\nrecovery | | | %x\nmaster | | | %x\n"
	res := fmt.Sprintf(tpl, ld.Homeserver, ld.Loginname, id.UserID(ld.Mxid).Homeserver(), resp.AccessToken, sha256.Sum256([]byte(ld.Password)), sha256.Sum256([]byte(deviceName)))

	return res, nil
}
