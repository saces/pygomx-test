import os
from time import time_ns
import logging
import json
from smal.bot import SMALBot
from _pygomx import lib, ffi

# setup logging, we want timestamps
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)s %(name)s - %(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)


DEFAULT_PREFIX = "!"


@ffi.callback("void(char*)")
def on_event(evt):
    e = ffi.string(evt)
    print("Got an event: ", e)


@ffi.callback("void(char*)")
def on_message(msg):
    m = ffi.string(msg).decode("utf-8")

    msg = json.loads(m)

    if msg["type"] != "m.room.message":
        # not a room message
        logger.error(f"not a room message: {msg}")
        return

    if msg["sender"] == "get own id from missing code":
        # ignore own messages
        # for now just do not send valid commands by yourself
        logger.info(f"ignore own message: {msg}")
        return

    if "msgtype" in msg["content"].keys() and msg["content"]["msgtype"] != "m.text":
        # only react to messages, not emotes
        logger.debug(f"ignore unknown message type: {msg}")
        return

    if msg["content"]["body"] == "!stop":
        logger.info(f"stopping the bot")
        bot.stop()
        return

    if msg["content"]["body"].startswith("!echo"):
        logger.error(f"reply to this: {msg}")

        bot.sendmessage(msg["roomid"], "huhu")

        return

    logger.info(f"ignored a message: {msg}")


def main():
    # create and run the bot
    global bot
    bot = SMALBot(DEFAULT_PREFIX)
    bot.SetOnEventHandler(on_event)
    bot.SetOnMessageHandler(on_message)
    bot.run()


if __name__ == "__main__":
    main()
