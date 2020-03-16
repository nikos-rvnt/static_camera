
import cv2 as cv
import numpy as np
import time
import TonboCamera
import alarmRequests
import queue, threading
#import matplotlib.pyplot as plt

# bufferless VideoCapture
class VideoCapture:

  def __init__(self, name):
    self.cap = cv.VideoCapture(name)
    self.q = queue.Queue()
    t = threading.Thread(target=self._reader)
    t.daemon = True
    t.start()

  # read frames as soon as they are available, keeping only most recent one
  def _reader(self):
    while True:
      ret, frame = self.cap.read()
      if not ret:
        break
      if not self.q.empty():
        try:
          self.q.get_nowait()   # discard previous (unprocessed) frame
        except Queue.Empty:
          pass
      self.q.put(frame)

  def read(self):
    return self.q.get()


if __name__ == '__main__':
    
    tonboThermal = 'rtsp://192.168.2.233:8555/video1'
    cam_thrm = VideoCapture(tonboThermal)
    tonby = TonboCamera.Tonbo()
    #tonby.resetThermal2Default()
    NumFramesPerPosition = 300
    # Scan
    #while 1:
    
        #Tonbo.setPanPos(camPositions[camPos_indx])
        #camPos_indx = (camPos_indx + 1) % len(camPositions)
        #time.sleep(1)
    tonby.setTiltPos(2.5)
    print('OOOOOOoOOOOO')
    time.sleep(8)
    #cam_thrm.set(cv.CAP_PROP_BUFFERSIZE, 0)
    frameThrm = cam_thrm.read()
    
    check = np.sum( frameThrm[ :, :, 0] > 55 )
    #cv.imshow('frm',frameThrm[:,:,0])
    #cv.waitKey(0)
    
    print(check)
    #_, ax = plt.subplots(111)
    if check > 1:
        # Fire Detected From Thermal Camera
        FOVTHERMAL = 10
        indcs = np.argwhere( frameThrm[ :, :,0] > 55 )
        columnMedian = [indcs[len(indcs)//2][0],indcs[len(indcs)//2][1]]
        
        #cam_thrm.release()
        while np.abs(columnMedian[0] - 288)>35:
            
            print(columnMedian[0] - frameThrm.shape[0]//2)
            print('aaaa')
            #cam_thrm = cv.VideoCapture(tonboThermal)
            frame = cam_thrm.read()
            #im = ax.imshow(frame[:,:,0])
            
            
            #print(retThrm)
            indcs = np.argwhere( frame[ :, :,0] > 55 )
            #columnMedian = [0,0]
            columnMedian = [indcs[len(indcs)//2][0],indcs[len(indcs)//2][1]]
            
            print(columnMedian)
            print(np.median(indcs, axis = 0)[0])
            if (columnMedian[0] - 288)>35:
                print('bbbb')              
                whichTilt = tonby.getTiltPos()
                tonby.setTiltPos( whichTilt + .5 )
                time.sleep(5)
                tonby.stopAllAction()
            elif (columnMedian[0] - 288)<-35: 
                print('ccc') 
                whichTilt = tonby.getTiltPos()
                tonby.setTiltPos( whichTilt - .5 )  
                time.sleep(5)
                
            else: 
                break
            
            tonby.stopAllAction()
            #cam_thrm.release()
            #time.sleep(8)
            #retThrm, frameThrm = cam_thrm.read()
            #indcs = np.argwhere( frameThrm[ 50:500, 50:650,0] > 170 )
            #indcs = np.argwhere( np.max(frameThrm[ 50:500, 50:650,:]) )
            #columnMedian = indcs[indcs.shape[0]//2]
            #print(columnMedian)
            #time.sleep(2)
        #Lat, Long = Tonbo.getCoordinates( 1, (Tonbo.getPanPos() + FOVTHERMAL*(360 - columnMedian)/(670 - 25))%360)
        #Lat, Long = tonby.getCoordinates( 1, Tonbo.getPanPos())
        print("Fire.............")
