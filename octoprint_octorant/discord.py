#coding: utf-8

# Simple module to send messages through a Discord WebHook

import json
import requests
from threading import Thread


class DiscordMessage(Thread):

    def __init__(self, url, message, username="", avatar="", attachment=None):
        Thread.__init__(self)
        self.url = url
        self.message = message
        self.username = username
        self.avatar = avatar
        self.file = attachment

    def set_file(self, filename, content):
        self.file = {'file': (filename, content)}

    def run(self):
        payload = {
            'content': self.message,
            'username' : self.username,
            'avatar_url' : self.avatar
        }

        resp = requests.post(
            self.url,
            files=self.file,
            data=payload
        )

        if resp:
            return True
        else:
            return False