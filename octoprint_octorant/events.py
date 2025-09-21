
color_default = 5793266
color_green = 8319575
color_red = 15882071

EVENTS = {
    # SYSTEM EVENTS
    "startup": {
        "enabled": True,
        "media": "",
        "message": "⏰ I just woke up! What are we gonna print today?",
        "variables": [],
        "embed_used": False,
        "embed_fields": [],
        "embed_color": color_default
    },
    "shutdown": {
        "enabled": True,
        "media": "",
        "message": "💤 Going to bed now!",
        "variables": [],
        "embed_used": False,
        "embed_fields": [],
        "embed_color": color_default
    },
    # PRINTER EVENTS
    "printer_state_connecting": {
        "enabled": False,
        "media": "",
        "message": "🔌 OctoPrint is connecting to your printer.",
        "variables": [],
        "embed_used": False,
        "embed_fields": [],
        "embed_color": color_default
    },
    "printer_state_operational": {
        "enabled": True,
        "media": "",
        "message": "✅ Your printer is operational.",
        "variables": [],
        "embed_used": False,
        "embed_fields": [],
        "embed_color": color_green
    },
    "printer_state_error": {
        "enabled": True,
        "media": "",
        "message": "⚠️ Your printer is in an erroneous state.",
        "variables": [],
        "embed_used": False,
        "embed_fields": [],
        "embed_color": color_red
    },
    "printer_state_unknown": {
        "enabled": True,
        "media": "",
        "message": "❔ Your printer is in an unknown state.",
        "variables": [],
        "embed_used": False,
        "embed_fields": [],
        "embed_color": color_red
    },
    "printer_state_offline": {
        "enabled": False,
        "media": "",
        "message": "❌ Your printer is offline.",
        "variables": [],
        "embed_used": False,
        "embed_fields": [],
        "embed_color": color_default
    },
    # PRINTS EVENTS
    "printing_started": {
        "enabled": True,
        "media": "snapshot",
        "message": "🖨️ I've started printing **{name}**",
        "variables": ["name", "path", "origin", "size", "owner", "user", "size_formatted"],
        "embed_used": False,
        "embed_fields": [
            ("Name", "name", True),
            ("Size", "size_formatted", True)
        ],
        "embed_color": color_default
    },
    "printing_paused": {
        "enabled": True,
        "media": "snapshot",
        "message": "⏸️ The printing was paused.",
        "variables": ["name", "path", "origin", "size", "owner", "user"],
        "embed_used": False,
        "embed_fields": [
            ("Name", "name", True),
            ("Size", "size_formatted", True)
        ],
        "embed_color": color_default
    },
    "printing_resumed": {
        "enabled": True,
        "media": "snapshot",
        "message": "▶️ The printing was resumed.",
        "variables": ["name", "path", "origin", "size", "owner", "user"],
        "embed_used": False,
        "embed_fields": [
            ("Name", "name", True),
            ("Size", "size_formatted", True)
        ],
        "embed_color": color_default
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
        "embed_used": False,
        "embed_fields": [
            ("Name", "name", True),
            ("Size", "size_formatted", True)
        ],
        "embed_color": color_red
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
        "embed_used": False,
        "embed_fields": [
            ("Name", "name", True),
            ("Size", "size_formatted", True),
            ("Time spent", "time_formatted", True)
        ],
        "embed_color": color_green
    },
    "printing_failed": {
        "enabled": True,
        "media": "snapshot",
        "message": "👎 Printing has failed! :(",
        "variables": [
            "name", 
            "path", 
            "origin", 
            "size", 
            "position", 
            "fileposition", 
            "progress", 
            "owner", 
            "user", 
            "time", 
            "time_formatted", 
            "reason"
        ],
        "embed_used": False,
        "embed_fields": [
            ("Name", "name", True),
            ("Size", "size_formatted", True),
            ("Time spent", "time_formatted", True),
            ("Stopped at", "progress", False),
            ("Reason", "reason", False)
        ],
        "embed_color": color_red
    },
    # SD TRANSFERS EVENTS
    "transfer_started": {
        "enabled": False,
        "media": "thumbnail",
        "message": "📼 Transfer started: {local} to {remote}",
        "variables": ["local", "remote"],
        "embed_used": False,
        "embed_fields": [
            ("Local", "local", False),
            ("Remote", "remote", False)
        ],
        "embed_color": color_default
    },
    "transfer_done": {
        "enabled": False,
        "media": "",
        "message": "📼 Transfer done in {time_formatted}",
        "variables": ["local", "remote", "time", "time_formatted"],
        "embed_used": False,
        "embed_fields": [
            ("Local", "local", False),
            ("Remote", "remote", False),
            ("Time spent", "time_formatted", True)
        ],
        "embed_color": color_green
    },
    "transfer_failed": {
        "enabled": False,
        "media": "",
        "message": "📼 Transfer has failed! :(",
        "variables": ["local", "remote", "time", "time_formatted"],
        "embed_used": False,
        "embed_fields": [
            ("Local", "local", False),
            ("Remote", "remote", False),
            ("Time spent", "time_formatted", True)
        ],
        "embed_color": color_red
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
            "size_formatted",
            "owner",
            "user",
            "progress",
            "progress_formatted",
            "spent",
            "spent_formatted",
            "remaining",
            "remaining_formatted",
            "reason"
        ],        
        "embed_used": False,
        "embed_fields": [
            ("Name", "name", True),
            ("Size", "size_formatted", True),
            ("Reason", "reason", True),
            ("Time spent", "spent_formatted", True),
            ("Remaining", "remaining_formatted", True)
            ("Progress", "progress_formatted", True),
        ],
        "embed_color": color_default
    },
    "transfer_progress": {
        "enabled": False,
        "media": "",
        "message": "📼 Transfer is at {progress}%",
        "variables": ["progress"],     
        "embed_used": False,
        "embed_fields": [
            ("Progress", "progress", True)
        ],
        "embed_color": color_default
    },
    # TIMELAPSES
    "timelapse_done": {
        "enabled": False,
        "media": "timelapse",
        "message": "🎥 Timelapse has been created: {movie_basename}",
        "variables": ["gcode", "movie", "movie_basename", "movie_basename_uri", "movie_prefix"],
        "embed_used": False,
        "embed_fields": [
            ("Gcode", "gcode", True),
            ("Filename", "movie_basename", True),
        ],
        "embed_color": color_green
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
        "embed_used": False,
        "embed_fields": [
            ("Gcode", "gcode", True),
            ("Filename", "movie_basename", True),
            ("Reason", "reason", False)
        ],
        "embed_color": color_green
    },
    # Not a real message, but we will treat it as one
    "test": {
        "enabled": True,
        "media": "snapshot",
        "message": "Hello hello! If you see this message, it means that the settings are correct!",
        "variables": [],
        "embed_used": True,
        "embed_fields": [],
        "embed_color": color_green
    },
}
