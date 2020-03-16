import cv2
import time
import matplotlib.pyplot as plt
cam_thrm = cv2.VideoCapture('rtsp://192.168.2.233:8554/video0')



r,f = cam_thrm.read()
plt.imshow(f)
plt.show()
#cv2.waitKey(1)

time.sleep(10)

#plt.imshow(f)
#cv2.waitKey(1)
