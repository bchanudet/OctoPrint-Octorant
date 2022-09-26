# coding=utf-8

import requests
import os

from PIL import Image
from io import BytesIO


class Media:

    def __init__(self, settings, logger):
        self.settings = settings
        self.logger = logger

    def grab_snapshot(self):
        # output variable
        snapshot = None

        # request a snapshot from the URL
        try:
            snapshotCall = requests.get(self.settings.global_get(["webcam","snapshot"]))

            # flags from the settings page if we need specific manipulation
            mustFlipH = self.settings.global_get_boolean(["webcam","flipH"])
            mustFlipV = self.settings.global_get_boolean(["webcam","flipV"])
            mustRotate = self.settings.global_get_boolean(["webcam","rotate90"])

            if snapshotCall :
                snapshotImage = BytesIO(snapshotCall.content)				

                # Only call Pillow if we need to transpose anything
                if (mustFlipH or mustFlipV or mustRotate): 
                    img = Image.open(snapshotImage)

                    self.logger.info("Transformations : FlipH={}, FlipV={} Rotate={}".format(mustFlipH, mustFlipV, mustRotate))

                    if mustFlipH:
                        img = img.transpose(Image.FLIP_LEFT_RIGHT)
                    
                    if mustFlipV:
                        img = img.transpose(Image.FLIP_TOP_BOTTOM)

                    if mustRotate:
                        img = img.transpose(Image.ROTATE_90)

                    newImage = BytesIO()
                    img.save(newImage,'png')			

                    snapshotImage = newImage	

                snapshot = {'file': ("snapshot.png", snapshotImage.getvalue())}

        except requests.ConnectTimeout:
            snapshot = None
            self.logger.error("ConnectTimeout on: '{}'".format(self.settings.global_get(["webcam","snapshot"])))
        except requests.ConnectionError:
            snapshot = None
            self.logger.error("ConnectionError on: '{}'".format(self.settings.global_get(["webcam","snapshot"])))
        
        return snapshot

    def grab_file(self, filepath, max_accepted_size=0):
        if os.path.exists(filepath) == False:
            return None

        if max_accepted_size > 0 and os.stat(filepath).st_size > max_accepted_size:
            return None

        with open(filepath,"rb") as f:
            return {'file': (os.path.basename(filepath), f.read())}

        return None