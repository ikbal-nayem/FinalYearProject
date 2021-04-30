import cv2
import time
import threading as th
from online_action import onlineRecognition
from process_image import ProcessImage

######################## Settings ############################

blur_level = 300    # Image maximum blur level to send request to recognition server (less value means more blur)
MIN_CONF_LEVEL = 95 # Minimum confidence level to unlock the system
UNLOCK_TIME = 10.0  # System unlock time after recognition successful

##############################################################

AUTHORIZED = False
SKIP = False


def setUnathorized():
    global AUTHORIZED
    AUTHORIZED = False
    print('System locked!')

def skipFrame(skip_time):
    global SKIP
    SKIP = True
    skip = th.Timer(skip_time, unskip)
    skip.start()

def unskip():
    global SKIP
    SKIP = False



class Main:    
    def __init__(self):
        self.process = ProcessImage(MIN_CONF_LEVEL, blur_level)
        self.pTime = 0

    def FPS(self, frame):
        cTime = time.time()
        fps = "FPS: {:.2f}".format(1/(cTime-self.pTime))
        self.pTime = cTime
        cv2.putText(frame, fps, (40, 40), cv2.LINE_AA, .5, (100,100,20), 2)


    def start(self):
        global AUTHORIZED
        global SKIP
        print('Start video capturing...')
        capture = cv2.VideoCapture("test_video.mp4")
        # capture = cv2.VideoCapture(0)
        while True:
            check, frame = capture.read()
            if SKIP or AUTHORIZED:
                continue
            frame = self.process.reshape(frame)     # Resize the source image
            has_face, is_blur = self.process.detectFace(frame)
            if has_face and not is_blur:
                print('[Face Found] Sending to the server...', end="")
                faces = onlineRecognition(frame)
                print('Respond')
                if len(faces['faces']) > 0:
                    for face in faces['faces']:
                        confidence = "{:.2f}".format(face['top_prediction']['confidence']*100)
                        if float(confidence) > MIN_CONF_LEVEL:
                            timer = th.Timer(UNLOCK_TIME, setUnathorized)
                            AUTHORIZED = True

                            # Do somthing after authentication

                            print('({})[{}] unlocked the system for {}sec'.format(face['top_prediction']['label'], confidence, UNLOCK_TIME))
                            timer.start()
                        # else:
                        #     skipFrame(1)
                    # self.process.drawRectangleAndLabel(frame, faces)
            else:
                skipFrame(2)
            # self.FPS(frame)     # Draw FPS

            # try:
            #     cv2.imshow('Camera Output', frame)
            # except:
            #     print('End of frame')
            #     break
            if cv2.waitKey(1) & 0xFF == ord('q') or not check:
                print('Bye Bye!')
                break

        capture.release()
        cv2.destroyAllWindows()

    def __call__(self):
        self.start()


if __name__ == "__main__":
    main = Main()
    main()

