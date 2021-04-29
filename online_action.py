import cv2
import requests


# URL = 'http://192.168.31.10:8000'
URL = 'https://facenet-facerecognition.herokuapp.com'
# URL = 'https://ikbal-nayem-facerecognition.zeet.app'

def onlineRecognition(frame):
	image = cv2.imencode(".jpg", frame)[1]
	file = {"image": ("image.jpg", image.tobytes(), 'image/jpeg', {'Expires': '0'})}
	resp = requests.post(f'{URL}/recognize', files=file)
	return(resp.json())