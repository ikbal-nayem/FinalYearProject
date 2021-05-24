print('Please wait the system is loading...')

import cv2
import time
import threading as th
from online_action import Action
from process_image import ProcessImage

######################## Settings ############################

FRAME_SIZE = 720	# Video frame width
MAX_EMPTY = 20		# Number of frame without any faces to stop capturing video
MAX_ATTEMPT = 5		# Try to recognize person
blur_level = 100    # Image maximum blur level to send request to recognition server (less value means more blur)
MIN_CONF_LEVEL = 95 # Minimum confidence level to unlock the system
UNLOCK_TIME = 10.0  # System unlock time after recognition successful

##############################################################



AUTHORIZED = False

def setUnathorized():
	global AUTHORIZED
	AUTHORIZED = False
	print('System locked!')



class Main:

	def __init__(self):
		self.process = ProcessImage(MIN_CONF_LEVEL, blur_level, FRAME_SIZE)
		self.action = Action()
		self.SKIP = False
		self.attempt = 1
		self.frame_with_no_face = 0


	def skipFrame(self, skip_time):
		self.SKIP = True
		skip = th.Timer(skip_time, self.unskip)
		skip.start()


	def unskip(self): self.SKIP = False


	def checkFaces(self, faces, frame):
		global AUTHORIZED
		for face in faces['faces']:
			confidence = "{:.2f}".format(face['top_prediction']['confidence']*100)
			if float(confidence) > MIN_CONF_LEVEL:
				timer = th.Timer(UNLOCK_TIME, setUnathorized)
				AUTHORIZED = True

				# Do somthing after authentication
				self.action.authorized(frame)

				print('[\033[1;32mSUCCESS\033[0;0m]\033[32m({} {}%) unlocking the system for {} sec\033[0m'.format(face['top_prediction']['label'], confidence, UNLOCK_TIME))
				timer.start()
				break
		if not AUTHORIZED:
			self.attempt += 1
			print('[\033[1;33mFAILED\033[0;0m] {} Unknown face/s detected!'.format(len(faces['faces'])))
			if self.attempt > MAX_ATTEMPT:
				print('[\033[1;31mUNAUTHORIZED\033[0;0m] Sending message to the admin...')
				
				# Do something about unauthorized person
				self.action.unauthorized(frame)


	def capture(self):
		self.attempt = 1
		frame_with_no_face = 0
		print('Start video capturing...')
		capture = cv2.VideoCapture("test_video.mp4")
		# capture = cv2.VideoCapture("http://192.168.31.10:8888")
		while True:
			success, frame = capture.read()
			if not success:
				print('End of frames')
				break
			if self.SKIP: continue
			frame = self.process.reshape(frame)     # Resize the source image
			has_face, is_blur = self.process.detectFace(frame)
			if has_face and not is_blur:
				print('[\033[0;36mATTEMPT {}\033[0;0m] Trying to recognize...'.format(self.attempt))
				faces = self.action.onlineRecognition(frame)
				if len(faces['faces']) > 0:
					self.checkFaces(faces, frame)

			frame_with_no_face = 0 if has_face else frame_with_no_face+1

			self.skipFrame(.5)

			cv2.imshow('Camera Output', frame)
			if cv2.waitKey(1) & 0xFF == ord('q') or self.attempt>MAX_ATTEMPT or AUTHORIZED or frame_with_no_face>MAX_EMPTY:
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

