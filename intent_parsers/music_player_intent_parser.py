from adapt.intent import IntentBuilder
from adapt.engine import IntentDeterminationEngine


class MusicPlayerIntentParser():
    def __init__(self):
        self.engine = IntentDeterminationEngine()
        # define music vocabulary
        music_verbs = [
            "listen",
            "hear",
            "play",
            "stop"
        ]

        for mv in music_verbs:
            self.engine.register_entity(mv, "MusicVerb")

        music_keywords = [
            "songs",
            "music"
        ]

        for mk in music_keywords:
            self.engine.register_entity(mk, "MusicKeyword")

        self.engine.register_regex_entity(
            "(play|hear|listen|listen to)\s*(the)?\s*(song|album)?\s*(?P<Media>.*)$"  # NoQA
        )

        music_intent = IntentBuilder("MusicIntent")\
            .require("MusicVerb")\
            .optionally("MusicKeyword")\
            .optionally("Media")\
            .build()

        self.engine.register_intent_parser(music_intent)

    def parse(self, sentence):
        for intent in self.engine.determine_intent(sentence):
            if intent.get('confidence') > 0:
                return intent
