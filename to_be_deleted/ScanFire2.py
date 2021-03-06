
import cv2 as cv
import numpy as np
import time
import TonboCamera
import alarmRequests
import coordError

def StaticScan():

	camPositions = list(range( 52, 0,-5)) + list(range(360-5,280,-5)) + list(range(285,360,5)) + list(range(5,52,5))
	camPositions = camPositions = [ camPositions[i]%360 for i in range(len(camPositions)) ]
	camPositions = []
	camPos_indx = 0
	cam_thrm = cv.VideoCapture("rtsp://192.168.2.233:8555/video1")
	#cam_thrm = cv.VideoCapture(0)
	Tonbo = TonboCamera.Tonbo()
	
	NumFramesPerPosition = 300
	# Scan
	while 1:
		
		Tonbo.setPanPos(camPositions[camPos_indx])
		camPos_indx = (camPos_indx + 1) % len(camPositions)
		time.sleep(1)
		Tonbo.setTiltPos(5)
		time.sleep(3)
		
		for i in range(NumFramesPerPosition):
			retThrm, frameThrm = cam_thrm.read()
			check = np.sum(frameThrm[50:500,50:650] > 250)
			
			if check > 15:
				# Fire Detected From Thermal Camera
				#FOVTHERMAL = 10
				#indcs = np.argwhere( frameThrm[frameThrm.shape[0]//2,50:650] > 250 )
				#columnMedian = indcs[indcs.shape[0]//2][0]
				
				#while np.abs(columnMedian[0] - frameThrm.shape[0]//2)>20:
					#if columnMedian[0] - frameThrm.shape[0]//2>0:
						#Tonbo.setTiltPos( Tonbo.getTiltPos() - 1 )
					#else:
						#Tonbo.setTiltPos( Tonbo.getTiltPos() + 1 )
				
				#while np.abs(columnMedian[1] - frameThrm.shape[1]//2)>20:
					#if columnMedian[1] - frameThrm.shape[1]//2>0:
						#Tonbo.setPanPos( (Tonbo.getPanPos() - 1)%360 )
					#else:
						#Tonbo.setPanPos( (Tonbo.getPanPos() + 1)%360 )
				
				#indcs = np.argwhere( frameThrm[frameThrm.shape[0]//2,50:650] > 250 )
				#columnMedian = indcs[indcs.shape[0]//2][0]
				
				#Lat, Long = Tonbo.getCoordinates( 1, (Tonbo.getPanPos() + FOVTHERMAL*(360 - columnMedian)/(670 - 25))%360)
				Lat, Long = Tonbo.getCoordinates( 1, Tonbo.getPanPos())
				print("Fire.............")
				# Stop Scanning
				return True, Lat, Long
	
	cam_thrm.release()
	# if break while loop
	return False, -1, -1


def UAVScan():
	
	cam_quad = cv.VideoCapture("rtmp://127.0.0.1:1935/live/quad")
	cntDetected = 0
	while 1:
		
		retQuad, frmQuad = cam_quad.read()
		qq = (np.sum((frmQuad[:,:,2].astype(int)-frmQuad[:,:,1].astype(int))>75))
		if qq:
			cntDetected +=1
		
		if cntDetected > 0:
			quadCoords = alarmRequests.getQuadCoords()
			latQuad = float(quadCoords[0])
			longQuad = float(quadCoords[1])
			absAltQuad = float(quadCoords[2])
			cv.imwrite( '/home/theasis/software/static_cam/fireFrame.jpg', frmQuad)
			print("Validated...")
			return True, latQuad, longQuad, absAltQuad
	
	cam_quad.release()
	# if break while loop
	return False, -1, -1, -1


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
    

	#while 1:

	#FireDetected, Lat, Long = StaticScan()

	camPositions = list(range( 52, 0,-5)) + list(range(360-5,280,-5)) + list(range(285,360,5)) + list(range(5,52,5))
	camPositions = camPositions = [ camPositions[i]%360 for i in range(len(camPositions)) ]
	camPositions = [31]
	camPos_indx = 0
	cam_thrm = cv.VideoCapture("rtsp://192.168.2.233:8555/video1")
	#cam_thrm = cv.VideoCapture(0)
	Tonbo = TonboCamera.Tonbo()
	
	NumFramesPerPosition = 300
	# Scan
	while 1:
		
		Tonbo.setPanPos(camPositions[camPos_indx])
		camPos_indx = (camPos_indx + 1) % len(camPositions)
		time.sleep(1)
		Tonbo.setTiltPos(6)
		time.sleep(8)
		
		for i in range(NumFramesPerPosition):
			retThrm, frameThrm = cam_thrm.read()
			check = np.sum(frameThrm[50:500,50:650,0] > 110)
			
			if check > 15:
				# Fire Detected From Thermal Camera
				FOVTHERMAL = 10
				indcs = np.argwhere( frameThrm[ 50:500, 50:650,0] > 110 )
				indcs = np.where( frameThrm[ 50:500, 50:650,0] > 110 )
				#indcs = np.argwhere( np.max(frameThrm[ 50:500, 50:650,0]) )
				#indcs = np.argwhere( frameThrm[frameThrm.shape[0]//2,50:650,:] > 170 )
				columnMedian = indcs[0][len(indcs[0])//2]
				
				while np.abs(columnMedian[0] - frameThrm.shape[0]//2)>20:
					print(columnMedian[0] - frameThrm.shape[0]//2)
					print('aaaa')
					if (columnMedian[0] - frameThrm.shape[0]//2)>20:
						print('bbbb')                        
						Tonbo.setTiltPos( Tonbo.getTiltPos() + 2 )
						time.sleep(8)
						retThrm, frameThrm = cam_thrm.read()
						print(retThrm)
						indcs = np.where( frameThrm[ 50:500, 50:650,0] > 110 )
						columnMedian = [0,0]
						columnMedian = indcs[0][len(indcs[0])//2]
						print(columnMedian)
					elif (columnMedian[0] - frameThrm.shape[0]//2)<-20: 
						print('ccc') 
						Tonbo.setTiltPos( Tonbo.getTiltPos() - 2 )  
						time.sleep(8)
						retThrm, frameThrm = cam_thrm.read()
						indcs = np.where( frameThrm[ 50:500, 50:650,0] > 110 )
						columnMedian = [0,0]
						columnMedian = indcs[0][len(indcs[0])//2]
						print(columnMedian)
					else: 
						break
					                    
					#time.sleep(8)
					#retThrm, frameThrm = cam_thrm.read()
					#indcs = np.argwhere( frameThrm[ 50:500, 50:650,0] > 170 )
					#indcs = np.argwhere( np.max(frameThrm[ 50:500, 50:650,:]) )
					#columnMedian = indcs[indcs.shape[0]//2]
					#print(columnMedian)
					time.sleep(2)
					
				
				#while np.abs(columnMedian[1] - frameThrm.shape[1]//2)>20:
					#if columnMedian[1] - frameThrm.shape[1]//2>0:
						#Tonbo.setPanPos( (Tonbo.getPanPos() - 1)%360 )
					#else:
						#Tonbo.setPanPos( (Tonbo.getPanPos() + 1)%360 )
				
				indcs = np.argwhere( frameThrm[frameThrm.shape[0]//2,50:650] > 170 )
				columnMedian = indcs[indcs.shape[0]//2]
				
				#Lat, Long = Tonbo.getCoordinates( 1, (Tonbo.getPanPos() + FOVTHERMAL*(360 - columnMedian)/(670 - 25))%360)
				Lat, Long = Tonbo.getCoordinates( 1, Tonbo.getPanPos())
				print("Fire.............")


	#if FireDetected and checkIfDroneIsHome():
    #if FireDetected:
		#alarmRequests.newAlarm( Lat, Long)
		#time.sleep(5)
		#FireValidated, latQuad, longQuad, absAltQuad = UAVScan()
		#if FireValidated:
			#alarmRequests.validateAlarm( latQuad, longQuad)
			#worstErr = coordError.coordError( absAltQuad, 45*np.pi/180)
			#print("Worst estimated error - X:" + str(worstErr[0]) + " Y: " + str(worstErr[1]))
		#else:
			#print("Not Validated")
		#alarmRequests.deleteAlarm()


