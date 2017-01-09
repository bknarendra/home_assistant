import sys
import inspect
from intent_parsers import *  # NoQA


class MyIntentParser():
    def __init__(self):
        parsers = [c[1] for c in inspect.getmembers(sys.modules["intent_parsers"], inspect.isclass)]  # NoQA
        self.parser_objs = []
        for o in parsers:
            self.parser_objs.append(o())

    def parse(self, sentence):
        for o in self.parser_objs:
            result = o.parse(sentence)
            if result is not None:
                return result
