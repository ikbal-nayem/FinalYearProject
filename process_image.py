import cv2


class ProcessImage:

	def __init__(self, MIN_CONF_LEVEL, blur_level, FRAME_SIZE=640):
		haar_model = 'haarcascade_frontalface_default.xml'
		self.cascade = cv2.CascadeClassifier(haar_model)
		self.MAX_WIDTH = FRAME_SIZE
		self.MIN_CONF_LEVEL = MIN_CONF_LEVEL
		self.blur_level = blur_level
		self.red = (0, 10, 255)
		self.green = (100, 200, 0)
		self.label_color = (100,0,200)

	def reshape(self, frame):
		try:
			height, width = frame.shape[0], frame.shape[1]
			if height < width and width > self.MAX_WIDTH:
				height = height - int(((width-self.MAX_WIDTH)/width)*height)
				width = self.MAX_WIDTH
			return cv2.resize(frame, (width, height))
		except:
			return frame


	def detectFace(self, frame):
		try:
			rects = self.cascade.detectMultiScale(frame, scaleFactor=1.3, minNeighbors=4, minSize=(100,100))
			is_blur = False
			if len(rects)>0:
				for (x, y, w, h) in rects:
					roi = frame[y+30:y+h-30, x+30:x+w-30]
					laplacian = cv2.Laplacian(roi, cv2.CV_64F).var()
					is_blur = True if laplacian<self.blur_level else False
					if not is_blur:
						break
			return True if len(rects)>0 else False, is_blur
		except:
			return False, False


	def drawRectangleAndLabel(self, frame, faces):
		for face in faces['faces']:
			confidence = "{:.2f}".format(face['top_prediction']['confidence']*100)
			top = int(face['bounding_box']['top'])
			bottom = int(face['bounding_box']['bottom'])
			left = int(face['bounding_box']['left'])
			right = int(face['bounding_box']['right'])
			cv2.rectangle(frame, (left, top), (right, bottom), self.green if float(confidence)>self.MIN_CONF_LEVEL else self.red , 1)
			face_label = "{} ({})".format(face['top_prediction']['label'], confidence) if float(confidence)>self.MIN_CONF_LEVEL else "?"
			cv2.putText(frame, face_label, (left, top), cv2.LINE_AA, .5, self.label_color, 2)

