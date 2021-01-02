"""Example app to react to an intent to tell you the time."""
import random
import logging
from datetime import datetime
import os

from pyowm import OWM
from pyowm.commons.exceptions import PyOWMError
from pyowm.utils import config
from pyowm.utils import timestamps
from rhasspyhermes.intent import Slot

from rhasspyhermes.nlu import NluIntent
from rhasspyhermes_app import EndSession, HermesApp

_LOGGER = logging.getLogger("WeatherApp")

host=os.getenv("MQTT_HOST", "localhost")
port=int(os.getenv("MQTT_PORT", "1883"))
username=os.getenv("MQTT_USERNAME")
password=os.getenv("MQTT_PASSWORD")

owm_key=os.getenv("OWM_KEY")
owm_default_geolocation=os.getenv("OWM_DEFAULT_GEOLOCATION", "52.5065133,13.1445612")

app = HermesApp("WeatherApp", host=host, port=port, username=username, password=password)

config_dict = config.get_default_config()
config_dict['language'] = 'de'

owm = OWM(owm_key, config_dict)
mgr = owm.weather_manager()
city_id_registry = owm.city_id_registry()

def get_slot(intent: NluIntent, slot_name: str, default=None):
    """extracts the value of a slot"""

    slot = next(filter(lambda slot: slot.slot_name == slot_name, intent.slots), None)
    if slot:
        return (slot.value.get("value", default), slot.raw_value)
    return default, None

@app.on_intent("GetTemperature")
async def get_temperature_intent(intent: NluIntent):
    """Tell the temperature."""

    raw_geolocation, raw_value = get_slot(intent, "geolocation", owm_default_geolocation)
    geolocation = raw_geolocation.split(",")

    poi = raw_value.title() if raw_value else "Default Location"

    _LOGGER.info(f"GetTemperature: {poi} ({geolocation})")

    try:
        
        weather = mgr.one_call(lat=float(geolocation[0]), lon=float(geolocation[1]))
        temperature_forecast = weather.forecast_daily[0].temperature('celsius')
        temperature = weather.current.temperature('celsius')

        _LOGGER.info("Temperature: %s", temperature)

        temp_current = round(temperature.get("temp"))
        temp_max = round(temperature_forecast.get("max", -999))
        temp_min = round(temperature_forecast.get("min", -999))
        temp_feels_like = round(temperature.get("feels_like", -999))

        text_temp = f"In {poi} beträgt die Temperatur aktuell {temp_current} °C." if raw_geolocation != owm_default_geolocation else f"Aktuell sind es {temp_current} °C."

        if temp_feels_like != -999 and temp_feels_like != temp_current:
            text_temp += f" Es fühlt sich an wie {temp_feels_like} °C."

        if temp_min != -999 and temp_min != temp_current:
            text_temp += f" Die Tiefsttemperatur beträgt {temp_min} °C."

        if temp_max != -999 and temp_max != temp_current:
            text_temp += f" Die Höchsttemperatur beträgt {temp_max} °C."

        return EndSession(text_temp)
    except PyOWMError as e:
        _LOGGER.exception("Could not get current temperature.", exc_info=e)

    return EndSession(f"Etwas ist schiefgelaufen.")

def relative_date_to_str(relative_date: int) -> str:
    """Convert a relative date to a human readable text."""

    mapping = {
        -2: "vorgestern",
        -1: "gestern",
        0: "heute",
        1: "morgen",
        2: "übermorgen"
    }

    return mapping.get(relative_date, f"vor {relative_date} Tagen" if relative_date < 0 else f"In {relative_date} Tagen")

def relative_time_to_str(relative_time: int) -> str:
    """Convert a relative time to a human readable text."""

    mapping = {
        0: "nacht",
        6: "früh",
        9: "morgen",
        11: "vormittag",
        12: "mittag",
        15: "nachmittag",
        18: "abend",
        22: "spät"
    }

    return mapping.get(relative_time, f"um {relative_time}:00 Uhr")


@app.on_intent("GetWeatherForecast")
async def get_weather_intent(intent: NluIntent):
    """Tell the weather."""

    # In H betr temp momentan 3 bei bew himmel. heute nacht höchstwahrscheinlich regenschauer bei tiefst 1 grad
    # Hier ist der Wetterb für morgen in HE höchstwahr gibt es Schnee bei einer Höchsttemperatur von 4 und Tiefsttemperat von 2
    # Sonntag 1C und wechselnd bewölkt usw...
    # Morgen gibt es in Hamburg vereinzelte Schauer bei Temperaturen zwischen 2 und 4 Grad.
    # Morgen wird es in Berlin schneien bei Temperat...

    # In {poi} beträgt die Temperatur {temp} °C bei {condition}. Heute Nacht höchstwahrscheinlich {condition_forecast_night} bei einer Tiefsttemperatur von {} °C.
    
    # Hier ist der Wetterbericht für 

    raw_geolocation, raw_value = get_slot(intent, "geolocation", owm_default_geolocation)
    geolocation = raw_geolocation.split(",")

    relative_time, _ = get_slot(intent, "relative_time")
    relative_date, _ = get_slot(intent, "relative_date")
    absolute_date, _ = get_slot(intent, "absolute_date")

    poi = raw_value.title() if raw_value else "Default Location"

    _LOGGER.info(f"GetWeatherForecast: {poi} ({geolocation})")

    try:
        
        weather = mgr.one_call(lat=float(geolocation[0]), lon=float(geolocation[1]))

        forecast_data = weather.forecast_daily[0]

        if relative_date:
            rel = int(relative_date)

            if rel < 0:
                return EndSession(random.choice(["Ich kann leider keine historischen Wetterberichte abrufen.", "Historische Wetterberichte werden zurzeit nicht unterstützt.", "Wetterdaten aus der Vergangenheit sind aktuell nicht verfügbar."]))
            elif rel > 6:
                return EndSession(random.choice(["Wetterdaten sind nur bis maximal 7 Tage in der Zukunft verfügbar.", "Der Wetterbericht kann nur für maximal eine Woche im Voraus abgefragt werden."]))

            forecast_data = weather.forecast_daily[rel]


        temperature = forecast_data.temperature('celsius')

        _LOGGER.info("Temperature: %s", temperature)

        condition = forecast_data.detailed_status
        temp_current = round(temperature.get("day"))
        temp_max = round(temperature.get("max", -999))
        temp_min = round(temperature.get("min", -999))
        temp_feels_like = round(temperature.get("feels_like_day", -999))



        is_default_location = raw_geolocation == owm_default_geolocation


        if relative_date:
            poi_data = f" in {poi}" if not is_default_location else ""
            text_temp = f"Wetter {relative_date_to_str(int(relative_date))}{poi_data}: {condition} bei Temperaturen zwischen {temp_min} und {temp_max} Grad."

        else:
            poi_data = f"In {poi} ist es {condition.lower()}" if not is_default_location else condition
            text_temp = f"{poi_data} bei aktuell {temp_current} Grad. Es fühlt sich an wie {temp_feels_like} Grad."

            if temp_min != -999 and temp_min != temp_current:
                text_temp += f" Die Tiefsttemperatur beträgt {temp_min} Grad."

            if temp_max != -999 and temp_max != temp_current:
                text_temp += f" Die Höchsttemperatur beträgt {temp_max} Grad."

        return EndSession(text_temp)
    except PyOWMError as e:
        _LOGGER.exception("Could not get current temperature.", exc_info=e)

    return EndSession(f"Etwas ist schiefgelaufen.")

_LOGGER.info(f"Starting app {app.client_name}.")
app.run()