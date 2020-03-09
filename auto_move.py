

import cv2 as cv
import numpy as np 
import time
import alarmRequests
import CamFunctions

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
    camPositions = [ 0.0, 23.0, 46.0, 69.0, 92.0, 115.0, 138.0]
    camPositions = [ 50.0, 42.0, 36.0, 28.0, 20.0, 12.0, 4.0, 12.0, 20.0, 28.0, 36.0, 42.0, 50.0]
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
        camPos_indx = camPos_indx%13
        time.sleep(1)
        CamFunctions.setTiltPos(8)
        time.sleep(3)
        
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
        for i in range(100):
            retThrm, frameThrm = cam_thrm.read()
            check = np.sum(frameThrm>200)
            
            
            check = 0
            if (check > 15) or (cnt == 6):
               
               #x_mean = int( np.mean( np.argwhere(frameThrm > 200)[:,1]))
               lati, longi = CamFunctions.sendCoordinates( 1, 0)
               droneFlag = 1
               #alarmRequests.newAlarm( lati, longi)
               #alarmRequests.newAlarm(38.282370,21.790614)
               print("Fire............")
            
        
            #validate fire
            if droneFlag == 1:
                #quadCoords_start = alarmRequests.getQuadCoords()	
                time.sleep(5)
                cam_quad = cv.VideoCapture("rtmp://127.0.0.1:1935/live/quad")
                while 1:

                    fireQCnt = 0
                    fireQ_frame = []

                    #frm = cv.imread('/media/nikos/Data/SFEDA/vids_thermal_drone/0011_cut/' + conts[i])
                    retQuad, frmQuad = cam_quad.read()
                    
                    #if not frmQuad:
                        #print("No image signal from drone")
                        #break
                    
                    isThereFire = checkIfFire( frmQuad)
                    if isThereFire:
                        #fireQ_frame.append(i)
                        fireCnt += 1

                    if fireCnt >= 10:
                        droneFlag = 0
                        #sendAlarm.validateAlarm()
                        print("Validated...")
                    elif fireCnt:
                        droneFlag = 0
                        #sendAlarm.deleteAlarm()
                        print("No fire...")
        
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
        
