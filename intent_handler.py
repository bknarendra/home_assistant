import sys
import inspect
from intent_handlers import *  # NoQA


class IntentHandler():

    def __init__(self):
        self.handlers = [c[1] for c in inspect.getmembers(sys.modules["intent_handlers"], inspect.isclass)]  # NoQA

    def handle(self, intent):
        handler_name = intent['intent_type'] + "Handler"
        for h in self.handlers:
            if h.__name__ == handler_name:
                return h(intent).handle()

        raise Exception("intent_not_handled")
