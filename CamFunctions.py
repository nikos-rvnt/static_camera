import math
import socket
import time
#import threading
#from multiprocessing import Process

UDP_IP = "192.168.2.233"
UDP_PORT = 5004



def sendToCam(message1):
    message1.append((sum(message1)+1)%256)
    encodedMessage1 = bytes(message1)
    #print(message1)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(encodedMessage1, (UDP_IP, UDP_PORT))
    #print((encodedMessage1))
def querMag():
    import binascii
    
    message2 = [255, 1, 0, 0x61, 0, 0, 0x62]
    encodedMessage2 = bytes(message2)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(encodedMessage2, (UDP_IP, UDP_PORT))
    a = sock.recv(7)
    b = binascii.hexlify(a)
    #print(b)
    Zoom = 0.01*(int(int(b,16)/pow(16,2))%pow(16,4))
    return Zoom


def zoom(comval):
    lsb = int((comval*100)%256)
    msb = int((comval*100)/256)
    sendToCam([255,1,0,0x5F, msb, lsb])
    


def setPanPos(ang):
    lsb = int((ang*100)%256)
    msb = int((ang*100)/256)
    sendToCam([255,1,0,0x4b, msb, lsb])
    

def setTiltPos(ang):
    lsb = int((ang*100)%256)
    msb = int((ang*100)/256)
    sendToCam([0xFF,0x0,0x0,0x4d, msb, lsb])

def setZeroPos():
    sendToCam([0xFF,0x1,0x0,0x49, 0x0, 0x0])

def StopRotation():
    sendToCam([255, 1, 0, 0, 0, 0])

def MoveLeft(speed):
    sendToCam([255, 1, 0, 4, speed, 0])

def MoveRight(speed):
    sendToCam([255, 1, 0, 2, speed, 0])

def MoveDown(speed):
    sendToCam([255, 1, 0, 10, 0, speed])
    
def MoveUp(speed):
    sendToCam([255, 1, 0, 10, 0, speed])
    
def getPanPos():
    import binascii
    
    message2= [255, 1, 0, 0x51, 0, 0, 0x52]
    encodedMessage2 = bytes(message2)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(encodedMessage2, (UDP_IP, UDP_PORT))
    a = sock.recv(7)
    b = binascii.hexlify(a)
    #print(b)
    Pan = 0.01*(int(int(b,16)/pow(16,2))%pow(16,4))
    #print(Pan)
    
    return Pan

def getTiltPos():
    import binascii
    
    message2= [255, 1, 0, 0x53, 0, 0, 0x54]
    encodedMessage2 = bytes(message2)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(encodedMessage2, (UDP_IP, UDP_PORT))
    a = sock.recv(7)
    b = binascii.hexlify(a)
    Tilt = 0.01*(int(int(b,16)/pow(16,2))%pow(16,4))
    #print(Tilt)
    return Tilt

def stopAllAction():
    sendToCam([255,1,0,0, 0, 0])

import requests 

def newAlarm(latitude, longitude):
    URL = "http://localhost:3000/new_alarm"
    PARAMS = {'latitude': latitude, 'longitude': longitude} 
    r = requests.get(url = URL, params = PARAMS) 
    print(r)


def sendCoordinates( D, pixelX):
    import numpy as np
    import math
    
    Pan = getPanPos() #- math.atan( (pixelX - 451.5614)/6077.5 )
    '''
    T = getTiltPos()
    if T > 180:
        Tilt = 90 + (360 - T)
    else:
        Tilt = 90 - T
    '''
    theta = 360 - 219    
    #H = 0.050
    #D = H * np.tan(math.radians(Tilt))
    #D = 0.3
    R = Pan - theta 
    dx = D * np.cos(math.radians(R))
    dy = D * np.sin(math.radians(R))

    latitude = 38.101849
    longitude =  21.345674
    r_earth = 6378

    new_latitude  = latitude  + (dx / r_earth) * (180 / np.pi)
    new_longitude = longitude - (dy / r_earth) * (180 / np.pi) / np.cos(latitude * np.pi/180);
    #print(R)
    
    print("D: " + str(D))

    print("Pan: " + str(Pan))
    #newAlarm( new_latitude, new_longitude)
    
   # print("Dx")
    #print(dx)
    #print("Dy")
   # print(dy)

    print(new_latitude)
    print(new_longitude)
    #new_latitude = 38.100012 
    #new_longitude = 21.353091
    return new_latitude, new_longitude

def EstimateDepth(Yhat):
	import numpy as np
	import math
	
	Beta = 0
	Y2 = 342
	D2 = 1200
	D1 = 600
	Y1 = 291

	# Estimate Parameters
	#Pan = 0
	Lambda = -math.log((Y2-Beta)/(Y1-Beta))/(D2-D1)
	Alpha = (Y1-Beta)/math.exp(-Lambda*D1)

	# Estimate Distance
	D = math.log((Yhat-Beta)/Alpha)/(-Lambda)
	D = D/1000
	return D

def CoordsExp():
    import cv2
    import numpy as np
    import matplotlib.pyplot as plt
    cap = cv2.VideoCapture("rtsp://192.168.2.233:8554/video0")
    ret, frame = cap.read()
    plt.figure()
    plt.imshow(frame)
    plt.show(block=False)
    th = 0.95
    y = np.array([x[0] for x in iter(np.argwhere(frame[:,:,0]>th*255))]).mean()
    s1,_,_ = frame.shape
    D = EstimateDepth(s1-y)
    sendCoordinates(D)
    
def display():
    import cv2
    import numpy as np
    
    cap = cv2.VideoCapture("rtsp://192.168.2.233:8555/video1")

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    #out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 25, (frame_width,frame_height))

    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10,40)
    fontScale = 1
    fontColor = (255,255,255)*0
    lineType = 2
    Pan,Tilt,Zoom = ("0", "0", "0")
    i = 0
    while(True):
        ret, frame = cap.read()
        points = (250,300,350,400,450,500,550)
        for dx in points:
            cv2.line(frame, (0,dx),(720,dx),(255,255,255),3)
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    #out.release()
    cv2.destroyAllWindows()
    
def record(num):
    import cv2
    import numpy as np
    import random
    cap = cv2.VideoCapture("rtsp://192.168.2.233:8554/video0")

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    out = cv2.VideoWriter(str(num)+str(random.randint(0,1000))+'DroneCalibFlight.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 25.0, (frame_width,frame_height))

    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10,40)
    fontScale = 1
    fontColor = (255,255,255)*0
    lineType = 2
    Pan,Tilt,Zoom = ("0", "0", "0")
    i = 0
    while(True):
        ret, frame = cap.read()
        if (i % 100 == 0):
            Pan = str(getPanPos())
            Tilt = str(getTiltPos())
            Zoom = str(querMag())
            
        i = i + 1
        
        cv2.putText(frame,'Pan: ' + Pan + ' Tilt: ' + Tilt + ' Z: ' + Zoom,
                    bottomLeftCornerOfText, font,
                    fontScale, fontColor, lineType)
        #thread.start_new_thread( out.write, (frame,))
        #thread.start_new_thread( cv2.imshow, ('frame', frame, ))
        out.write(frame)
        #cv2.imshow('frame',frame)
        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break
    out.release()
    cap.release()
    cv2.destroyAllWindows()

def bgs():
    import cv2
    import numpy as np
    #cap = cv2.VideoCapture('rtsp://192.168.2.233:8554/video0')
    cap = cv2.VideoCapture('C:/Users/TONBO/Desktop/Recordings/2019/07/05/video1_2019_07_05_11_33_32_e.avi')
    history = 30
    varThreshold = 16
    bShadowDetection = False
    fgbg = cv2.createBackgroundSubtractorMOG2(history, varThreshold, bShadowDetection)

    while(True):
        ret, frame = cap.read()
        fgmask = fgbg.apply(frame, learningRate = 0.001)
        #gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame',fgmask)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()



def imCoords2Angles(x,y):
	a1 = math.atand((x - 315.8608),3.5989)*180/pi
	a2 = math.atand((x - 451.5614),4.2493)*180/pi
	return(a1,a2)
