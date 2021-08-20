import cv2
import pyrebase
import requests
from Messenger import MessageTemplate
from datetime import datetime
from CONF import auth


# URL = 'http://192.168.31.10:8000'
URL = 'https://facenet-facerecognition.herokuapp.com'
# URL = 'https://feb5f636-2302-493e-b51a-c153b27177a6.id.repl.co'



with open('userInfo', 'r') as f:
	adminID = f.read()


class Action:
	def __init__(self):
		self.message = MessageTemplate(adminID)
		self.recognition_server = URL
		firebase = pyrebase.initialize_app(auth.FIREBASE_CONF)
		self.storage = firebase.storage()
		self.db = firebase.database()
		self.listen()


	def listen(self):
		def stream_handler(msg):
			if msg['event']=='patch':
				print(msg['data'])
				self.db.child(adminID).update({'command': '', 'received': True})
		self.listener = self.db.child(adminID).stream(stream_handler)


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
		image = self.cv2ToImage(image_frame)
		resp = self.message.genericTemplate(
			title="Attention!",
			subtitle="Unknown person in your doorstep.",
			image_url=self.makeImageURL(image),
			buttons=[{'title': 'Open Door', 'action': 'OPEN'}, {'title': 'Set Alert', 'action': 'ALERT'}]
		)

	def authorized(self, image_frame=None):
		image = self.cv2ToImage(image_frame)
		resp = self.message.genericTemplate(
			title="Welcome Home!",
			subtitle="Welcome back admin.",
			image_url=self.makeImageURL(image),
			buttons=[{'title': 'Lock The Door', 'action': 'CLOSE'}]
		)
