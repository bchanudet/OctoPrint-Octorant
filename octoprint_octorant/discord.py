#coding: utf-8

# Simple module to send messages through a Discord WebHook

import json
import requests
from threading import Thread


class Hook(Thread):

    def __init__(self, url, message, username="", avatar="", attachment=None):
        Thread.__init__(self)
        self.url = url
        self.message = message
        self.username = username
        self.avatar = avatar
        self.attachment = attachment
        self.payload = {}

    def format(self):
        self.payload = {
            'content': self.message,
            'username' : self.username,
            'avatar_url' : self.avatar
        }

    def run(self):
        self.format()

        resp = requests.post(self.url,files=self.attachment,data=self.payload)
        if resp:
            return True
        else:
            return False