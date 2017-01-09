import json
import os
import random
from gtts import gTTS


class SpecialQueries():
    def __init__(self):
        with open("resources/special_question_answers.json") as data_file:
            self.qa = json.load(data_file)

    def is_special_query(self, query):
        return self.get_answer(query)

    def process(self, query):
        answer = self.get_answer(query)
        tts = gTTS(text=answer, lang='en')
        tts.save("resources/answer.mp3")
        os.system("mplayer -quiet resources/answer.mp3 >/dev/null 2>&1")

    def get_answer(self, query):
        for q in self.qa:
            questions = q["questions"]
            for ques in questions:
                if ques.lower() == query.lower():
                    return random.choice(q["answers"])

        return None
