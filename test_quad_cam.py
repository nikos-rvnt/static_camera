
import cv2 as cv
import numpy as np


if __name__ == '__main__':

        #quad_cam = cv.VideoCapture('rtmp://127.0.0.1:1935/live/quad')
        quad_cam = cv.VideoCapture('rtsp://192.168.2.233:8554/video0')
        
        retQ, frameQ = quad_cam.read()
        if not retQ:
            print('\nNo image signal !\n')
    
        while retQ:
            
            retQ, frameQ = quad_cam.read()
            cv.imshow('frame', frameQ)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        quad_cam.release()
        cv.destroyAllWindows()
