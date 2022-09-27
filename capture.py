import cv2
import time
import threading
from process_image import ProcessImage
from online_service import OnlineService
from RPi_Action import authentication, RPiAction

VIDEO_CAPTURE = 0
# Image maximum blur level to send request to recognition server (less value means more blur)
BLUR_LEVEL = 110
MAX_ATTEMPT = 3		# Try to recognize a person
MAX_FRAME_WITHOUT_FACE = 20		# Stop capturing images after n number of empty frame


print('Please wait until the system is loading...')
S_CAP = False

UNA = False

image_process = ProcessImage(BLUR_LEVEL)
service = OnlineService()
rpi = RPiAction()


def setUNA():
    global UNA
    UNA = True
    return

def startCapture():
    print(f'Start video capturing from index {VIDEO_CAPTURE}...')
    global UNA
    num_of_attempt = 0
    frame_without_face = 0
    capture = cv2.VideoCapture(VIDEO_CAPTURE)
    while num_of_attempt < MAX_ATTEMPT and not authentication.isAuthorized:
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
                frame, notify_admin=(num_of_attempt == MAX_ATTEMPT-1), una=UNA)
            if resp.get('isAuthorized'):
                authentication.authorized()
                break
            num_of_attempt += 1
            if num_of_attempt == MAX_ATTEMPT:
                print('\033[91mAccess denied.\033[0;0m')
                authentication.unauthorized()
        else:
            frame_without_face += 1

        if frame_without_face > MAX_FRAME_WITHOUT_FACE:
            print("No faces found!")
            break
        time.sleep(0.7)

    print("Stop capturing video")
    UNA = False
    capture.release()


def cap():
    global S_CAP
    print('Checking doorstep ...')
    S_CAP = True
    rpi.beep.single()
    startCapture()
    S_CAP = False


def lookAtDoorstep():
    while True:
        if rpi.isInDoorStep() and not S_CAP:
            rpi.beep.single()
            startCapture()


# th = threading.Thread(target=lookAtDoorstep)

# if __name__ == "__main__":
#     lookAtDoorstep()
