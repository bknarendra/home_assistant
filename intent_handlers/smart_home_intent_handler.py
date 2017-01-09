from util import Util
if Util.is_system_linux():
    from nanpy import ArduinoApi, SerialManager


class SmartHomeIntentHandler():
    EQUIPMENTS = ["light", "fan"]
    EQUIPMENT_TO_PIN_MAP = {
        "fan": 8,
        "lights": 7,
        "light": 7
    }

    def __init__(self, intent):
        self.intent = intent
        if Util.is_system_mac():
            return

        # initialize raspberry pi
        connection = SerialManager(device='/dev/ttyACM0')
        self.arduino_conn = ArduinoApi(connection=connection)
        self.equipment = self.intent["EquipmentKeyword"]
        self.state = self.intent["OnOffKeyword"]

    def get_pin(self):
        return self.EQUIPMENT_TO_PIN_MAP[self.equipment]

    def handle(self):
        print(self.equipment)
        print(self.state)
        if Util.is_system_mac():
            return

        pin = self.get_pin()
        state_to_set = self.arduino_conn.LOW if self.state == "on" else self.arduino_conn.HIGH  # NoQA

        self.arduino_conn.pinMode(pin, self.arduino_conn.OUTPUT)
        self.arduino_conn.digitalWrite(pin, state_to_set)
