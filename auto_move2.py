import cv2 as cv
import numpy as np 
import time
import alarmRequests
import CamFunctions
import sys
sys.path.insert(1, '/home/theasis/Desktop/subsense/Python/')
import RunThis

# Camera Initialization
CamFunctions.zoom(3)



#import sys
#sys.path.insert(1, '/home/theasis/software/static_cam/Nikos/tonbo_funk1.tar/tonbo_funk1/cam_funcs/')
#import moveCamera

def checkIfHasStopped():

    isStopped = False

    check1 = CamFunctions.getPanPos()
    time.sleep(0.1)
    check2 = CamFunctions.getPanPos()
    time.sleep(0.1)
    check3 = CamFunctions.getPanPos()

    if (check3 - check2)<=2.0 and (check2 - check1)<=2.0:
        isStopped = True

    return isStopped

# check for fire from drone stream (BGR)
def checkIfFire( frame ):

	thereIsFire = False
	# from BGR 
	red_cnt = 0
	maxRB = 0
	rbInd = [0,0]
	maxRG = 0
	rgInd = [0,0]
	for i in range( frame.shape[0]):
		for j in range( frame.shape[1]):

			if (int(frame[i,j,2]) - int(frame[i,j,0])) > maxRB:
				maxRB = int(frame[i,j,2]) - int(frame[i,j,0])
				rbInd = [i,j]

			if (int(frame[i,j,2]) - int(frame[i,j,1])) > maxRG:
				maxRG = int(frame[i,j,2]) - int(frame[i,j,1])
				rgInd = [i,j]

			#if frame[i,j,0] > 180 and frame[i,j,1] > 200 and frame[i,j,2] == 255:
			if (int(frame[i,j,2]) - int(frame[i,j,1])) > 75 and (int(frame[i,j,2]) - int(frame[i,j,0])) > 115:
				red_cnt += 1

			if red_cnt >= 1:
				thereIsFire = True
				break

	print( "RG diff: " , maxRG)
	print("RG_diff pixels: ", rgInd)
	print( "RB diff: " , maxRB)
	print("RB_diff pixels: ", rbInd)

	return thereIsFire


if __name__ == '__main__':

    # rgb, thermal video captures
    #cam_rgb = cv.VideoCapture("rtsp://192.168.2.233:8554/video0")
    cam_thrm = cv.VideoCapture("rtsp://192.168.2.233:8555/video1")



    prevPanPos = 0.0
    # prevPanPos = moveCamera.getPanPos()
    # flag == 1 move right, flag == 2 move left
    moveFlag = 2
    angle_cnt = 0
    pos_cnt = 0
    droneFlag = 0
    fireCnt = 0
    # list of static camera positions
    #camPositions = [ 0.0, 23.0, 46.0, 69.0, 92.0, 115.0, 138.0]
    camPositions = [ 0.0, 340.0, 320.0, 300.0, 300.0, 320.0, 340.0, 0.0]
    camPos_indx = 0
    
    cam_thrm.set( cv.CAP_PROP_POS_FRAMES, 0)

    
    CamFunctions.setPanPos(camPositions[camPos_indx])

    retThrm, frameThrm = cam_thrm.read()
    #if frameRgb is None:
        #print("\nProblem with the rgb image signal...!\n")
    if frameThrm is None:
        print("\nProblem with the thermal image signal...!\n") 
        
    cnt = 0
    while 1:

        CamFunctions.setPanPos( camPositions[camPos_indx] )
        camPos_indx += 1
        camPos_indx = camPos_indx%8
        #time.sleep(1)
        #CamFunctions.setTiltPos(8)
        time.sleep(3)
        RunThis.main()
        #check if camera has stopped before ask for image signal
        #while not checkIfHasStopped():
            #while False, sleep for 250 milliseconds
            #time.sleep(.250) 

        #read rgb, thermal image
        #cam_rgb.set( cv.CAP_PROP_POS_FRAMES, 0)
        #retRgb, frameRgb = cam_rgb.read()

        #retThrm, frameThrm = cam_thrm.read()
        cnt += 1
        frms = []
                
        #cv.imshow('frame', frame)
        #cv.waitKey(1)


        #move right
        #if abs(50.0 - angle_cnt) <= 2.0 and moveFlag == 1:
            #angle_cnt = 0
            #moveFlag = 1
            #prevPanPos = 138.0 - 23.0
            #CamFunctions.setPanPos(prevPanPos)
            #camPos_indx -= 1
            #CamFunctions.setPanPos(camPositions[camPos_indx])
            #time.sleep(3)
        #move left
        #elif abs( angle_cnt) <= 2.0 and moveFlag == 2:
            #angle_cnt = 0
            #moveFlag = 2
            #prevPanPos = 23.0
            #CamFunctions.setPanPos(prevPanPos)
            #camPos_indx += 1
            #CamFunctions.setPanPos(camPositions[camPos_indx])
            #camPos_indx -= 1
            #CamFunctions.setPanPos(camPositions[camPos_indx])
            #time.sleep(3)
        #move right
        #elif moveFlag == 1:
            #prevPanPos = CamFunctions.getPanPos() - 23.0
            #CamFunctions.setPanPos(prevPanPos)
            #time.sleep(3)
        #move left
        #elif moveFlag == 2:
            #prevPanPos = CamFunctions.getPanPos() + 23.0
            #CamFunctions.setPanPos(prevPanPos)
            #camPos_indx += 1
            #CamFunctions.setPanPos(camPositions[camPos_indx])
            #time.sleep(3)

        #angle_cnt += 23.0
        pos = CamFunctions.getPanPos()
        print('PanPos: ', pos)
        
