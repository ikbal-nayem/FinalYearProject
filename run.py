import cv2
from process_image import ProcessImage
from online_service import OnlineService

VIDEO_CAPTURE = 0
# Image maximum blur level to send request to recognition server (less value means more blur)
BLUR_LEVEL = 150
MAX_ATTEMPT = 5		# Try to recognize person


print('Please wait until the system is loading...')

image_process = ProcessImage(BLUR_LEVEL)


async def authorized():
  print("Authorized")


async def unauthorized():
  print("Unauthorized")


def startCapture():
  print('Start video capturing...')
  service = OnlineService()
  num_of_attempt = 0
  capture = cv2.VideoCapture(VIDEO_CAPTURE)
  while num_of_attempt < MAX_ATTEMPT:
    success, frame = capture.read()
    if not success:
      print('Stop video capturing')
      break
    frame = image_process.reshape(frame)
    has_face, is_blur = image_process.detectFace(frame)
    if has_face and not is_blur:
      print('[\033[0;36mATTEMPT {}\033[0;0m] Trying to recognize...'.format(
          num_of_attempt))
      resp = service.recognition(
          frame, notify_admin=(num_of_attempt == MAX_ATTEMPT-1))
      if not resp['isAuthorized']:
        num_of_attempt += 1
        continue
      authorized()
      return
    unauthorized()


if __name__ == "__main__":
  startCapture()
