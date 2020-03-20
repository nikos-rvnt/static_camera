import Subsense
from matplotlib.transforms import Affine2D
import numpy as np
import cv2
import os

def CheckForSmoke(OMask,TMask,Optical,FrameNum):
    sx,sy = OMask.shape
    P = np.sum(OMask > 5*TMask)
    print("Possible Smoke Pixels: " + str(P), FrameNum)
    cv2.imwrite('Img/Detect/Frames_' + str(FrameNum/250) + '_PixelsDetected_'+ str(P) +'.jpg', np.uint8(255*(OMask > TMask)))

def main():
    import sys
    import time
    import subprocess
    MaskExclude = np.ones((576,720,3))
    if len(sys.argv)==4:
        MaskExclude = cv2.imread(sys.argv[3])>0
    if len(sys.argv) < 3:
        print('Usage: %s video-file'%os.path.basename(sys.argv[0]))
        sys.exit(-1)
    Optical_video_path = sys.argv[1]
    Thermal_video_path = sys.argv[2]
    capOptical = cv2.VideoCapture(Optical_video_path)
    capThermal = cv2.VideoCapture(Thermal_video_path)
    subtractorOptical = Subsense.Lobster(lbsp_thresh = .1, num_samples_for_moving_avg = 25)
    subtractorThermal = Subsense.Lobster(lbsp_thresh = .05, num_samples_for_moving_avg = 25, min_color_dist_thresh = 10)
    i = 0
    T = np.float32([[0.9557, 0.0369, -1.4987], [-0.0235, 0.8806, 44.2869]])
    kernel = np.ones((40,30),np.uint8)
    DropFrame = 1
    SumOptical = np.zeros((576,720))
    SumThermal = np.zeros((576,720))
    t1 = time.time()
    while True:
        i = i + 1
        ret1, Optical = capOptical.read()
        ret2, Thermal = capThermal.read()
        if (Optical is None) or (Thermal is None):
            break
        if i % 250 == 0:
            CheckForSmoke(SumOptical,SumThermal,Optical,i)
            SumOptical = np.zeros((576,720))
            SumThermal = np.zeros((576,720))
            subtractorOptical.release()
            subtractorThermal.release()
            subtractorOptical = Subsense.Lobster(lbsp_thresh = .1, num_samples_for_moving_avg = 25)
            subtractorThermal = Subsense.Lobster(lbsp_thresh = .05, num_samples_for_moving_avg = 25, min_color_dist_thresh = 10)

        fg_mask_Optical=subtractorOptical.apply(np.uint8(Optical*MaskExclude))
        fg_mask_Thermal=subtractorThermal.apply(np.uint8(Thermal*MaskExclude))
        fg_mask_Optical = cv2.warpAffine(fg_mask_Optical, T,(720,576))
        dilation = cv2.dilate(fg_mask_Thermal,kernel,iterations = 1)
        SumOptical = SumOptical + fg_mask_Optical
        SumThermal = SumThermal + dilation
        # Uncomment to Save Images to Folder Img
        # img2save = np.dstack((fg_mask_Optical,np.zeros(fg_mask_Thermal.shape),dilation))
        # cv2.imwrite('Img/' + str(i/DropFrame)+'.jpg', np.uint8(img2save))
        # cv2.imwrite('Img/O' + str(i/DropFrame)+'.jpg', np.uint8(fg_mask_Optical))
        # cv2.imwrite('Img/T' + str(i/DropFrame)+'.jpg', np.uint8(fg_mask_Thermal))
        # cv2.imwrite('Img/F' + str(i/DropFrame)+'.jpg', np.uint8(img2save/2 + cv2.warpAffine(Optical, T,(720,576))))

    subtractorOptical.release()
    subtractorThermal.release()
    t2 = time.time()
    print("Fps Calculated:")
    print(i/(t2-t1))
if __name__=='__main__':
    main()
