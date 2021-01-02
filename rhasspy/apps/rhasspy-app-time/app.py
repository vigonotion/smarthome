"""Example app to react to an intent to tell you the time."""
import logging
from datetime import datetime
import os

from rhasspyhermes.nlu import NluIntent
from rhasspyhermes_app import EndSession, HermesApp

_LOGGER = logging.getLogger("TimeApp")

host=os.getenv("MQTT_HOST", "localhost")
port=os.getenv("MQTT_PORT", 1883)
username=os.getenv("MQTT_USERNAME")
password=os.getenv("MQTT_PASSWORD")

app = HermesApp("TimeApp", host=host, port=port, username=username, password=password)


@app.on_intent("GetTime")
async def get_time(intent: NluIntent):
    """Tell the time."""
    _LOGGER.info("GetTime")
    now = datetime.now().strftime("%H:%M")
    return EndSession(f"Es ist {now} Uhr.")

@app.on_intent("GetDate")
async def get_date(intent: NluIntent):
    """Tell the date."""
    _LOGGER.info("GetDate")
    now = datetime.now().strftime("%d.%m.%Y")
    return EndSession(f"Heute ist der {now}.")


_LOGGER.info(f"Starting app {app.client_name}.")
app.run()