import cv2
import requests
import json
from datetime import datetime


class OnlineService:
    def __init__(self):
        self.loadUserInfo()

    def loadUserInfo(self):
        with open('app-config.json', 'r') as openfile:
            json_object = json.load(openfile)
        self.recognition_server_url = json_object['server_url']
        self.user_id = json_object['user_id']
        print("\033[1;33mUser ID -", self.user_id)
        print("Recognition server address -",
              self.recognition_server_url, "\033[0;0m")


    def cv2ToImage(self, frame):
        date = datetime.now()
        image_name = "{}.jpg".format(date.isoformat())
        image = cv2.imencode(".jpg", frame)[1]
        return (image_name, image.tobytes(), 'image/jpeg', {'Expires': '0'})

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
