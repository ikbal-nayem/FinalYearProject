import cv2
# import pyrebase
import requests
import json
# from Messenger import MessageTemplate
from datetime import datetime
# from CONF import auth


# URL = 'http://192.168.31.10:8000'
# URL = 'https://facenet-facerecognition.herokuapp.com'
# URL = 'https://feb5f636-2302-493e-b51a-c153b27177a6.id.repl.co'


# with open('userInfo', 'r') as f:
# 	adminID = f.read()


class OnlineService:
	def __init__(self):
		with open('app-config.json', 'r') as openfile:
			json_object = json.load(openfile)
		self.recognition_server_url = json_object['server_url']
		print("Recognition server address -", self.recognition_server_url)
		self.user_id = json_object['user_id']
	# self.message = MessageTemplate(adminID)
	# firebase = pyrebase.initialize_app(auth.FIREBASE_CONF)
	# self.storage = firebase.storage()
	# self.db = firebase.database()
	# self.listen()

	# def listen(self):
	# 	def stream_handler(msg):
	# 		if msg['event']=='patch':
	# 			print(msg['data'])
	# 			self.db.child(adminID).update({'command': '', 'received': True})
	# 	self.listener = self.db.child(adminID).stream(stream_handler)

	def cv2ToImage(self, frame):
		date = datetime.now()
		image_name = "{}.jpg".format(date.isoformat())
		image = cv2.imencode(".jpg", frame)[1]
		return (image_name, image.tobytes(), 'image/jpeg', {'Expires': '0'})

	# def makeImageURL(self, image):
	# 	img_info = self.storage.child("messenger/images/{}".format(image[0])).put(image[1])
	# 	return self.storage.child(img_info['name']).get_url(img_info['downloadTokens'])

	def recognition(self, frame, notify_admin=False):
		image = self.cv2ToImage(frame)
		file = {"image": image}
		try:
			resp = requests.post(self.recognition_server_url, files=file, data={
		                     "user_id": self.user_id, "notify_admin": notify_admin})
			return resp.json()
		except requests.exceptions.ConnectionError:
			raise Exception("Connecting to {} failed".format(
				self.recognition_server_url))

	# def unauthorized(self, image_frame=None):
	# 	image = self.cv2ToImage(image_frame)
	# 	resp = self.message.genericTemplate(
	# 		title="Attention!",
	# 		subtitle="Unknown person in your doorstep.",
	# 		image_url=self.makeImageURL(image),
	# 		buttons=[{'title': 'Open Door', 'action': 'OPEN'}, {'title': 'Set Alert', 'action': 'ALERT'}]
	# 	)

	# def authorized(self, image_frame=None):
	# 	image = self.cv2ToImage(image_frame)
	# 	resp = self.message.genericTemplate(
	# 		title="Welcome Home!",
	# 		subtitle="Welcome back admin.",
	# 		image_url=self.makeImageURL(image),
	# 		buttons=[{'title': 'Lock The Door', 'action': 'CLOSE'}]
	# 	)
