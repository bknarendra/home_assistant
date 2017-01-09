from my_intent_parser import MyIntentParser
from intent_handler import IntentHandler
from special_queries import SpecialQueries


class Processor(object):
    def __init__(self):
        self.parser = MyIntentParser()
        self.handler = IntentHandler()
        self.special_queries = SpecialQueries()

    def process(self, sentence):
        if self.special_queries.is_special_query(sentence):
            self.special_queries.process(sentence)
            return

        intent = self.parser.parse(sentence)
        if not intent and "intent_type" not in intent:
            raise Exception("intent_not_parsed")

        return self.handler.handle(intent)
