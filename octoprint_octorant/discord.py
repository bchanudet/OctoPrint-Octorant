# coding: utf-8

# Simple module to send messages through a Discord WebHook

import logging
import time
import requests

from threading import Thread
from octoprint.util import TypedQueue
from .media import Media


class Message:
    def __init__(self, content: str, media: Media = None) -> None:
        self.content = content
        self.media: Media = media


class DiscordMessage(Thread):
    def __init__(self, logger: logging.Logger):
        Thread.__init__(self, daemon=True)

        self._logger = logger

        self.url = ""
        self.username = ""
        self.avatar = ""
        self.thread_id = 0

        self.queue = TypedQueue()
        self.stop_until = 0

    def set_config(self, url, username="", avatar="", thread_id=0):
        self.url = url
        self.username = username
        self.avatar = avatar
        self.thread_id = thread_id

    def send_message(self, content: str, media: Media = None):
        if self.stop_until > time.time():
            self._logger.debug(
                "Rate limited by Discord until: {}".format(self.stop_until)
            )
            return

        # Setup variables
        message = Message(content, media)

        self._logger.debug(
            "Adding message to queue: {} (rate-limit: {})".format(
                message.content, self.stop_until
            )
        )
        self.queue.put(message)

        if self.is_alive() is False:
            self.start()

        return

    def run(self):
        while True:
            message: Message = self.queue.get()

            if self.stop_until > time.time():
                self.queue.task_done()
                self._logger.warn(
                    "Not sent because of rate-limiting until {}".format(self.stop_until)
                )
                continue

            file = None

            # If not setup, just close already
            if self.url == "":
                self.queue.task_done()
                self._logger.debug("DiscordMessage: No Webhook URL provided")
                continue

            if message.content == "":
                self.queue.task_done()
                self._logger.debug("DiscordMessage: Content is empty")
                continue

            # Grab the media
            if message.media is not None:
                file = message.media.get()

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
                    files=file,
                    data=payload,
                    timeout=60,
                )

                if response.status_code == 429:
                    data = response.json()
                    if int(data["retry_after"]) > 0:
                        self.stop_until = time.time() + (
                            int(data["retry_after"]) / 1000
                        )

                    self._logger.debug(data)
                    self._logger.warn(
                        "Rate limited by Discord API. Won't send message until {}".format(
                            self.stop_until
                        )
                    )
                else:
                    self.stop_until = 0

            except requests.ConnectTimeout:
                self._logger.error(
                    "ConnectTimeout triggered when sending message to Discord"
                )
            except requests.ConnectionError:
                self._logger.error(
                    "ConnectionError triggered when sending message to Discord"
                )

            finally:
                self.queue.task_done()
