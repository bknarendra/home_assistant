import os
import re
import requests
import json
import time
from bs4 import BeautifulSoup
from gtts import gTTS


class WeatherIntentHandler():
    def __init__(self, intent):
        self.intent = intent
        self.location = intent["Location"]

    def handle(self):
        weather = self._get_weather_data()
        tts = gTTS(text=weather, lang='en')
        tts.save("resources/weather.mp3")
        os.system("mplayer -quiet resources/weather.mp3 >/dev/null 2>&1")

    def _get_weather_data(self):
        location = self.location
        api_url = "http://api.wunderground.com"
        location = location
        autocomplete_url = "http://autocomplete.wunderground.com/aq?cb=j&query=%s&h=1&ski=1&features=1&_=%s" % (location, int(time.time() * 1000))  # NoQA
        b = requests.get(autocomplete_url).content
        json_str = re.sub(
            r"\)(?=[^)]*$).*",
            '',
            re.sub(
                r"\s*[a-zA-Z0-9_]\s*\(",
                '',
                b
            )
        )
        location_weather_url = json.loads(json_str)["RESULTS"][0]['l']
        data = requests.get(api_url + location_weather_url).content
        soup = BeautifulSoup(data, "lxml")
        weather = "Current condition is %s" % (
            soup.find("", {"id": "curCond"}).text
        )
        weather = weather + ", and temperature is %s " % (
            soup.find("", {"id": "curTemp"}).text.strip().replace("\n", " ")
        )
        return weather
