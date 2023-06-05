# OctoPrint-OctoRant 1.3.2


OctoRant is a plugin allowing Octoprint to send notifications to a Discord channel via a webhook URL. When wanted it can directly send a snapshot to Discord (without needing third-party services).

[![GitHub license](https://img.shields.io/github/license/bchanudet/OctoPrint-Octorant)](https://github.com/bchanudet/OctoPrint-Octorant/blob/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/bchanudet/OctoPrint-Octorant)](https://github.com/bchanudet/OctoPrint-Octorant/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/bchanudet/OctoPrint-Octorant)](https://github.com/bchanudet/OctoPrint-Octorant/issues)

## OctoRant is only a **notifier**!

OctoRant is *one-way only*, from your printer to your Discord channel. This plugin **is not able** to receive commands for your printer from Discord. However a good fellow @cameroncros forked the plugin exactly to add this feature. Feel free to try [DiscordRemote](https://plugins.octoprint.org/plugins/DiscordRemote/)

License : [MIT](./LICENSE)

## Changelog

### 1.3.0+

A lot of improvements came with this new version. Follow the 🎇 icon in this file to see what's new.

### History

See [the release history](https://github.com/bchanudet/OctoPrint-Octorant/releases) to get a quick summary of what's new in the latest versions.


## Setup

### Install the plugin

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/bchanudet/OctoPrint-Octorant/archive/master.zip

### Create the WebHook in Discord

Please follow [Discord's official guide on Webhooks](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks) to create a Webhook URL. Once you have it, head over to the plugin configuration to finish the setup.

## Configuration

The plugin can be configured in the configuration panel, under the "OctoRant" panel.

### Discord Settings

- **WebHook URL** : please follow the Setup procedure to retrieve the URL of the WebHook.
- **Bot name** : You can override the name you put on the WebHook description in Discord by a name. Useful if the webhook is not specific to OctoRant and also used for other things.
- **Bot Avatar URL** : You can also override the avatar us put in Discord for the WebHook. The URL needs to be globally accessible (it will be retrieved by Discord's servers).

In order for you to be sure these settings work, every time you change one of them, a test message will be sent to the corresponding Discord Channel. If you don't receive it, something is most likely wrong!

### Message Settings

Here you can customize every message handled by OctoRant.

- **Toggle the message** : by unchecking the checkbox in front of the message title, you can disable the message. It won't be sent to Discord.
- **Message** : you can change the default content here. See the section [Message format](#message-format) for more information.
- **Include media** : Embed a media with your message. Depending on the message you can choose which media to send:
    - **Webcam snapshot**: If configured in Octoprint, a snapshot of your webcam watching your printer
    - 🎇 **GCode thumbnail**: If your gcode files contains a preview thumbnail (according to PrusaSlicer format), OctoRant will send it.
    - 🎇 **Timelapse movie**: Only on the "timelapse done" message, you can make OctoRant try to send the timelapse to Discord. Beware of the upload limit of your destination server though (8MB by default, but can be more if the server is boosted)

### 🎇 Smart progress notifications

Coming in v1.3.0, OctoRant now includes several progress criterias that can be combined altogther:
- **Percentage of completion**: Be notified every `X`% during the print. _This is the new name of the option that existed in < 1.3.0 under the "Notify every XX%"_
- **Timed interval**: For long prints were percentage change too slowly, you can enable a timed notification every `X` seconds, from as low as every second.
- **Height**: _(in Beta)_ Be notified for each `X`mm. A _quick'n'dirty_ algorithm was set to discard unrelated movements (like hovering above the plate to do Z-homing at the center), but false positives are still possible

Considering those three criteria could generate a massive amount of messages, a fourth value is available:
- **Throttle notification**: When enabled, a minimum of `X` seconds between progress notifications will be respected.

### Scripts Settings

**🎇Depreciation notice**: Those settings are now deprecated and will be removed in a further release of the plugin. This is mostly due by the fact that Octoprint offers a much more powerful option with the [Event Manager](https://docs.octoprint.org/en/master/events/index.html), and also because I always thought I did a half-assed feature. In order to use the Event Manager with OctoRant, two new events are available : `plugin_octorant_before_notify` and `plugin_octorant_after_notify`. An `{event}` variable is available to know which event was triggered by OctoRant.

Octorant allows you to launch scripts everytime a message is sent:

- Before sending: perfect for turning some LED on to ensure the webcam will always have enough light when taking the snapshot
- After sending: perfect for turning the same LED off :)

Script configuration was made voluntarily a little harder, as running scripts exposes much more the host computer. You can find more indications on the [wiki](https://github.com/bchanudet/OctoPrint-Octorant/wiki/Launching-scripts)


## Message format

Messages are regular Discord messages, which means you can use :
- `**markdown**` format (see [Discord Documentation](https://support.discordapp.com/hc/en-us/articles/210298617-Markdown-Text-101-Chat-Formatting-Bold-Italic-Underline-))
- `:emoji:` shortcuts to display emojis
- Mentions are a little trickier:
    - General mentions (`@everyone`, `@here`) should work as usual
    - Role mentions (e.g. `@admin`) must be written `<@&ID>` (notice the `&`), where `ID` must be the [Role ID](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)
    - User mentions (e.g. `@bchanudet`) must be written `<@ID>` (no `&` here), where `ID` is the [User ID](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)

Some events also support variables. 🎇 The list of variables is now directly visible on the configuration page. 

For more reference, you can go to the [Octoprint documentation on Events](http://docs.octoprint.org/en/master/events/index.html#sec-events-available-events)

## Issues and Help

If you encounter any trouble don't hesitate to [open an issue](https://github.com/bchanudet/OctoPrint-Octorant/issues/new). I'll gladly do my best to help you setup this plugin.

This is my first project ever in Python, so if you happen to be more experimented and you noticed some bad things, feel free to tell me!
