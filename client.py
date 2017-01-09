import speech_recognition as sr
import snowboydecoder
from gtts import gTTS
import os
import time
import requests
import urllib


class Client():

    def __init__(self):
        self.detector = None
        self.server_url = "http://192.168.0.104:8080"

    def speak(self, str):
        file_path = './resources/%s.wav' % (str.strip().lower().replace(" ", "_"))  # NoQA
        if os.path.isfile(file_path):
            os.system("mplayer %s" % (file_path))
        else:
            tts = gTTS(text=str, lang='en')
            tts.save("resources/temp.mp3")
            # Change this to code to play mp3 on raspberry pi.
            os.system("mplayer -quiet resources/temp.mp3 >/dev/null 2>&1")

    def detected_callback(self):
        self.detector.terminate()
        self.speak("Yes Sir")
        r = sr.Recognizer()
        print("recording...")
        with sr.Microphone() as source:
            audio = r.listen(source)

        try:
            print("sending data to google for recognition")
            string = r.recognize_google(audio)
            print("response from google: " + string)
            self.send_cmd_to_server(string)
        except Exception as e:
            print(e)
            self.speak("Sorry, I could not understand that")

        time.sleep(1)
        self.start_hotword_detection()

    def send_cmd_to_server(self, cmd):
        request_url = "%s/process?%s" % (
            self.server_url,
            urllib.urlencode({"cmd": cmd})
        )
        print("sending request : %s" % (request_url))
        requests.get(request_url, timeout=600)

    def stop_music_callback(self):
        self.send_cmd_to_server("stop the music")

    def start_hotword_detection(self):
        self.detector = snowboydecoder.HotwordDetector(
            ["resources/Alice.pmdl", "resources/stop_the_music.pmdl"],
            sensitivity=[0.45, 0.50],
            audio_gain=3
        )
        self.detector.start([self.detected_callback, self.stop_music_callback])

client = Client()
client.start_hotword_detection()
