from adapt.intent import IntentBuilder
from adapt.engine import IntentDeterminationEngine


class JokeIntentParser():
    def __init__(self):
        self.engine = IntentDeterminationEngine()
        joke_verbs = [
            "tell",
            "crack"
        ]
        for mv in joke_verbs:
            self.engine.register_entity(mv, "JokeVerb")

        joke_keywords = [
            "joke"
        ]
        for mk in joke_keywords:
            self.engine.register_entity(mk, "JokeKeyword")

        joke_intent = IntentBuilder("JokeIntent")\
            .require("JokeVerb")\
            .optionally("JokeKeyword")\
            .build()

        self.engine.register_intent_parser(joke_intent)

    def parse(self, sentence):
        for intent in self.engine.determine_intent(sentence):
            if intent.get('confidence') > 0:
                return intent
