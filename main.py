import speech_recognition as sr
import snowboydecoder
from gtts import gTTS
import os
import time
from processor import Processor


class SmartAssitant():

    def __init__(self):
        self.detector = None
        self.processor = Processor()

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
            self.processor.process(string)
        except Exception as e:
            print(e)
            self.speak("Sorry, I could not understand that")

        time.sleep(1)
        self.start_hotword_detection()

    def stop_music_callback(self):
        self.processor.process("stop the music")

    def start_hotword_detection(self):
        self.detector = snowboydecoder.HotwordDetector(
            ["resources/Alice.pmdl", "resources/stop_the_music.pmdl"],
            sensitivity=[0.45, 0.50],
            audio_gain=3
        )
        self.detector.start([self.detected_callback, self.stop_music_callback])

smart_assitant = SmartAssitant()
smart_assitant.start_hotword_detection()


# def detect_with_wit_ai():
#     print("uploading to wit for recognition")
#     wav_data = audio.get_wav_data(
#         convert_rate=None if audio.sample_rate >= 8000 else 8000,
#         convert_width=2
#     )
#     url = "https://api.wit.ai/speech?v=20160526"
#     request = Request(
#         url,
#         data=wav_data,
#         headers={
#             "Authorization": "Bearer {0}".format(WIT_AI_KEY),
#             "Content-Type": "audio/wav"
#         }
#     )
#     try:
#         response = urlopen(request)
#     except Exception as e:
#         print(e)
#         speak("Sorry, I could not understand that")

#     print("processing response")
#     response_text = response.read().decode("utf-8")
#     result = json.loads(response_text)
#     entites = result['entities']
#     if "on_off" in entites:
#         new_state = entites['on_off'][0]['value']
#         entity = entites['object'][0]['value']
#         turn_on_off(new_state, entity)
#     elif "intent" in entites:
#         intent = entites["intent"]
#         if intent['value'] == 'play':
#             pass
#     else:
#         speak("Sorry, I could not understand that")
