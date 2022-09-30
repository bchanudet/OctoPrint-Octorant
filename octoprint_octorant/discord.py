#coding: utf-8

# Simple module to send messages through a Discord WebHook

import json
import requests
from threading import Thread

from .media import Media


class DiscordMessage(Thread):

    def __init__(self, url, message, username="", avatar="", media:Media=None):
        Thread.__init__(self)
        self.url = url
        self.message = message
        self.username = username
        self.avatar = avatar
        self.media = media

    def run(self):
        file = None

        if self.media is not None:
            file = self.media.get()

        payload = {
            'content': self.message,
            'username' : self.username,
            'avatar_url' : self.avatar
        }

        resp = requests.post(
            self.url,
            files=file,
            data=payload
        )

        if resp:
            return True
        else:
            return False