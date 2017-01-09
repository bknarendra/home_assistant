from adapt.intent import IntentBuilder
from adapt.engine import IntentDeterminationEngine


class SmartHomeIntentParser():
    def __init__(self):
        self.engine = IntentDeterminationEngine()
        # smart home intent vocabalory
        switch_tasks_keyword = [
            "switch",
            "turn"
        ]
        for stk in switch_tasks_keyword:
            self.engine.register_entity(stk, "SwitchTasksKeyword")

        on_off_keyword = [
            "on",
            "off"
        ]

        for stk in on_off_keyword:
            self.engine.register_entity(stk, "OnOffKeyword")

        equipment_keyword = [
            "lights",
            "light",
            "fan"
        ]

        for stk in equipment_keyword:
            self.engine.register_entity(stk, "EquipmentKeyword")

        smart_home_intent = IntentBuilder("SmartHomeIntent")\
            .require("SwitchTasksKeyword")\
            .require("OnOffKeyword")\
            .require("EquipmentKeyword")\
            .build()

        self.engine.register_intent_parser(smart_home_intent)

    def parse(self, sentence):
        for intent in self.engine.determine_intent(sentence):
            if intent.get('confidence') > 0:
                return intent
