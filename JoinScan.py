import buferlessVideoCapture, TonboCamera, alarmRequests, time, sys, cv2
import numpy as np
sys.path.insert(1, '/home/theasis/Desktop/subsense/Python/')
import Subsense
from ScanSmoke import SmokeDetector
from ScanFire import * 



def JoinScan(NumFramesPerPositionThermal = 50, NumFramesPerPositionOptical = int(300 / 5)):
	"""
	Function to scann jointly for Fire and Smoke using optical and thermal static camera
	Scanning Strategy: Check for fire for every position using thermal camera, check for smoke every 5 positions. 
	If Fire Detected --> Alarm
	If Smoke Detected--> smoke centering and check again using Zoom
	params:	NumFramesPerPositionThermal: Frames needed for FireDetector
			NumFramesPerPositionOptical: Frames needed for SmokeDetector
	return:	Detected: True if fire or smoke detected
			Lat, Long: Coordinates of Detection
			Type: Smoke or Fire
	"""
	p1 = list(range(280, 360 + 55 + 1, 5)) + list(range(360 + 50, 275 - 1, -5))
	camPositions = [x % 360 for x in p1]
	camPos_indx = 0

	
	CamThermal = buferlessVideoCapture.VideoCapture("rtsp://192.168.2.233:8555/video1")
	CamOptical = buferlessVideoCapture.VideoCapture("rtsp://192.168.2.233:8554/video0")

	Tonbo = TonboCamera.Tonbo(Zoom = 2, Brightness = 0x7, Gain = 0x16)
	Tonbo.setTiltPos(4)

	while 1:
		Tonbo.setPanPos(camPositions[camPos_indx])
		camPos_indx = (camPos_indx + 1) % len(camPositions)
		time.sleep(1)

		FireDetected, displacement =  FireDetector(CamThermal, NumFramesPerPosition = NumFramesPerPositionThermal)
		if FireDetected:
			newPan = (Tonbo.getPanPos() - displacement) % 360
			time.sleep(1)
			Lat, Long = Tonbo.getCoordinates( 1, newPan)
			Tonbo.setPanPos(newPan)
			return True, Lat, Long, "Fire"
		
		if camPos_indx % 5 == 0:
			SmokeDetectedL1, displacement = SmokeDetector(CamOptical = CamOptical, Level = 1, NumFramesPerPosition = NumFramesPerPositionOptical)
			if SmokeDetectedL1:
				newPan = (Tonbo.getPanPos() - displacement) % 360
				time.sleep(1)
				Tonbo.setPanPos(newPan)
				Tonbo.setZoom(8)

				SmokeDetectedL2, displacement = SmokeDetector(CamOptical = CamOptical, Level = 2, NumFramesPerPosition = NumFramesPerPositionOptical) 
				if SmokeDetectedL2:
					newPan = (Tonbo.getPanPos() - displacement) % 360
					time.sleep(1)
					Lat, Long = Tonbo.getCoordinates( 1, newPan)
					Tonbo.setPanPos(newPan)
					return True, Lat, Long, "Smoke"
				else:
					Tonbo.setZoom(2)

	CamThermal.release()
	CamOptical.release()
	return False, -1, -1, "None"


	

if __name__ == '__main__':
    
	Detected, Lat, Long, D = JoinScan()

	#if FireDetected and checkIfDroneIsHome():
	if Detected:
		print(D + " Detected...!!!")
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
