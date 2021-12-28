CATEGORIES = ["system","printer","prints","progress"]

EVENTS = {
    "startup" : {
        "category": "system",
        "name" : "Octoprint Startup",
        "enabled" : True,
        "with_snapshot": False,
        "message" : "⏰ I just woke up! What are we gonna print today?"
    },
    "shutdown" : {
        "category": "system",
        "name" : "Octoprint Shutdown",
        "enabled" : True,
        "with_snapshot": False,
        "message" : "💤 Going to bed now!"
    },
    "printer_state_operational":{
        "category": "printer",
        "name" : "Printer state : operational",
        "enabled" : True,
        "with_snapshot": False,
        "message" : "✅ Your printer is operational."
    },
    "printer_state_error":{
        "category": "printer",
        "name" : "Printer state : error",
        "enabled" : True,
        "with_snapshot": False,
        "message" : "⚠️ Your printer is in an erroneous state."
    },
    "printer_state_unknown":{
        "category": "printer",
        "name" : "Printer state : unknown",
        "enabled" : True,
        "with_snapshot": False,
        "message" : "❔ Your printer is in an unknown state."
    },
    "printing_started":{
        "category": "prints",
        "name" : "Printing process : started",
        "enabled" : True,
        "with_snapshot": True,
        "message" : "🖨️ I've started printing **{name}**"
    },
    "printing_paused":{
        "category": "prints",
        "name" : "Printing process : paused",
        "enabled" : True,
        "with_snapshot": True,
        "message" : "⏸️ The printing was paused."
    },
    "printing_resumed":{
        "category": "prints",
        "name" : "Printing process : resumed",
        "enabled" : True,
        "with_snapshot": True,
        "message" : "▶️ The printing was resumed."
    },
    "printing_cancelled":{
        "category": "prints",
        "name" : "Printing process : cancelled",
        "enabled" : True,
        "with_snapshot": True,
        "message" : "🛑 The printing was stopped."
    },
    "printing_done":{
        "category": "prints",
        "name" : "Printing process : done",
        "enabled" : True,
        "with_snapshot": True,
        "message" : "👍 Printing is done! Took about {time_formatted}"
    },
    "printing_failed":{
        "category": "prints",
        "name" : "Printing process : failed",
        "enabled" : True,
        "with_snapshot": True,
        "message" : "👎 Printing has failed! :("
    },
    "printing_progress":{
        "category": "progress",
        "name" : "Printing progress (by completion)",
        "enabled" : True,
        "with_snapshot": True,
        "message" : "📢 Printing is at {progress}%",
        "step" : 10,
        "step_unit":"%"
    },
    "bed_cooled":{
        "category": "prints",
        "name" : "Printing process : bed cooled",
        "enabled" : True,
        "with_snapshot": True,
        "message" : "❄️ The print bed is cool!",
        "temperature" : 30,
        "temperature_unit" : "C"
    },
    "test":{ # Not a real message, but we will treat it as one
        "category": "test",
        "name": "Test message",
        "enabled" : True,
        "with_snapshot": True,
        "message" : "Hello hello! If you see this message, it means that the settings are correct!"
    },
}
