# static_camera
code of static camera functionalities

### Init dir includes executable files to start up theasis system.
Open up a terminal and type:

1) ./SetupUI.sh
2) ./Init1.sh - to start mongodb, memcached, docker and create Theasis hotspot
3) web_browser --> http://localhost:1234
4) ./Init2.sh - to start Node.js server application
5) ./Init3.sh - to run websocket_client
6) ./Init4.sh - to run algorithm for smoke/fire detection from static camera and drone thermal camera stream

( if any of the above is not executable, you can force it to be by typing "sudo chmod +777 /path/to/file.extension" )

### image_processing dir includes python files of Smoke Detection algorithm

- Subsense.py
- SmokeDetection.py

### alarmRequests.py includes http request functions:

- newAlarm(latitude,longitude): to introduce a new smoke/fire alarm to the system 
- deleteAlarm(): to delete an unvalidated alarm 
- validateAlarm(): to validate an alarm 
- getQuadCoords(): to get current (with a small latency) quadcopter latitude, longitude 

### TonboCamera.py contains Tonbo class with all necessary static camera functionalities

- resetOptical2Default()/resetThermal2Default(): resets optical/thermal cam to its default settings

- setZoom()/getZoom(): sets/returns the optical cam zoom level 
- setThermalZoom()/getThermalZoom(): sets/returns the thermal cam zoom level 
- setThermalFocusNear(): focus thermal cam for near distances
- setThermalFocusFar(): focus thermal cam for far distances
- setThermalGain(): sets the thermal cam gain level (values: 00-62) 
- setThermalBrightness(): sets the thermal cam brightness level (values: 00-62) 
- setPanPos()/getPanPos(): sets/returns the pan position, that is the camera rotation angle from the zero position
- setTiltPos()/getTiltPos(): sets/returns the tilt position, that is the camera upside down angle 
- setZeroPos(): sets the initial position of the camera (getPanPos() on zero position will return 0 angle)
- stopAllAction(): stops any move of the camera
- getCoordinates(): returns the target (possible fire/smoke pixels) coordinates given the estimated distance and the camera pan position
- imCoords2angles(): computes the pan, tilt angles of the target 

### To check via ffplay if image signal is properly transmitted:

 Tonbo Static Camera:
  - (optical cam): ffplay "rtsp://192.168.2.233:8554/video0"
  - (thermal cam): ffplay "rtsp://192.168.2.233:8555/video1"

 DJI Quadcopter (only thermal camera signal is transmitted and stream is enabled when quadcopter is on mission):
  - ffplay "rtmp://127.0.0.1:1935/live/quad" 
  
### To record video stream via ffmpeg:
 - Tonbo Static Camera:
    - (optical cam): ffmpeg -i rtsp://192.168.2.233:8554/video0 -vcodec copy -acodec copy staticOptical_video.mp4
    - (thermal cam): ffmpeg -i rtsp://192.168.2.233:8555/video1 -vcodec copy -acodec copy staticThermal_video.mp4   
  
  - DJI Quadcopter (only thermal camera signal is transmitted and stream is enabled when quadcopter is on mission):
    - ffmpeg -i rtmp://127.0.0.1:1935/live/quad -vcodec copy -acodec copy quadStream_video.mp4
 
Video stream recording can be also done from another PC connected to Theasis hotspot. In that case, the video source should be changed to:
 
  - Tonbo Static Camera:
    * (optical cam): ffmpeg -i rtsp://192.168.2.100:8554/video0 -vcodec copy -acodec copy staticOptical_video.mp4
    * (thermal cam): ffmpeg -i rtsp://192.168.2.100:8555/video1 -vcodec copy -acodec copy staticThermal_video.mp4   
    * ffmpeg -i rtmp://192.168.2.100:1935/live/camera -vcodec copy -acodec copy staticStream_video.mp4
    (the third case works for sure, but only the static camera video source that is displayed from the UI (http://www.localhost:1234/) can be recorded)
  
  - DJI Quadcopter (only thermal camera signal is transmitted and stream is enabled when quadcopter is on mission):
    * ffmpeg -i rtmp://192.168.2.100:1935/live/quad -vcodec copy -acodec copy quadStream_video.mp4
    
### To record video stream via VLC:

 Video stream either from static camera or from quadcopter can be recorded from VLC. You should open a VLC and go to:
 
  -> Media/Convert/Network: enter the desired video source path and then select Convert. Then enter the destination file path of the recorded video and from the settings click on "Display the output" and at the Profile choose the video/audio codecs.
  
### To record video stream via OBS:

 Open OBS Studio and While stream to the UI is enabled, just click on Start Recording from the Controls panel. 
