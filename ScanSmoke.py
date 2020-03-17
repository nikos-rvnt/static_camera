import buferlessVideoCapture TonboCamera, alarmRequests, coordError, time
import numpy as np
sys.path.insert(1, '/home/theasis/Desktop/subsense/Python/')
import Subsense


def StaticScan():

	camPositions = [34]
	camPos_indx = 0
	cam_optical = buferlessVideoCapture.VideoCapture("rtsp://192.168.2.233:8554/video0")
	Tonbo = TonboCamera.Tonbo(Brightness = 7, Gain = 10)
	Tonbo.setZoom(2)
	
	MaskExclude = np.zeros((576,720,3))
	MaskExclude[50:-50,50:-50,:] = 1

	NumFramesPerPosition = 300 / 5
	# Scan
	while 1:
		# Move Camera
		Tonbo.setPanPos(camPositions[camPos_indx])
		camPos_indx = (camPos_indx + 1) % len(camPositions)
		time.sleep(.5)
		Tonbo.setTiltPos(4)
		time.sleep(2)
		
		subtractorOptical = Subsense.Lobster(lbsp_thresh = .1, num_samples_for_moving_avg = 25)
		SumOptical = np.zeros((576, 720))
		
		for i in range(NumFramesPerPosition):
			frameOptical = cam_optical.read()
				
			fg_mask_Optical=subtractorOptical.apply(np.uint8(frameOptical*MaskExclude))
			if (np.sum(fg_mask_Optical/255) > 0.01*(576*720)):
				fg_mask_Optical = 0*fg_mask_Optical

			SumOptical = SumOptical + fg_mask_Optical / 255
		
		subtractorOptical.release()
		check = np.sum(SumOptical > (60/5))
		if check > NumberExceededThreshold:
			# Fire Detected From Thermal Camera
			FOVTHERMAL = 10
			indcs = np.argwhere( frameThrm[frameThrm.shape[0]//2,50:650] > 250 )
			columnMedian = indcs[indcs.shape[0]//2][0]
			
			#Lat, Long = Tonbo.getCoordinates( 1, (Tonbo.getPanPos() + FOVTHERMAL*(360 - columnMedian)/(670 - 25))%360)
			Lat, Long = Tonbo.getCoordinates( 1, Tonbo.getPanPos())
			print("Smoke.............")
			# Stop Scanning
			return True, Lat, Long
	
	# if break while loop
	return False, -1, -1



if __name__ == '__main__':
    

	SmokeDetected, Lat, Long = StaticScan()
	if SmokeDetected:
		print(" Smoke Detected.....!!")
		
