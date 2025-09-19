EVENTS = {
    # SYSTEM EVENTS
    "startup": {
        "enabled": True,
        "media": "",
        "message": "⏰ I just woke up! What are we gonna print today?",
        "variables": [],
    },
    "shutdown": {
        "enabled": True,
        "media": "",
        "message": "💤 Going to bed now!",
        "variables": [],
    },
    # PRINTER EVENTS
    "printer_state_operational": {
        "enabled": True,
        "media": "",
        "message": "✅ Your printer is operational.",
        "variables": [],
    },
    "printer_state_error": {
        "enabled": True,
        "media": "",
        "message": "⚠️ Your printer is in an erroneous state.",
        "variables": [],
    },
    "printer_state_unknown": {
        "enabled": True,
        "media": "",
        "message": "❔ Your printer is in an unknown state.",
        "variables": [],
    },
    # PRINTS EVENTS
    "printing_started": {
        "enabled": True,
        "media": "snapshot",
        "message": "🖨️ I've started printing **{name}**",
        "variables": ["name", "path", "origin", "size", "owner", "user"],
    },
    "printing_paused": {
        "enabled": True,
        "media": "snapshot",
        "message": "⏸️ The printing was paused.",
        "variables": ["name", "path", "origin", "size", "owner", "user"],
    },
    "printing_resumed": {
        "enabled": True,
        "media": "snapshot",
        "message": "▶️ The printing was resumed.",
        "variables": ["name", "path", "origin", "size", "owner", "user"],
    },
    "printing_cancelled": {
        "enabled": True,
        "media": "snapshot",
        "message": "🛑 The printing was stopped.",
        "variables": [
            "name",
            "path",
            "origin",
            "size",
            "owner",
            "user",
            "time",
            "time_formatted",
        ],
    },
    "printing_done": {
        "enabled": True,
        "media": "snapshot",
        "message": "👍 Printing is done! Took about {time_formatted}",
        "variables": [
            "name",
            "path",
            "origin",
            "size",
            "owner",
            "user",
            "time",
            "time_formatted",
        ],
    },
    "printing_failed": {
        "enabled": True,
        "media": "snapshot",
        "message": "👎 Printing has failed! :(",
        "variables": ["time", "reason", "error"],
    },
    # SD TRANSFERS EVENTS
    "transfer_started": {
        "enabled": False,
        "media": "thumbnail",
        "message": "📼 Transfer started: {local} to {remote}",
        "variables": ["local", "remote"],
    },
    "transfer_done": {
        "enabled": False,
        "media": "",
        "message": "📼 Transfer done in {time_formatted}",
        "variables": ["local", "remote", "time", "time_formatted"],
    },
    "transfer_failed": {
        "enabled": False,
        "media": "",
        "message": "📼 Transfer has failed! :(",
        "variables": ["local", "remote", "time"],
    },
    # PROGRESS EVENTS
    "printing_progress": {
        "enabled": True,
        "media": "snapshot",
        "message": "📢 Printing is at {progress}%",
        "variables": [
            "name",
            "path",
            "origin",
            "size",
            "owner",
            "user",
            "progress",
            "spent",
            "remaining",
            "spent_formatted",
            "remaining_formatted",
        ],
    },
    "transfer_progress": {
        "enabled": False,
        "media": "",
        "message": "📼 Transfer is at {progress}%",
        "variables": ["progress"],
    },
    # TIMELAPSES
    "timelapse_done": {
        "enabled": False,
        "media": "timelapse",
        "message": "🎥 Timelapse has been created: {movie_basename}",
        "variables": ["gcode", "movie", "movie_basename", "movie_basename_uri", "movie_prefix"],
    },
    "timelapse_failed": {
        "enabled": False,
        "media": "",
        "message": "🎥 Timelapse is not available",
        "variables": [
            "gcode",
            "movie",
            "movie_basename",
            "movie_prefix",
            "returncode",
            "out",
            "error",
            "reason",
        ],
    },
    # Not a real message, but we will treat it as one
    "test": {
        "enabled": True,
        "media": "snapshot",
        "message": "Hello hello! If you see this message, it means that the settings are correct!",
    },
}
