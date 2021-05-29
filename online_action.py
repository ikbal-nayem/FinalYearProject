import cv2
import pyrebase
import requests
from Messenger import MessageTemplate
from datetime import datetime
from RPi_Action import RPi_Action
from CONF import auth


# URL = 'http://192.168.31.10:8000'
URL = 'https://facenet-facerecognition.herokuapp.com'



class Action:
	def __init__(self):
		self.message = MessageTemplate()
		self.recognition_server = URL
		firebase = pyrebase.initialize_app(auth.FIREBASE_CONF)
		self.storage = firebase.storage()
		self.rasp_pi = RPi_Action()


	def cv2ToImage(self, frame):
		date = datetime.now()
		image_name = "{}.jpg".format(date.isoformat())
		image = cv2.imencode(".jpg", frame)[1]
		return (image_name, image.tobytes(), 'image/jpeg', {'Expires': '0'})

	def makeImageURL(self, image):
		img_info = self.storage.child("messenger/images/{}".format(image[0])).put(image[1])
		return self.storage.child(img_info['name']).get_url(img_info['downloadTokens'])

	def onlineRecognition(self, frame):
		image = self.cv2ToImage(frame)
		file = {"image": image}
		resp = requests.post('{}/recognize'.format(self.recognition_server), files=file)
		return resp.json()

	def unauthorized(self, image_frame=None):
		self.rasp_pi.beep.unAuth()
		image = self.cv2ToImage(image_frame)
		resp = self.message.genericTemplate(
			title="Attention!",
			subtitle="Unknown person in your doorstep.",
			image_url=self.makeImageURL(image),
			buttons=[{'title': 'Open Door'}, {'title': 'Set Alert'}]
		)

	def authorized(self, image_frame=None):
		image = self.cv2ToImage(image_frame)
		resp = self.message.genericTemplate(
			title="Welcome Home!",
			subtitle="Welcome back admin.",
			image_url=self.makeImageURL(image),
			buttons=[{'title': 'Lock The Door'}]
		)
