import buferlessVideoCapture, TonboCamera, alarmRequests, time, sys, cv2
import numpy as np

def StaticScan():
	camPositions = [43,25,5,25]
	camPos_indx = 0
	CamOptical = buferlessVideoCapture.VideoCapture("rtsp://192.168.2.233:8554/video0")
	Tonbo = TonboCamera.Tonbo(Zoom = 2)
	Tonbo.setTiltPos(4)

	# Start Scanning
	while 1:
		# Move Camera
		Tonbo.setPanPos(camPositions[camPos_indx])
		camPos_indx = (camPos_indx + 1) % len(camPositions)
		time.sleep(.5)
		#Tonbo.setTiltPos(4)
		time.sleep(3)
		
		SmokeDetected, displacement = SmokeDetector(CamOptical = CamOptical, Level = 1)
		if SmokeDetected:
			newPan = (Tonbo.getPanPos() - displacement) % 360
			time.sleep(1)
			Lat, Long = Tonbo.getCoordinates( 1, newPan)
			Tonbo.setPanPos(newPan)
			return True, Lat, Long

	
	# if break while loop
	return False, -1, -1

def SmokeDetector(CamOptical, useThermal , NumFramesPerPosition = int(300 / 5), StaticOpticalThreshold = 1/3,
				NumberExceededThreshold = 100, MaskExclude = 1, Display = False):
		"""
		Function to detect smoke using only optical or both optical and thermal static cameras
		:params	CamOptical: buferlessVideoCapture object to read optical video
				useThermal: If True function uses also thermal camera to distinct Smoke from other moving objects
				NumFramesPerPosition: Number of frames to be processed using frames dropping,  total time = NumFramesPerPosition / SubsenseFPS
				StaticOpticalThreshold: Rate of frames needed for each pixel to be detected as moving object
				NumberExceededThreshold: Number of pixels exceeded StaticOpticalThreshold
				MaskExclude: Image Masking (Size(576,720))
				Display: If True displays moving object detection (Moving Object with Black)
		:return	Detected: True if smoke detected
				displacement: Pan adjustment needed for smoke centering
		"""
		import sys, cv2
		import numpy as np
		sys.path.insert(1, '/home/theasis/Desktop/subsense/Python/')
		import Subsense

		MaskExclude = np.dstack((MaskExclude,MaskExclude,MaskExclude))
		BGS = Subsense.Lobster(lbsp_thresh = .15, num_samples_for_moving_avg = 2, num_bg_samples = 5)
		SumOptical = np.zeros((576, 720))
		for i in range(NumFramesPerPosition):
			FrameOptical = CamOptical.read()
			FrameOptical = FrameOptical * MaskExclude
			FG_Optical=BGS.apply(np.uint8(FrameOptical))

			#if (np.sum(FG_Optical/255) > 0.01*(576*720)):
				#FG_Optical = 0*FG_Optical
			if Display:
				FG_Mask3D = np.dstack((FG_Optical, FG_Optical, FG_Optical)
				cv2.imshow('Optical Mask', (FG_Mask3D == 0) * FrameOptical)
				cv2.waitKey(1)

			SumOptical = SumOptical + FG_Optical / 255

		
		check = np.sum(SumOptical > NumFramesPerPosition * StaticOpticalThreshold)
		if check > NumberExceededThreshold:
			corr = np.median(np.argwhere(SumOptical > NumFramesPerPosition * StaticOpticalThreshold),axis = 0)[1]
			displacement = Tonbo.OPTICALFOV * (corr - Tonbo.OPTICALCPOINT[1])/660 
			print("Smoke.............")
			# Stop Scanning
			return True, displacement

		cv2.destroyAllWindows()
		BGS.release()
		return False, 0


if __name__ == '__main__':
    

	SmokeDetected, Lat, Long = StaticScan()
	if SmokeDetected:
		print(" Smoke Detected.....!!")
		alarmRequests.newAlarm( Lat, Long)
		time.sleep(5)
		
