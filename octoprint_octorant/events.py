CATEGORIES = ["system","printer","prints","transfers","progress","timelapses"]

EVENTS = {
    # SYSTEM EVENTS
    "startup" : {
        "category": "system",
        "name" : "Octoprint Startup",
        "enabled" : True,
        "media": "",
        "medias_list": ["snapshot"],
        "message" : "⏰ I just woke up! What are we gonna print today?"
    },
    "shutdown" : {
        "category": "system",
        "name" : "Octoprint Shutdown",
        "enabled" : True,
        "media": "",
        "medias_list": ["snapshot"],
        "message" : "💤 Going to bed now!"
    },
    # PRINTER EVENTS
    "printer_state_operational":{
        "category": "printer",
        "name" : "Printer state: operational",
        "enabled" : True,
        "media": "",
        "medias_list": ["snapshot"],
        "message" : "✅ Your printer is operational."
    },
    "printer_state_error":{
        "category": "printer",
        "name" : "Printer state: error",
        "enabled" : True,
        "media": "",
        "medias_list": ["snapshot"],
        "message" : "⚠️ Your printer is in an erroneous state."
    },
    "printer_state_unknown":{
        "category": "printer",
        "name" : "Printer state: unknown",
        "enabled" : True,
        "media": "",
        "medias_list": ["snapshot"],
        "message" : "❔ Your printer is in an unknown state."
    },
    # PRINTS EVENTS
    "printing_started":{
        "category": "prints",
        "name" : "Printing process: started",
        "enabled" : True,
        "media": "snapshot",
        "medias_list": ["thumbnail","snapshot"],
        "message" : "🖨️ I've started printing **{name}**"
    },
    "printing_paused":{
        "category": "prints",
        "name" : "Printing process: paused",
        "enabled" : True,
        "media": "snapshot",
        "medias_list": ["thumbnail","snapshot"],
        "message" : "⏸️ The printing was paused."
    },
    "printing_resumed":{
        "category": "prints",
        "name" : "Printing process: resumed",
        "enabled" : True,
        "media": "snapshot",
        "medias_list": ["thumbnail","snapshot"],
        "message" : "▶️ The printing was resumed."
    },
    "printing_cancelled":{
        "category": "prints",
        "name" : "Printing process: cancelled",
        "enabled" : True,
        "media": "snapshot",
        "medias_list": ["thumbnail","snapshot"],
        "message" : "🛑 The printing was stopped."
    },
    "printing_done":{
        "category": "prints",
        "name" : "Printing process: done",
        "enabled" : True,
        "media": "snapshot",
        "medias_list": ["thumbnail","snapshot"],
        "message" : "👍 Printing is done! Took about {time_formatted}"
    },
    "printing_failed":{
        "category": "prints",
        "name" : "Printing process: failed",
        "enabled" : True,
        "media": "snapshot",
        "medias_list": ["thumbnail","snapshot"],
        "message" : "👎 Printing has failed! :("
    },
    # SD TRANSFERS EVENTS
    "transfer_started":{
        "category": "transfers",
        "name" : "Transfer to SD card: started",
        "enabled" : False,
        "media": "thumbnail",
        "medias_list": ["thumbnail","snapshot"],
        "message" : "📼 Transfer started: {local} to {remote}"
    },
    "transfer_done":{
        "category": "transfers",
        "name" : "Transfer to SD card: done",
        "enabled" : False,
        "media": "",
        "medias_list": ["thumbnail","snapshot"],
        "message" : "📼 Transfer done in {time_formatted}"
    },
    "transfer_failed":{
        "category": "transfers",
        "name" : "Transfer to SD card: failed",
        "enabled" : False,
        "media": "",
        "medias_list": ["thumbnail","snapshot"],
        "message" : "📼 Transfer has failed! :("
    },

    # PROGRESS EVENTS
    "printing_progress":{
        "category": "progress",
        "name" : "Printing progress (by completion)",
        "enabled" : True,
        "media": "snapshot",
        "medias_list": ["thumbnail","snapshot"],
        "message" : "📢 Printing is at {progress}%",
        "step" : 10,
        "step_unit":"%"
    },
    "transfer_progress":{
        "category": "progress",
        "name" : "SD card transfer progress (by completion)",
        "enabled" : False,
        "media": "",
        "medias_list": ["thumbnail","snapshot"],
        "message" : "📼 Transfer is at {progress}%",
        "step" : 10,
        "step_unit":"%"
    },

    # TIMELAPSES
    "timelapse_done": {
        "category": "timelapses",
        "name": "Timelapse is available",
        "enabled": False,
        "media": "timelapse",
        "medias_list": ["snapshot","timelapse"],
        "message": "🎥 Timelapse has been created: {movie_basename}"
    },
    "timelapse_failed": {
        "category": "timelapses",
        "name": "Timelapse rendering has failed",
        "enabled": False,
        "media": "",
        "medias_list": ["snapshot"],
        "message": "🎥 Timelapse is not available"
    },

    # Not a real message, but we will treat it as one
    "test":{ 
        "category": "test",
        "name": "Test message",
        "enabled" : True,
        "media": "snapshot",
        "medias_list": ["snapshot"],
        "message" : "Hello hello! If you see this message, it means that the settings are correct!"
    },
}