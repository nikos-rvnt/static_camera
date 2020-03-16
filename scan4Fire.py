
import cv2 as cv
import numpy as np
import time

import TonboCamera
import alarmRequests
import coordError
from buferlessVideoCapture import VideoCapture 

def StaticScan():

	camPositions = list(range( 52, 0,-5)) + list(range(360-5,280,-5)) + list(range(285,360,5)) + list(range(5,52,5))
	camPositions = camPositions = [ camPositions[i]%360 for i in range(len(camPositions)) ]
	camPositions = [34]
	camPos_indx = 0
	cam_thrm = VideoCapture("rtsp://192.168.2.233:8555/video1")
	#cam_thrm = cv.VideoCapture(0)
	tonby = TonboCamera.Tonbo()
	
	NumFramesPerPosition = 300
	# Scan
	while 1:
		
		tonby.setPanPos(camPositions[camPos_indx])
		camPos_indx = (camPos_indx + 1) % len(camPositions)
		time.sleep(1)
		tonby.setTiltPos(5)
		time.sleep(3)
		
		for i in range(NumFramesPerPosition):
			frameThrm = cam_thrm.read()
			check = np.sum(frameThrm[50:500,50:650] > 240)
			print(check)
			
			if check > 15:
				# Fire Detected From Thermal Camera
				#FOVTHERMAL = 10
				#indcs = np.argwhere( frameThrm[frameThrm.shape[0]//2,50:650] > 250 )
				#pixFireMedian = indcs[indcs.shape[0]//2][0]
				
				#Lat, Long = Tonbo.getCoordinates( 1, (Tonbo.getPanPos() + FOVTHERMAL*(360 - pixFireMedian)/(670 - 25))%360)
				
				indcs = np.argwhere( frameThrm[ :, :,0] > 55 )
				pixFireMedian = [indcs[len(indcs)//2][0],indcs[len(indcs)//2][1]]
				
				while np.abs(pixFireMedian[0] - 288)>15 and np.abs(pixFireMedian[1] - frameThrm.shape[1])>15:
					           
					print("\nDifference from central row: ", pixFireMedian[0] - frameThrm.shape[0]//2)
					print("\nDifference from central column: ", pixFireMedian[0] - frameThrm.shape[0]//2)
					print("\nCentral Fire pixel: ", pixFireMedian)
                    
					frameThrm = cam_thrm.read()
					indcs = np.argwhere( frameThrm[ :, :,0] > 55 )
					pixFireMedian = [indcs[len(indcs)//2][0],indcs[len(indcs)//2][1]]
					                    
					# check if central fire pixel is under the central row
					if (pixFireMedian[0] - 288)>15 :
                                       
						currentTilt = tonby.getTiltPos()
						tonby.setTiltPos( currentTilt + .5 )
						time.sleep(.05)
						
					# check if central fire pixel is over the central row
					elif (pixFireMedian[0] - 288)<-15 : 
					                         
						currentTilt = tonby.getTiltPos()
						tonby.setTiltPos( currentTilt - .5 )  
						time.sleep(.05)
					                    
 					# check if central fire pixel is right of the central row
					if (pixFireMedian[1] - frameThrm.shape[1]//2)>15 :
					                                       
						currentPan = tonby.getPanPos()
						tonby.setPanPos( currentPan - .5 )
						time.sleep(.05)
						
					# check if central fire pixel is left of the central row
					elif (pixFireMedian[1] - frameThrm.shape[1]//2)<-15 : 
						
						currentPan = tonby.getPanPos()
						tonby.setPanPos( currentPan + .5 )  
						time.sleep(.05)
						                                     
					tonby.stopAllAction()
				
				Lat, Long = tonby.getCoordinates( 1, tonby.getPanPos())
				print("Fire.............")
				# Stop Scanning
				return True, Lat, Long
	
	cam_thrm.release()
	# if break while loop
	return False, -1, -1


def UAVScan():
	
	cam_quad = VideoCapture("rtmp://127.0.0.1:1935/live/quad")
	cntDetected = 0
	while 1:
		
		frmQuad = cam_quad.read()
		qq = (np.sum((frmQuad[:,:,2].astype(int)-frmQuad[:,:,1].astype(int))>75))
		if qq:
			cntDetected +=1
		
		if cntDetected > 0:
			quadCoords = alarmRequests.getQuadCoords()
			latQuad = float(quadCoords[0])
			longQuad = float(quadCoords[1])
			#absAltQuad = float(quadCoords[2])
			cv.imwrite( '/home/theasis/software/static_cam/fireFrame.jpg', frmQuad)
			print("Validated...")
			return True, latQuad, longQuad
	
	cam_quad.release()
	# if break while loop
	return False, -1, -1


def checkIfDroneIsHome():

	droneHomeCoords = [ 38.123456, 21.567890]
	#isDroneHome = True

	droneCurrentCoords = alarmRequests.getQuadCoords()
	droneCurrentCoords[0] = float(droneCurrentCoords[0])
	droneCurrentCoords[1] = float(droneCurrentCoords[1])
	droneCurrentCoords[2] = float(droneCurrentCoords[2])
	if np.abs(droneHomeCoords[0] - droneCurrentCoords[0])<0.00001 and np.abs(droneHomeCoords[1] - droneCurrentCoords[1])<0.00001:
		isDroneHome = True
	else:  
		isDroneHome = False

	return isDroneHome



if __name__ == '__main__':
    

	while 1:

		FireDetected, Lat, Long = StaticScan()

		#if FireDetected and checkIfDroneIsHome():
		if FireDetected:
			alarmRequests.newAlarm( Lat, Long)
			time.sleep(5)
			FireValidated, latQuad, longQuad = UAVScan()
			if FireValidated:
				alarmRequests.validateAlarm( latQuad, longQuad)
				#worstErr = coordError.coordError( 60, 45*np.pi/180)
				#print("Worst estimated error - X:" + str(worstErr[0]) + " Y: " + str(worstErr[1]))
			else:
				print("Not Validated")
			alarmRequests.deleteAlarm()


