import cv2
import os, time


class ProcessImage:
	def __init__(self, MIN_CONF_LEVEL):
		cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))
		haar_model = os.path.join(cv2_base_dir, 'data/haarcascade_frontalface_default.xml')
		self.cascade = cv2.CascadeClassifier(haar_model)
		self.MIN_CONF_LEVEL = MIN_CONF_LEVEL
		self.red = (0, 10, 255)
		self.green = (100, 200, 0)
		self.label_color = (100,0,200)

	def detectFace(self, frame):
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		rects = self.cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=4, minSize=(60,60))
		return True if len(rects)>0 else False

	def drawRectangleAndLabel(self, frame, faces):
		for face in faces['faces']:
			confidence = "{:.2f}".format(face['top_prediction']['confidence']*100)
			top = int(face['bounding_box']['top'])
			bottom = int(face['bounding_box']['bottom'])
			left = int(face['bounding_box']['left'])
			right = int(face['bounding_box']['right'])
			cv2.rectangle(frame, (left, top), (right, bottom), self.green if float(confidence)>self.MIN_CONF_LEVEL else self.red , 1)
			face_label = str(f"{face['top_prediction']['label']} ({confidence})") if float(confidence)>self.MIN_CONF_LEVEL else "?"
			cv2.putText(frame, face_label, (left, top), cv2.LINE_AA, .5, self.label_color, 2)