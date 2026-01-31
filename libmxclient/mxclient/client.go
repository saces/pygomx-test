// Copyright (C) 2026 saces@c-base.org
// SPDX-License-Identifier: AGPL-3.0-only
package mxclient

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"mxclientlib/determinant/mxpassfile"

	_ "github.com/mattn/go-sqlite3"
	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"
	"go.mau.fi/util/dbutil"
	_ "go.mau.fi/util/dbutil/litestream"
	"maunium.net/go/mautrix"
	"maunium.net/go/mautrix/crypto"
	"maunium.net/go/mautrix/crypto/cryptohelper"
	"maunium.net/go/mautrix/event"
	"maunium.net/go/mautrix/id"
	"maunium.net/go/mautrix/sqlstatestore"
)

type MXClient struct {
	*mautrix.Client
	OnEvent   func(string)
	OnMessage func(string)
}

func (mxc *MXClient) _onEvent(ctx context.Context, evt *event.Event) {
	if evt.GetStateKey() == mxc.UserID.String() && evt.Content.AsMember().Membership == event.MembershipInvite {
		_, err := mxc.JoinRoomByID(ctx, evt.RoomID)
		if err == nil {
			log.Info().
				Str("room_id", evt.RoomID.String()).
				Str("inviter", evt.Sender.String()).
				Msg("Joined room after invite")
		} else {
			log.Error().Err(err).
				Str("room_id", evt.RoomID.String()).
				Str("inviter", evt.Sender.String()).
				Msg("Failed to join room after invite")
		}
	} else {
		fmt.Printf("Got event: %#v\n", evt)
	}
}

func (mxc *MXClient) _onMessage(ctx context.Context, evt *event.Event) {
	out, err := json.Marshal(map[string]interface{}{"sender": evt.Sender.String(),
		"type":    evt.Type.String(),
		"id":      evt.ID.String(),
		"roomid":  evt.RoomID.String(),
		"content": evt.Content.Raw})

	if err != nil {
		log.Error().Err(err).
			Str("id", evt.ID.String()).
			Str("inviter", evt.Sender.String()).
			Msg("Marshalling error")
		return
	}
	mxc.OnMessage(string(out))

	/*
		log.Info().
			Str("sender", evt.Sender.String()).
			Str("type", evt.Type.String()).
			Str("id", evt.ID.String()).
			Str("roomid", evt.RoomID.String()).
			Str("body", evt.Content.AsMessage().Body).
			Msg("Received message")
		fmt.Printf("Got message: %#v\n", evt)
	*/
}

type sendmessage_data_content struct {
	Body string `json:"body"`
}

type sendmessage_data struct {
	RoomId  id.RoomID                `json:"roomid"`
	Type    event.Type               `json:"type"`
	Content sendmessage_data_content `json:"content"`
}

func (mxc *MXClient) SendRoomMessage(ctx context.Context, data string) (*mautrix.RespSendEvent, error) {
	var smd sendmessage_data
	err := json.Unmarshal([]byte(data), &smd)
	if err != nil {
		return nil, err
	}

	resp, err := mxc.SendMessageEvent(ctx, smd.RoomId, event.EventMessage, smd.Content)
	if err != nil {
		return nil, err
	}
	return resp, nil

}

// NewMXClient creates a new Matrix Client ready for syncing
func NewMXClient(homeserverURL string, userID id.UserID, accessToken string) (*MXClient, error) {
	client, err := mautrix.NewClient(homeserverURL, userID, accessToken)
	if err != nil {
		return nil, err
	}

	// keep this for the import
	client.Log = zerolog.Nop()
	// client.Log = zerolog.New(os.Stdout)
	// client.SyncTraceLog = true

	resp, err := client.Whoami(context.Background())
	if err != nil {
		return nil, err
	}
	client.DeviceID = resp.DeviceID

	//fmt.Printf("Device ID: %s\n", client.DeviceID)

	rawdb, err := dbutil.NewWithDialect("smalbot.db", "sqlite3")
	if err != nil {
		return nil, err
	}

	//fmt.Println("db is offen.")

	syncer, ok := client.Syncer.(*mautrix.DefaultSyncer)
	if !ok {
		return nil, errors.New("panic: syncer implementation error")
	}

	//mxclient.StateStore = mautrix.NewMemoryStateStore()

	stateStore := sqlstatestore.NewSQLStateStore(rawdb, dbutil.NoopLogger, false)
	err = stateStore.Upgrade(context.Background())
	if err != nil {
		return nil, fmt.Errorf("failed to upgrade state db: %w", err)
	}
	client.StateStore = stateStore

	pickleKey := []byte("pickle")

	//cryptoStore := crypto.NewMemoryStore(nil)
	cryptoStore := crypto.NewSQLCryptoStore(rawdb, dbutil.ZeroLogger(log.With().Str("db_section", "crypto").Logger()), "", "", pickleKey)
	err = cryptoStore.DB.Upgrade(context.Background())
	if err != nil {
		return nil, fmt.Errorf("failed to upgrade crypto db: %w", err)
	}

	client.Crypto, err = cryptohelper.NewCryptoHelper(client, pickleKey, cryptoStore)
	if err != nil {
		return nil, err
	}

	err = client.Crypto.Init(context.TODO())
	if err != nil {
		return nil, err
	}

	client.Store = cryptoStore

	mxclient := &MXClient{client, nil, nil}

	syncer.ParseEventContent = true
	syncer.OnEvent(client.StateStoreSyncHandler)

	syncer.OnEventType(event.EventMessage, mxclient._onMessage)
	syncer.OnEventType(event.StateMember, mxclient._onEvent)

	return mxclient, nil
}

func CreateClient(storage_path string, url string, userID string, accessToken string) (*MXClient, error) {
	return nil, fmt.Errorf("nope.")
}

func CreateClientPass(mxpassfile_path string, storage_path string, url string, localpart string, domain string) (*MXClient, error) {
	pf, err := mxpassfile.ReadPassfile(mxpassfile_path)
	if err != nil {
		return nil, err
	}
	//fmt.Printf("mxpass pf: '%#v'\n", pf)
	//fmt.Printf("mxpass find: '%s' '%s' '%s'\n", url, localpart, domain)
	e := pf.FindPasswordFill(url, localpart, domain)
	if e != nil {
		//fmt.Printf("mxpass: %#v\n", e)
		return NewMXClient(e.Matrixhost, id.NewUserID(e.Localpart, e.Domain), e.Token)
	}
	return nil, fmt.Errorf("nope.")
}
