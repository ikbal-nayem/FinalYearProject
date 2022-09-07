import cv2
import time
from process_image import ProcessImage
from online_service import OnlineService

VIDEO_CAPTURE = 2
# Image maximum blur level to send request to recognition server (less value means more blur)
BLUR_LEVEL = 110
MAX_ATTEMPT = 3		# Try to recognize person
MAX_FRAME_WITHOUT_FACE = 20		# Try to recognize person


print('Please wait until the system is loading...')

image_process = ProcessImage(BLUR_LEVEL)


def authorized():
  print("Authorized")


def unauthorized():
  print("Unauthorized")


def startCapture():
  print('Start video capturing...')
  service = OnlineService()
  num_of_attempt = 0
  frame_without_face = 0
  capture = cv2.VideoCapture(VIDEO_CAPTURE)
  while num_of_attempt < MAX_ATTEMPT:
    success, frame = capture.read()
    if not success:
      print('Stoped capturing')
      break
    frame = image_process.reshape(frame)
    has_face, is_blur = image_process.detectFace(frame)
    if has_face and not is_blur:
      frame_without_face = 0
      print('[\033[0;36mATTEMPT {}\033[0;0m] Trying to recognize...'.format(
          num_of_attempt+1))
      # cv2.imwrite(f"img{num_of_attempt}.jpg", frame)
      resp = service.recognition(
          frame, notify_admin=(num_of_attempt == MAX_ATTEMPT-1))
      if resp.get('isAuthorized'):
        authorized()
        break
      num_of_attempt += 1
      if num_of_attempt == MAX_ATTEMPT:
        unauthorized()
    else:
      frame_without_face += 1

    if frame_without_face > MAX_FRAME_WITHOUT_FACE:
      break
    time.sleep(0.5)

  print("Stop capturing videos")
  capture.release()


if __name__ == "__main__":
  startCapture()
