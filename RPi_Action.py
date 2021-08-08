from gpiozero import Buzzer



class RPi_Action:
	def __init__(self):
		self.beep = Beeper()
		self.door = Door()

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
		self.bz = Buzzer(3)		# GPIO 3 for beep


	def lock(self):
		self.bz.beep(on_time=0.1, n=1, background=True)

	def unlock(self):
		self.bz.beep(on_time=0.05, off_time=0.15, n=2, background=True)

	def unAuth(self):
		self.bz.beep(on_time=0.5, off_time=0.3, n=3, background=True)