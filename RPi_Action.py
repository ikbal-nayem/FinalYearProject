from gpiozero import Buzzer, DistanceSensor
from time import sleep


# GPIO26 for beep
buzzer = Buzzer(26)
# GPIO17 and GPIO18 for trigger and echo
ultra_sonic = DistanceSensor(echo=18, trigger=17, max_distance=1.4, queue_len=1)


class RPi_Action:
	def __init__(self):
		self.beep = Beeper()
		self.door = Door()
		self.check_range = DistanceMeasure()

	def unlockTheDoor(self):
		self.beep.unlock()

	def lockTheDoor(self):
		self.beep.lock()




class Door:
	def open(self):
		pass
	def close(self):
		pass




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
		self.bz.beep(on_time=0.5, off_time=0.3, n=3, background=True)




class DistanceMeasure:
	def __init__(self):
		self.sensor = ultra_sonic

	def start(self):
		return self.sensor.wait_for_in_range()




# def start(t):
# 	for i in range(t):
# 		print(sensore.distance*100)
# 		sleep(1)