# coding: utf-8

# Simple module to send messages through a Discord WebHook

import logging
import time
import requests
import traceback
import queue
import json

from threading import Thread
from octoprint.events import Events, eventManager

from .media import Media


class Message:
    def __init__(self, event_id = "") -> None:
        self.event_id = event_id
        self.content = ""
        self.media = None
        self.embed = None


class DiscordSender(Thread):
    def __init__(self, logger: logging.Logger):
        Thread.__init__(self, daemon=True, name="octorant-discord-sender")

        self._logger = logger

        self.url = ""
        self.username = ""
        self.avatar = ""
        self.thread_id = 0

        self.queue = queue.Queue()
        self.stop_until = 0

        self.start()
        self._logger.debug("Discord thread has started")

    def set_config(self, url, username="", avatar="", thread_id=0):
        self.url = url
        self.username = username
        self.avatar = avatar
        self.thread_id = thread_id

    def send_message(self, message: Message):
        if self.stop_until > time.time():
            self._logger.debug(
                "Rate limited by Discord until: {}".format(self.stop_until)
            )
            return

        self._logger.debug(
            "Adding message to queue: {} (rate-limit: {})".format(
                message.content, self.stop_until
            )
        )
        self.queue.put(message)

    def run(self):
        while True:
            message: Message = self.queue.get()
            files = list()

            if self.stop_until > time.time():
                self.queue.task_done()
                self._logger.warn(
                    "Not sent because of rate-limiting until {}".format(self.stop_until)
                )
                continue

            # If not setup, just close already
            if self.url == "":
                self.queue.task_done()
                self._logger.debug("DiscordMessage: No Webhook URL provided")
                continue

            if message.content == "" and message.embed is None:
                self.queue.task_done()
                self._logger.debug("DiscordMessage: Message is empty")
                continue

            eventManager().fire("plugin_octorant_before_notify", {"event": message.event_id })

            # Grab the media
            if message.media is not None and message.media.type is not None:
                files.append(message.media.get())

            # Setup the payload
            payload = {
                "content": message.content,
            }

            if self.username != "":
                payload["username"] = self.username

            if self.avatar != "":
                payload["avatar_url"] = self.avatar

            try:
                response: requests.Response = requests.post(
                    self.url
                    + (
                        "?thread_id={}".format(self.thread_id)
                        if self.thread_id > 0
                        else ""
                    ),
                    data = {
                        "payload_json": json.dumps(payload)
                    },
                    files=files,
                    timeout=60,
                )

                self.stop_until = 0

                self._logger.debug("Discord Response status_code: {}".format(response.status_code))
                if response.status_code == 429:
                    data = response.json()
                    if int(data["retry_after"]) > 0:
                        self.stop_until = time.time() + (
                            int(data["retry_after"]) / 1000
                        )

                    self._logger.debug(data)
                    self._logger.warning(
                        "Rate limited by Discord API. Won't send message until {}".format(
                            self.stop_until
                        )
                    )
                elif response.status_code >= 300:
                    self._logger.warning(
                        "Error from Discord webhook: {}".format(
                            response.content
                        )
                    )

            except requests.ConnectTimeout:
                self._logger.error(
                    "ConnectTimeout triggered when sending message to Discord"
                )
            except requests.ConnectionError:
                self._logger.error(
                    "ConnectionError triggered when sending message to Discord"
                )

            except Exception as e:
                self._logger.error("Exception in Sender: {} {}".format(e, traceback.format_exc()))

            finally:
                eventManager().fire("plugin_octorant_after_notify", {"event": message.event_id})
                self.queue.task_done()
