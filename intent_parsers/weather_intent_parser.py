from adapt.intent import IntentBuilder
from adapt.engine import IntentDeterminationEngine


class WeatherIntentParser():
    def __init__(self):
        self.engine = IntentDeterminationEngine()
        weather_verbs = [
            "weather",
            "temperature",
            "forecast"
        ]

        for mv in weather_verbs:
            self.engine.register_entity(mv, "WeatherVerb")

        self.engine.register_regex_entity(
            "in\s*(?P<Location>[A-Z][^\s]*\s*?)+.*$"  # NoQA
        )

        weather_intent = IntentBuilder("WeatherIntent")\
            .require("WeatherVerb")\
            .require("Location")\
            .build()

        self.engine.register_intent_parser(weather_intent)

    def parse(self, sentence):
        for intent in self.engine.determine_intent(sentence):
            if intent.get('confidence') > 0:
                return intent
