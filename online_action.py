import cv2
import requests

def onlineRecognition(frame):
	image = cv2.imencode(".jpg", frame)[1]
	file = {"image": ("image.jpg", image.tobytes(), 'image/jpeg', {'Expires': '0'})}
	resp = requests.post('http://localhost:8000/recognize', files=file)
	return(resp.json())