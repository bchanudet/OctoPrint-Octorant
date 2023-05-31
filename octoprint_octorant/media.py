# coding=utf-8

from ast import Pass
from email.mime import base
import requests
import os
import base64
import re

from PIL import Image
from io import BytesIO

GCODE_COMMENT_LINE_PREFIX = ';'
MAX_THUMBNAIL_SIZE_BYTES = 8192

regexThumbnailDelimiter = re.compile("^thumbnail (begin [0-9]+x[0-9]+ ([0-9]+)|end)")

class Media:

    def __init__(self, settings, logger):
        self.settings = settings
        self.logger = logger

        self.type = None

        # For gcode thumbnail and timelapses
        self.filePath = ""

        # For snapshot
        self.url = ""
        self.mustFlipH = False
        self.mustFlipV = False
        self.mustRotate = False

        # For timelapse
        self.maxAcceptedSize = 0
        

    def set_thumbnail(self, filePath):
        self.logger.debug("Media is thumbnail: {}".format(filePath))
        self.type = "thumbnail"
        self.filePath = filePath

    def set_snapshot(self, url, mustFlipH, mustFlipV, mustRotate):
        self.logger.debug("Media is snapshot: {}".format(url))
        self.type = "snapshot"
        self.url = url
        self.mustFlipH = mustFlipH
        self.mustFlipV = mustFlipV
        self.mustRotate = mustRotate

    def set_timelapse(self, filePath, maxAcceptedSize = 0):
        self.logger.debug("Media is timelapse: {}".format(filePath))
        self.type = "timelapse"
        self.filePath = filePath
        self.maxAcceptedSize = maxAcceptedSize
        

    def get(self):
        if self.type == "thumbnail":
            return self.__grab_gcode_thumbnail()
        elif self.type == "snapshot":
            return self.__grab_snapshot()
        elif self.type == "timelapse":
            return self.__grab_file()

        return None

    def __grab_gcode_thumbnail(self):
        thumbnailB64 = ""
        thumbnailBegan = False
        thumbnailLastSize = -1

        if os.path.exists(self.filePath) == False: 
            self.logger.debug("Gcode file not found: {}".format(self.filePath))
            return None

        with open(self.filePath, 'r') as f:
            for line in f:
                if not line.startswith(GCODE_COMMENT_LINE_PREFIX):
                    # skip lines that are not full-line comments
                    continue

                if line.startswith("G1"):
                    # we hit first actions to the printer, better to stop now.
                    break

                # remove prefix and space/newline chars
                strippedLine = line[len(GCODE_COMMENT_LINE_PREFIX):].strip()

                match = regexThumbnailDelimiter.match(strippedLine)
                if match:
                    if match.group(1).startswith("begin"):
                        thumbnailSize = int(match.group(2))
                        self.logger.debug("Found thumbnail of {} bytes".format(thumbnailSize))
                        if thumbnailSize > thumbnailLastSize:
                            thumbnailBegan = True
                            thumbnailLastSize = thumbnailSize
                            thumbnailB64 = ""
                        else:
                            self.logger.debug("Skipped, already got a bigger thumbnail")
                            thumbnailBegan = False
                            thumbnailB64 = ""
                            continue

                    elif match.group(1).startswith("end"):
                        thumbnailBegan = False
                else:
                    if thumbnailBegan:
                        thumbnailB64 += strippedLine
        
        if len(thumbnailB64) > 0:
            return {'file': ("thumbnail.png", base64.b64decode(thumbnailB64))}

        self.logger.debug("No thumbnail found")
        return None      

    def __grab_snapshot(self):
        # output variable
        snapshot = None

        # request a snapshot from the URL
        try:
            snapshotCall = requests.get(self.url)

            if snapshotCall :
                snapshotImage = BytesIO(snapshotCall.content)				

                # Only call Pillow if we need to transpose anything
                if (self.mustFlipH or self.mustFlipV or self.mustRotate): 
                    img = Image.open(snapshotImage)

                    self.logger.debug("Transformations on snapshot : FlipH={}, FlipV={} Rotate={}".format(self.mustFlipH, self.mustFlipV, self.mustRotate))

                    if self.mustFlipH:
                        img = img.transpose(Image.FLIP_LEFT_RIGHT)
                    
                    if self.mustFlipV:
                        img = img.transpose(Image.FLIP_TOP_BOTTOM)

                    if self.mustRotate:
                        img = img.transpose(Image.ROTATE_90)

                    newImage = BytesIO()
                    img.save(newImage,'png')			

                    snapshotImage = newImage	

                snapshot = {'file': ("snapshot.png", snapshotImage.getvalue())}

        except requests.ConnectTimeout:
            snapshot = None
            self.logger.error("Error while fetching snapshot: ConnectTimeout")
        except requests.ConnectionError:
            snapshot = None
            self.logger.error("Error while fetching snapshot: ConnectTimeout")
        
        return snapshot

    def __grab_file(self):
        if os.path.exists(self.filePath) == False:
            self.logger.debug("Media not found: {}".format(self.filePath))
            return None

        if self.maxAcceptedSize > 0 and os.stat(self.filePath).st_size > self.maxAcceptedSize:
            self.logger.debug("Media bigger than max allowed size")
            return None

        with open(self.filePath,"rb") as f:
            return {'file': (os.path.basename(self.filePath), f.read())}

        return None
