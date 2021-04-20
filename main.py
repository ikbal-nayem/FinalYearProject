import cv2
import os, time
import threading as th
from online_action import onlineRecognition
from process_image import ProcessImage



MIN_CONF_LEVEL = 80

AUTHORIZED = False
SKIP = False


def setUnathorized():
    global AUTHORIZED
    AUTHORIZED = False
    print('System locked!')

def unskip():
    global SKIP
    SKIP = False



class Main:    
    def __init__(self):
        # self.process = ProcessImage(MIN_CONF_LEVEL)
        self.pTime = 0

    def FPS(self, frame):
        cTime = time.time()
        fps = "FPS: {:.2f}".format(1/(cTime-self.pTime))
        self.pTime = cTime
        cv2.putText(frame, fps, (40, 40), cv2.LINE_AA, .5, (100,100,20), 2)


    def start(self):
        # global AUTHORIZED
        # global SKIP
        print('Start video capturing...')
        capture = cv2.VideoCapture("test_video.mp4")
        # capture = cv2.VideoCapture(0)
        while True:
            check, frame = capture.read()
            # frame = cv2.resize(frame, (640, 480))
            # has_face = self.process.detectFace(frame)
            # if has_face and not AUTHORIZED  and not SKIP:
            #     faces = onlineRecognition(frame)
            #     if len(faces['faces']) > 0:
            #         for face in faces['faces']:
            #             confidence = "{:.2f}".format(face['top_prediction']['confidence']*100)
            #             if float(confidence) > MIN_CONF_LEVEL:
            #                 timer = th.Timer(10.0, setUnathorized)
            #                 AUTHORIZED = True

            #                 # Do somthing after authentication

            #                 print('({})[{}] unlocking the system'.format(face['top_prediction']['label'], confidence))
            #                 timer.start()
            #             else:
            #                 SKIP = True
            #                 skip = th.Timer(0.5, unskip)
            #                 skip.start()
            #         # self.process.drawRectangleAndLabel(frame, faces)
            self.FPS(frame)     # Draw FPS

            cv2.imshow('Camera Output', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
              break

        capture.release()
        cv2.destroyAllWindows()

    def __call__(self):
        self.start()


if __name__ == "__main__":
    print('Initializing tools...', end="")
    main = Main()
    print('Done')
    main()