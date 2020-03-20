import buferlessVideoCapture
import cv2 as cv
import numpy as np
import time
import TonboCamera
import alarmRequests
#import coordError

def StaticScan():

	p1 = list(range(280, 360 + 55 + 1, 5)) + list(range(360 + 50, 275 - 1, -5))
	camPositions = [x % 360 for x in p1]
	camPos_indx = 0
	CamThermal = buferlessVideoCapture.VideoCapture("rtsp://192.168.2.233:8555/video1")
	Tonbo = TonboCamera.Tonbo(Zoom = 7, Brightness = 0x7, Gain = 0x16)
	print("Number Of Positions " + str(len(camPositions)/2))
	Tonbo.setTiltPos(4.5)
	# Scan
	while 1:
		
		Tonbo.setPanPos(camPositions[camPos_indx])
		print(camPos_indx)
		print(camPositions[camPos_indx])
		print("\n")
		camPos_indx = (camPos_indx + 1) % len(camPositions)
		time.sleep(1)
		#Tonbo.setTiltPos(4.5)
		#time.sleep(1)
		FireDetected, displacement = FireDetector(CamThermal)
		if FireDetected:
			# Move Camera In Center of Detection
			newPan = (Tonbo.getPanPos() - displacement) % 360
			time.sleep(1)
			Lat, Long = Tonbo.getCoordinates( 1, newPan)
			Tonbo.setPanPos(newPan)
			return True, Lat, Long

	CamThermal.release()
	# if break while loop
	return False, -1, -1



def FireDetector(CamThermal, NumFramesPerPosition = 50, StaticThermalThreshold = 250,
				 NumberExceededThreshold = 25, MaskExclude = 1, Display = False):
		"""
		Function to detect fire using only thermal camera based on thresholding image's intesity
		:params	CamThermal: buferlessVideoCapture object to read thermal video
				NumFramesPerPosition: Number of frames to be processed
				StaticThermalThreshold: Image intensity needed for each pixel to be detected as fire
				NumberExceededThreshold: Number of pixels exceeded StaticThermalThreshold
				MaskExclude: Image Masking (Size(576,720))
				Display: If True displays thermal image
		:return	Detected: True if fire detected
				displacement: Pan adjustment needed for fire centering
		"""
	import cv2
	MaskExclude = np.dstack((MaskExclude,MaskExclude,MaskExclude))
	for i in range(NumFramesPerPosition):
		frameThrm = CamThermal.read()
		frameThrm = frameThrm * MaskExclude
		check = np.sum(frameThrm[ :, :,0] > StaticThermalThreshold)
		#print(check)
		if Display:
			cv.imshow('Thermal', frameThrm)
			cv.waitKey(1)
		if check > NumberExceededThreshold:
			print("Detected") 
			time.sleep(1)
			# Fire Detected From Thermal Camera
			indcs = np.argwhere(frameThrm[ :, :,0] > StaticThermalThreshold)
			corr = np.median(np.argwhere(indcs),axis = 0)[1]
			displacement = Tonbo.THERMALFOV * (corr - Tonbo.THERMALCPOINT[1])/ 641
			print("Fire.............")
			# Stop Scanning
			return True, displacement
	cv2.destroyAllWindows()
	return False, 0

def UAVScan(RGDiff = 75, FramesCount = 5):
	"""
	Function to detect fire using UAV thermal camera based on thresholding image's intesity
	:params	RGDiff: 
			FramesCount:
	:return	Detected: True if fire detected
			latQuad, longQuad : Coordinates of fire detection
	"""
	cam_quad = cv.VideoCapture("rtmp://127.0.0.1:1935/live/quad")
	cntDetected = 0
	while 1:
		
		retQuad, frmQuad = cam_quad.read()
		if not retQuad:
			continue
        
		qq = (np.sum((frmQuad[:,:,2].astype(int)-frmQuad[:,:,1].astype(int))>RGDiff))
		if qq:
			cntDetected +=1
		
		if cntDetected > FramesCount:
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
    
	FireDetected, Lat, Long = StaticScan()

	#if FireDetected and checkIfDroneIsHome():
	if FireDetected:
		#return 0
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


