from gpiozero import Buzzer, DistanceSensor
from time import sleep
import threading


UNLOCK_TIME = 5

# GPIO26 for beep
buzzer = Buzzer(26)
# GPIO17 and GPIO18 for trigger and echo
ultra_sonic = DistanceSensor(
    echo=18, trigger=17, max_distance=1.5, queue_len=1)


class RPiAction:
    def __init__(self):
        self.beep = Beeper()
        self.sonic = ultra_sonic

    def isInDoorStep(self):
        print('Checking doorstep ...')
        return self.sonic.wait_for_in_range()

    def unlockTheDoor(self):
        self.beep.unlock()
        print("Door open")

    def lockTheDoor(self):
        self.beep.lock()
        print("Door closed")


class Beeper:
    def __init__(self):
        self.bz = buzzer

    def single(self):
        self.bz.beep(on_time=0.2, n=1, background=True)

    def lock(self):
        self.bz.beep(on_time=0.1, n=1, background=True)

    def unlock(self):
        self.bz.beep(on_time=0.05, off_time=0.15, n=2, background=True)

    def unAuth(self):
        self.bz.beep(on_time=0.5, off_time=0.3, n=5, background=True)


class Authentication():
    def __init__(self):
        self.action = RPiAction()
        self.isAuthorized = False

    def authorized(self):
        self.isAuthorized = True
        print("\033[92mAccess granted\033[0;0m")
        self.action.unlockTheDoor()
        # threading.Timer(UNLOCK_TIME, self.unauthorized)
        sleep(UNLOCK_TIME)
        self.unauthorized()

    def unauthorized(self):
        self.isAuthorized = False
        self.action.lockTheDoor()

    def setAlarm(self):
        print("\033[0;36mAlarming\033[0;0m")
        self.action.beep.unAuth()


authentication = Authentication()
