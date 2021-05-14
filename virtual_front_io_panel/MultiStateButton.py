from enum import Enum
from datetime import datetime

class MultiStateButton:
    was_pressed_timestamp = None

    class PressEvent(Enum):
        SHORT_PRESS = 1
        LONG_PRESS = 2
        SUPER_LONG_PRESS = 3

    # Minimum amount of time for this event to be triggered in seconds
    PressTime = {
        PressEvent.SHORT_PRESS: 0,
        PressEvent.LONG_PRESS: 1.5,
        PressEvent.SUPER_LONG_PRESS: 5
    }

    def __init__(self, gpioController, gpioPort):
        super(MultiStateButton, self).__init__()
        self.gpioController = gpioController
        self.gpioPort = gpioPort
        gpioController.set_direction((1 << gpioPort), 0)

    # GPIO is normally high
    def isPressed(self):
        return not bool(self.gpioController.read() & (1 << self.gpioPort))

    def getState(self):
        if self.isPressed() and self.was_pressed_timestamp is None:
            # First time that button was pressed
            self.was_pressed_timestamp = datetime.now()
            return False
        elif not self.isPressed() and self.was_pressed_timestamp is not None:
            time_pressed = (datetime.now() - self.was_pressed_timestamp).total_seconds()
            self.was_pressed_timestamp = None

            # Check which event matches the time pressed
            # Checking from largest to smallest minimum press time
            for event in reversed(self.PressEvent):
                if time_pressed >= self.PressTime[event]:
                    return event
            return self.PressEvent.SHORT_PRESS
        else:
            return False
