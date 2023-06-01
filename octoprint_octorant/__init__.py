# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import octoprint.settings
import octoprint.util
import subprocess
import datetime
import time
import os

from octoprint.events import Events, eventManager
from octoprint.util import RepeatedTimer
from .discord import DiscordMessage
from .events import EVENTS
from .media import Media


class OctorantPlugin(
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.EventHandlerPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin,
):
    def __init__(self):
        self.events = EVENTS
        self.uploading = False

        # progress specific variables
        self.progressTimer = None
        self.lastProgressNotifiedAt = 0
        self.lastProgressPercent = 0
        self.lastProgressTime = 0
        self.lastProgressHeight = 0

        # Discord webhook handler
        self.discord: DiscordMessage = None

    def initialize(self):
        # Instantiate Discord handler
        self.discord = DiscordMessage(self._logger)
        self.discord.set_config(
            self._settings.get(["url"], merged=True),
            self._settings.get(["username"], merged=True),
            self._settings.get(["avatar"], merged=True),
        )

    def on_after_startup(self):
        self._logger.info("OctoRant is started!")

    ##~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return {
            "url": "",
            "username": "",
            "avatar": "",
            "events": self.events,
            "allow_scripts": False,
            "script_before": "",
            "script_after": "",
            "progress": {
                "percentage_enabled": True,
                "percentage_step": 10,
                "time_enabled": False,
                "time_step": 0,
                "height_enabled": False,
                "height_step": 0,
                "throttle_enabled": False,
                "throttle_step": 0,
            },
        }

    # Restricts some paths to some roles only
    def get_settings_restricted_paths(self):
        # settings.events.tests is a false message, so we should never see it as configurable.
        # settings.url, username and avatar are admin only.
        return dict(
            never=[["events", "test"]],
            admin=[
                ["url"],
                ["username"],
                ["avatar"],
                ["script_before"],
                ["script_after"],
            ],
        )

    # Overrides
    def on_settings_save(self, data):
        old_bot_settings = "{}{}{}".format(
            self._settings.get(["url"], merged=True),
            self._settings.get(["avatar"], merged=True),
            self._settings.get(["username"], merged=True),
        )

        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

        new_bot_settings = "{}{}{}".format(
            self._settings.get(["url"], merged=True),
            self._settings.get(["avatar"], merged=True),
            self._settings.get(["username"], merged=True),
        )

        if old_bot_settings != new_bot_settings:
            self._logger.info("Settings have changed. Send a test message...")

            self.discord.set_config(
                self._settings.get(["url"], merged=True),
                self._settings.get(["username"], merged=True),
                self._settings.get(["avatar"], merged=True),
            )

            self.notify_event("test")

    def get_settings_version(self):
        return 2

    def on_settings_migrate(self, target, current):
        self._logger.debug("Migrating settings from {} to {}".format(current, target))

        if current == None and target == 2:
            for evt in self._settings.get(["events"]):
                if self._settings.get(["events", evt, "with_snapshot"]) != None:
                    self._logger.debug("Migrating event {}".format(evt))
                    self._settings.set(
                        ["events", evt, "media"],
                        "snapshot"
                        if self._settings.get_boolean(["events", evt, "with_snapshot"])
                        == True
                        else "none",
                    )
                    self._settings.remove(["events", evt, "with_snapshot"])

            if self._settings.get(["events", "progress", "enabled"]) != None:
                self._settings.set_boolean(
                    ["progress", "percentage_enabled"],
                    self._settings.get_boolean(["events", "progress", "enabled"]),
                )
                self._settings.set_int(
                    ["progress", "percentage_step"],
                    self._settings.get_int(["events", "progress", "step"], merged=True),
                )

        self._logger.debug("Migration done!")

    ##~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return dict(js=["js/octorant.js"], css=["css/octorant.css"])

    ##~~ TemplatePlugin mixin
    def get_template_configs(self):
        return [dict(type="settings", custom_bindings=True)]

    ##~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
        # for details.
        return dict(
            octorant=dict(
                displayName="OctoRant Plugin",
                displayVersion=self._plugin_version,
                # version check: github repository
                type="github_release",
                user="bchanudet",
                repo="OctoPrint-Octorant",
                current=self._plugin_version,
                # update method: pip
                pip="https://github.com/bchanudet/OctoPrint-Octorant/archive/{target_version}.zip",
            )
        )

    def register_custom_events(*args, **kwargs):
        return ["before_notify", "after_notify"]

    ##~~ EventHandlerPlugin hook
    def on_event(self, event: str, payload):
        # Let's avoid dealing with our own events...
        if event.startswith("plugin_octorant"):
            return

        # System
        if event == Events.STARTUP:
            return self.notify_event("startup")
        if event == Events.SHUTDOWN:
            return self.notify_event("shutdown")

        # Printer
        if event == Events.PRINTER_STATE_CHANGED:
            if payload["state_id"] == "OPERATIONAL":
                return self.notify_event("printer_state_operational")
            elif payload["state_id"] == "ERROR":
                return self.notify_event("printer_state_error")
            elif payload["state_id"] == "UNKNOWN":
                return self.notify_event("printer_state_unknown")
            else:
                self._logger.debug(
                    "Event {}/{} was not handled".format(event, payload["state_id"])
                )

        # Prints
        if event == Events.PRINT_STARTED:
            self.uploading = False
            self.start_progress_check()
            return self.notify_event("printing_started", payload)
        if event == Events.PRINT_PAUSED:
            self.stop_progress_check()
            return self.notify_event("printing_paused", payload)
        if event == Events.PRINT_RESUMED:
            self.uploading = False
            self.start_progress_check()
            return self.notify_event("printing_resumed", payload)
        if event == Events.PRINT_CANCELLED:
            self.stop_progress_check()
            return self.notify_event("printing_cancelled", payload)
        if event == Events.PRINT_DONE:
            self.stop_progress_check()
            payload["time_formatted"] = str(
                datetime.timedelta(seconds=int(payload["time"]))
            )
            return self.notify_event("printing_done", payload)

        # SD Card transfer
        if event == Events.TRANSFER_STARTED:
            self.uploading = True
            self.start_progress_check()
            return self.notify_event("transfer_started", payload)
        if event == Events.TRANSFER_DONE:
            payload["time_formatted"] = str(
                datetime.timedelta(seconds=int(payload["time"]))
            )
            self.uploading = False
            self.stop_progress_check()
            self.notify_event("transfer_done", payload)
            return True
        if event == Events.TRANSFER_FAILED:
            self.uploading = False
            self.stop_progress_check()
            self.notify_event("transfer_failed", payload)
            return True

        # Timelapses
        if event == Events.MOVIE_DONE:
            return self.notify_event("timelapse_done", payload)
        if event == Events.MOVIE_FAILED:
            return self.notify_event("timelapse_failed", payload)

        # Helps discovering new events that ae not documented
        self._logger.debug("Event {} was not handled".format(event))
        return True

    def start_progress_check(self):
        # If already set, we must stop it
        if self.progressTimer is not None:
            self.stop_progress_check()

        # Reset all variables
        self.lastProgressNotifiedAt = 0
        self.lastProgressPercent = 0
        self.lastProgressTime = 0
        self.lastProgressHeight = 0

        # Start the thread
        self.progressTimer = RepeatedTimer(0.5, self.progress_check)
        self.progressTimer.start()

    def stop_progress_check(self):
        if self.progressTimer is not None:
            self.progressTimer.cancel()
            self.progressTimer = None

    def progress_check(self):
        notifyReason = ""

        # First we check the throttle and return if we are too early
        if (
            self._settings.get_boolean(["progress", "throttle_enabled"], merged=True)
            == True
        ):
            if time.time() < (
                self.lastProgressNotifiedAt
                + self._settings.get_int(["progress", "throttle_step"], merged=True)
            ):
                return

        # Get the printer data
        printer_data = self._printer.get_current_data()

        # don't do anything if the printer is paused
        if self._printer.is_pausing():
            return

        # Time check.
        if (
            notifyReason == ""
            and self._settings.get_boolean(["progress", "time_enabled"], merged=True)
            == True
        ):
            if time.time() > (
                self.lastProgressTime
                + self._settings.get_int(["progress", "time_step"], merged=True)
            ):
                self._logger.debug(
                    "Progress Check: Timer threshold was hit (last: {}, current: {})".format(
                        self.lastProgressTime, time.time()
                    )
                )
                self.lastProgressTime = time.time()
                notifyReason = "time"
            else:
                self._logger.debug(
                    "Progress Check: Timer not triggerd (last: {}, current: {})".format(
                        self.lastProgressTime, time.time()
                    )
                )

        # Percentage check
        if (
            notifyReason == ""
            and self._settings.get_boolean(
                ["progress", "percentage_enabled"], merged=True
            )
            == True
        ):
            if int(printer_data["progress"]["completion"]) > 0:
                if int(printer_data["progress"]["completion"]) > (
                    self.lastProgressPercent
                    + self._settings.get_int(
                        ["progress", "percentage_step"], merged=True
                    )
                ):
                    self._logger.debug(
                        "Progress Check: Percentage threshold was hit (last: {}, current: {})".format(
                            self.lastProgressPercent,
                            int(printer_data["progress"]["completion"]),
                        )
                    )
                    self.lastProgressPercent = int(
                        printer_data["progress"]["completion"]
                    )
                    notifyReason = "percentage"
                else:
                    self._logger.debug(
                        "Progress Check: Percentage not triggerd (last: {}, current: {})".format(
                            self.lastProgressPercent,
                            int(printer_data["progress"]["completion"]),
                        )
                    )

        # Height check
        if (
            notifyReason == ""
            and self._settings.get_boolean(["progress", "height_enabled"], merged=True)
            == True
        ):
            if printer_data["currentZ"] is not None:
                # let's check for abnormal Z moves and discard them.
                # basic test if the current Z is larger than 5 times the step configured, that means a strange move that we'll discard.
                if float(printer_data["currentZ"]) > 0 and float(
                    printer_data["currentZ"]
                ) > (
                    self.lastProgressHeight
                    + (
                        self._settings.get_float(
                            ["progress", "height_step"], merged=True
                        )
                        * 5
                    )
                ):
                    return

                if float(printer_data["currentZ"]) > 0 and float(
                    printer_data["currentZ"]
                ) > (
                    self.lastProgressHeight
                    + self._settings.get_float(["progress", "height_step"], merged=True)
                ):
                    self._logger.debug(
                        "Progress Check: Height threshold was hit (last: {}, current: {})".format(
                            self.lastProgressHeight, float(printer_data["currentZ"])
                        )
                    )
                    self.lastProgressHeight = float(printer_data["currentZ"])
                    notifyReason = "height"

                else:
                    self._logger.debug(
                        "Progress Check: Height not triggerd (last: {}, current: {})".format(
                            self.lastProgressHeight, float(printer_data["currentZ"])
                        )
                    )

        # Alright let's notify if necessary
        if notifyReason != "":
            self.lastProgressNotifiedAt = time.time()
            payload = {}
            payload["reason"] = notifyReason

            if self.uploading == False:
                payload = self._printer._payload_for_print_job_event()

                payload["reason"] = notifyReason
                payload["progress"] = 0
                payload["remaining"] = 0
                payload["remaining_formatted"] = "0s"
                payload["spent"] = 0
                payload["spent_formatted"] = "0s"

                if printer_data["progress"] is not None:
                    if printer_data["progress"]["printTimeLeft"] is not None:
                        payload["remaining"] = int(
                            printer_data["progress"]["printTimeLeft"]
                        )
                        payload["remaining_formatted"] = str(
                            datetime.timedelta(seconds=payload["remaining"])
                        )
                    if printer_data["progress"]["printTime"] is not None:
                        payload["spent"] = int(printer_data["progress"]["printTime"])
                        payload["spent_formatted"] = str(
                            datetime.timedelta(seconds=payload["spent"])
                        )
                    if printer_data["progress"]["completion"] is not None:
                        payload["progress"] = int(
                            printer_data["progress"]["completion"]
                        )

            self.notify_event(
                "printing_progress" if not self.uploading else "transfer_progress",
                payload,
            )

    def notify_event(self, eventID, data={}):
        if eventID not in self.events:
            self._logger.error("Tried to notifiy on inexistant eventID : ", eventID)
            return False

        event_configuration = self._settings.get(["events", eventID], merged=True)

        if event_configuration["enabled"] != True:
            self._logger.debug(
                "Event {} is not enabled. Returning gracefully".format(eventID)
            )
            return False

        # Alter a bit the payload to offer more variables
        if "time" in data:
            data["time_formatted"] = str(datetime.timedelta(seconds=int(data["time"])))

        self._logger.debug(
            "Available variables for event " + eventID + ": " + ", ".join(list(data))
        )
        try:
            message = event_configuration["message"].format(**data)
        except KeyError as error:
            # Detected some tags that are not found in the payload
            message = (
                event_configuration["message"]
                + """\r\n:sos: **OctoRant Error**: unknown variable `{"""
                + error.args[0]
                + """}`."""
            )
        finally:
            # Let's get some media
            media = Media(self._settings, self._logger)

            if event_configuration["media"] != "":
                if event_configuration["media"] == "thumbnail":
                    media.set_thumbnail(
                        self._file_manager.path_on_disk(data["origin"], data["path"])
                    )
                elif event_configuration["media"] == "snapshot":
                    media.set_snapshot(
                        url=self._settings.global_get(["webcam", "snapshot"]),
                        mustFlipH=self._settings.global_get_boolean(
                            ["webcam", "flipH"]
                        ),
                        mustFlipV=self._settings.global_get_boolean(
                            ["webcam", "flipV"]
                        ),
                        mustRotate=self._settings.global_get_boolean(
                            ["webcam", "rotate90"]
                        ),
                    )
                elif event_configuration["media"] == "timelapse":
                    media.set_timelapse(filePath=data["movie"])

            return self.send_message(eventID, message, media)

    def exec_script(self, eventName, which=""):
        # I want to be sure that the scripts are allowed by the special configuration flag
        scripts_allowed = self._settings.get(["allow_scripts"], merged=True)
        if scripts_allowed is None or scripts_allowed == False:
            return ""

        # Finding which one should be used.
        script_to_exec = None
        if which == "before":
            script_to_exec = self._settings.get(["script_before"], merged=True)

        elif which == "after":
            script_to_exec = self._settings.get(["script_after"], merged=True)  # type: ignore

        # Finally exec the script
        out = ""
        self._logger.debug(
            "{}:{} File to start: '{}'".format(eventName, which, script_to_exec)
        )

        try:
            if (
                script_to_exec is not None
                and len(script_to_exec) > 0
                and os.path.exists(script_to_exec)
            ):
                out = subprocess.check_output(script_to_exec)
        except (OSError, subprocess.CalledProcessError) as err:
            out = err
        finally:
            self._logger.debug("{}:{} > Output: '{}'".format(eventName, which, out))
            return out

    def send_message(self, eventID, message, media: Media = None):
        # return false if no URL is provided
        if "http" not in self._settings.get(["url"], merged=True):
            return False

        # exec "before" script if any
        eventManager().fire("plugin_octorant_before_notify", {"event": eventID})
        self.exec_script(eventID, "before")

        # Send to Discord WebHook
        self.discord.send_message(message, media)

        # exec "after" script if any
        self.exec_script(eventID, "after")
        eventManager().fire("plugin_octorant_after_notify", {"event": eventID})

        return True


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "OctoRant"
__plugin_pythoncompat__ = ">=2.7,<4"


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = OctorantPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
        "octoprint.events.register_custom_events": __plugin_implementation__.register_custom_events,
    }
