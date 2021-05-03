print('Please wait the system is loading...')

import cv2
import time
import threading as th
from online_action import onlineRecognition
from process_image import ProcessImage

######################## Settings ############################

FRAME_SIZE = 720	# Video frame width
MAX_ATTEMPT = 5		# Try to recognize person
blur_level = 300    # Image maximum blur level to send request to recognition server (less value means more blur)
MIN_CONF_LEVEL = 95 # Minimum confidence level to unlock the system
UNLOCK_TIME = 10.0  # System unlock time after recognition successful

##############################################################

AUTHORIZED = False
SKIP = False


def setUnathorized():
	global AUTHORIZED
	AUTHORIZED = False
	print('System locked!')

def skipFrame(skip_time):
	global SKIP
	SKIP = True
	skip = th.Timer(skip_time, unskip)
	skip.start()

def unskip():
	global SKIP
	SKIP = False



class Main:    

	def __init__(self):
		self.process = ProcessImage(MIN_CONF_LEVEL, blur_level, FRAME_SIZE)

	def capture(self):
		global AUTHORIZED
		global SKIP
		attempt = 1
		print('Start video capturing...')
		capture = cv2.VideoCapture("videoplayback.mp4")
		# capture = cv2.VideoCapture(0)
		while True:
			success, frame = capture.read()
			if not success:
				print('End of frame')
				break
			if SKIP:
				continue
			frame = self.process.reshape(frame)     # Resize the source image
			has_face, is_blur = self.process.detectFace(frame)
			if has_face and not is_blur:
				print('[\033[0;36mATTEMPT {}\033[0;0m] Trying to recognize...'.format(attempt))
				faces = onlineRecognition(frame)
				if len(faces['faces']) > 0:
					for face in faces['faces']:
						confidence = "{:.2f}".format(face['top_prediction']['confidence']*100)
						if float(confidence) > MIN_CONF_LEVEL:
							timer = th.Timer(UNLOCK_TIME, setUnathorized)
							AUTHORIZED = True

							# Do somthing after authentication

							print('[\033[1;32mSUCCESS\033[0;0m]({}-{}%) unlocked the system for {}sec'.format(face['top_prediction']['label'], confidence, UNLOCK_TIME))
							timer.start()
							break
						# else:
							# skipFrame(1)
					if not AUTHORIZED:
						attempt += 1
						print('[\033[1;33mFAILED\033[0;0m] {} Unknown face/s detected!'.format(len(faces['faces'])))
						if attempt > MAX_ATTEMPT:
							print('[\033[1;31mUNAUTHORIZED\033[0;0m] Sending message to the admin...')
							# Do something about unauthorized person
			else:
				skipFrame(.1)

			cv2.imshow('Camera Output', frame)
			if cv2.waitKey(1) & 0xFF == ord('q') or attempt > MAX_ATTEMPT or AUTHORIZED:
				print('Stop capturing.')
				break

		capture.release()
		cv2.destroyAllWindows()


	def start(self):
		print('System is ready')
		while True:
			action = int(input('\n1. Start video capture\n2. Exit\n\nChoose: '))
			if action == 1:
				self.capture()
			else:
				print('Exiting the program.')
				break

	def __call__(self):
		self.capture()




if __name__ == "__main__":
	main = Main()
	main.start()

