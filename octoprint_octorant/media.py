# coding=utf-8

import requests
import os
import base64
import re
import sys

from octoprint.util.version import is_octoprint_compatible

if is_octoprint_compatible(">=1.9"):
    from octoprint.webcams import get_snapshot_webcam

from PIL import Image
from io import BytesIO

GCODE_COMMENT_LINE_PREFIX = ";"
MAX_THUMBNAIL_SIZE_BYTES = 8192

reThumbDelim = re.compile("^thumbnail (begin [0-9]+x[0-9]+ ([0-9]+)|end)")


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

    def set_timelapse(self, filePath, maxAcceptedSize=0):
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

        if os.path.exists(self.filePath) is False:
            self.logger.debug("Gcode file not found: {}".format(self.filePath))
            return None

        with open(self.filePath, "r") as f:
            for line in f:
                if not line.startswith(GCODE_COMMENT_LINE_PREFIX):
                    # skip lines that are not full-line comments
                    continue

                if line.startswith("G1"):
                    # we hit first actions to the printer, better to stop now.
                    break

                # remove prefix and space/newline chars
                strippedLine = line[len(GCODE_COMMENT_LINE_PREFIX) :].strip()

                match = reThumbDelim.match(strippedLine)
                if match:
                    if match.group(1).startswith("begin"):
                        thumbnailSize = int(match.group(2))
                        self.logger.debug(
                            "Found thumbnail of {} bytes".format(thumbnailSize)
                        )

                        if thumbnailSize > MAX_THUMBNAIL_SIZE_BYTES:
                            self.logger.debug("skip, bigger than threshold")
                            thumbnailBegan = False
                            thumbnailB64 = ""
                        elif thumbnailSize > thumbnailLastSize:
                            thumbnailBegan = True
                            thumbnailLastSize = thumbnailSize
                            thumbnailB64 = ""
                        else:
                            self.logger.debug("skip, already got one bigger")
                            thumbnailBegan = False
                            thumbnailB64 = ""
                            continue

                    elif match.group(1).startswith("end"):
                        thumbnailBegan = False
                else:
                    if thumbnailBegan:
                        thumbnailB64 += strippedLine

        if len(thumbnailB64) > 0:
            return {"file": ("thumbnail.png", base64.b64decode(thumbnailB64))}

        self.logger.debug("No thumbnail found")
        return None

    def __grab_snapshot(self):
        # output variable
        snapshot = None
        snapshotImage = None

        if is_octoprint_compatible(">=1.9"):
            # OctoPrint 1.9+: Use the new functions to get the snapshot
            webcam = get_snapshot_webcam()

            if webcam is not None:
                self.mustFlipH = webcam.config.flipH
                self.mustFlipV = webcam.config.flipV
                self.mustRotate = webcam.config.rotate90
                snap = webcam.providerPlugin.take_webcam_snapshot(webcam.config.name)
                image = bytes().join(snap)
                self.logger.debug("Got snapshot of {} bytes".format(len(image)))
                snapshotImage = BytesIO(image)

        else:
            # request a snapshot from the URL
            try:
                snapshotCall = requests.get(self.url, stream=True)
                snapshotImage = BytesIO(snapshotCall.content)
            except requests.ConnectTimeout:
                snapshotImage = None
                self.logger.error("Error while fetching snapshot: ConnectTimeout")
            except requests.ConnectionError:
                snapshotImage = None
                self.logger.error("Error while fetching snapshot: ConnectTimeout")

        if snapshotImage is None:
            self.logger.error("Snapshot is empty")
            return None

        # Only call Pillow if we need to transpose anything
        if self.mustFlipH or self.mustFlipV or self.mustRotate:
            self.logger.debug(
                "Transformations on snapshot :"
                + "FlipH={}, FlipV={} Rotate={}".format(
                    self.mustFlipH, self.mustFlipV, self.mustRotate
                )
            )

            try:
                img = Image.open(snapshotImage)

                if self.mustFlipH:
                    img = img.transpose(Image.FLIP_LEFT_RIGHT)

                if self.mustFlipV:
                    img = img.transpose(Image.FLIP_TOP_BOTTOM)

                if self.mustRotate:
                    img = img.transpose(Image.ROTATE_90)

                newImage = BytesIO()
                img.save(newImage, "jpeg")

                snapshotImage = newImage.getvalue()
            except:
                self.logger.error(sys.exc_info())

            finally:
                if len(snapshotImage) == 0:
                    self.logger.error("Snapshot result is empty")
                    return None

        snapshot = {"file": ("snapshot.jpg", snapshotImage)}

        return snapshot

    def __grab_file(self):
        if os.path.exists(self.filePath) is False:
            self.logger.debug("Media not found: {}".format(self.filePath))
            return None

        if os.stat(self.filePath).st_size <= 0:
            self.logger.debug("Media seems empty")
            return None

        if (
            self.maxAcceptedSize > 0
            and os.stat(self.filePath).st_size > self.maxAcceptedSize
        ):
            self.logger.debug("Media bigger than max allowed size")
            return None

        with open(self.filePath, "rb") as f:
            return {"file": (os.path.basename(self.filePath), f.read())}

        return None
