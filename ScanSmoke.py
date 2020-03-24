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
		
		SmokeDetected, corr = SmokeDetector(CamObjects = (CamOptical,), Level = 1, Display = True)
		if SmokeDetected:
			displacement = Tonbo.OPTICALFOV[2][1] * (corr - Tonbo.OPTICALCPOINT[2][1])/660 
			newPan = (Tonbo.getPanPos() - displacement) % 360
			time.sleep(1)
			Lat, Long = Tonbo.getCoordinates( 1, newPan)
			Tonbo.setPanPos(newPan)
			return True, Lat, Long

	
	# if break while loop
	return False, -1, -1

def SmokeDetector(CamObjects, Level , NumFramesPerPosition = int(300 / 5), StaticOpticalThreshold = 1/3,
				NumberExceededThreshold = 100, MaskExclude = 1, Display = False):
		"""
		Function to detect smoke using only optical or both optical and thermal static cameras
		:params	CamObjects: buferlessVideoCapture object to read optical and Thermal (if Level == 2) video
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
		if Level == 1:
			BGS_Optical = Subsense.Lobster(lbsp_thresh = .15, num_samples_for_moving_avg = 2, num_bg_samples = 5)
			CamOptical, = CamObjects
		elif Level == 2:
			BGS_Optical = Subsense.Lobster(lbsp_thresh = .15, num_samples_for_moving_avg = 2, num_bg_samples = 5)
			BGS_Thermal = Subsense.Lobster(lbsp_thresh = .05, num_samples_for_moving_avg = 2, min_color_dist_thresh = 10)
			CamOptical, CamThermal = CamObjects
			kernel = np.ones((40,30),np.uint8)
			T = np.float32([[0.9557, 0.0369, -1.4987], [-0.0235, 0.8806, 44.2869]])
		
		SumThermal = np.zeros((576,720))
		SumOptical = np.zeros((576, 720))
		for i in range(NumFramesPerPosition):
			# Optical Foreground
			FrameOptical = CamOptical.read()
			FrameOptical = FrameOptical * MaskExclude
			FG_Optical = BGS_Optical.apply(np.uint8(FrameOptical))

			# Thermal Foreground
			if Level == 2:
				FrameThermal = CamThermal.read()
				FG_Thermal = BGS_Thermal.apply(np.uint8(FrameThermal))
				FG_Optical = cv2.warpAffine(FG_Optical, T,(720,576))
				SumThermal = SumThermal + cv2.dilate(FG_Thermal, kernel,iterations = 1) / 255
			
			SumOptical = SumOptical + FG_Optical / 255
			
			if Display:
				FG_Mask3D = np.dstack((FG_Optical, FG_Optical, FG_Optical))
				cv2.imshow('Optical Mask', np.uint8((FG_Mask3D == 0) * FrameOptical))
				cv2.waitKey(1)
				if Level == 2:
					FG_Mask3D = np.dstack((FG_Thermal, FG_Thermal, FG_Thermal))
					cv2.imshow('Thermal Mask', np.uint8((FG_Mask3D == 0) * FrameThermal))
					cv2.waitKey(1)
	
		check = np.sum((SumOptical - SumThermal) > NumFramesPerPosition * StaticOpticalThreshold)		
		
		if check > NumberExceededThreshold:
			corr = np.median(np.argwhere(SumOptical > NumFramesPerPosition * StaticOpticalThreshold),axis = 0)[1]
			print("Smoke.............")
			# Stop Scanning
			return True, corr

		cv2.destroyAllWindows()
		BGS_Optical.release()
		if Level == 2:
			BGS_Thermal.release()
		return False, 0


if __name__ == '__main__':
    
	SmokeDetected, Lat, Long = StaticScan()
	if SmokeDetected:
		print(" Smoke Detected.....!!")
		alarmRequests.newAlarm( Lat, Long)
		time.sleep(5)
		

#if (np.sum(FG_Optical/255) > 0.01*(576*720)):
				#FG_Optical = 0*FG_Optical
