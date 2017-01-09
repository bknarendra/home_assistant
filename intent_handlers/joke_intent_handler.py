import os
import random
import requests
from bs4 import BeautifulSoup
from gtts import gTTS


class JokeIntentHandler():
    def __init__(self, intent):
        self.intent = intent

    def handle(self):
        joke = self._get_joke()
        print "joke = %s" % (joke)
        tts = gTTS(text=joke, lang='en')
        tts.save("resources/joke.mp3")
        os.system("mplayer -quiet resources/joke.mp3 >/dev/null 2>&1")

    def _get_joke(self):
        page = random.randint(1, 150)
        url = "http://onelinefun.com/"
        if page > 1:
            url = url + "%s/" % (page)
        content = requests.get(url).content

        soup = BeautifulSoup(content)
        jokes = soup.findAll("", {"class": "oneliner"})
        chosen = random.randint(0, len(jokes) - 1)
        return jokes[chosen].findAll("p")[0].text
