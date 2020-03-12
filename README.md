# static_camera
code of static camera functionalities

### Init dir includes executable files to start up theasis system.
Open up a terminal and type:

1) ./start_docker&hotspot.sh - to start mongodb, memcached, docker and create Theasis hotspot
2) web_browser --> http://localhost:1234
3) ./start_theasisApp.sh - to start Node.js server application
4) ./start_websocket.sh - to run websocket_client
5) ./start_cam_algo.sh - to run algorithm for smoke/fire detection from static camera and drone thermal camera stream

### image_processing dir includes python files of Smoke Detection algorithm

- Subsense.py
- SmokeDetection.py

### alarmRequests.py includes http request functions:

- newAlarm(latitude,longitude): to introduce a new smoke/fire alarm to the system 
- deleteAlarm(): to delete an unvalidated alarm 
- validateAlarm(): to validate an alarm 
- getQuadCoords(): to get current (with a small latency) quadcopter latitude, longitude 

### TonboCamera.py contains Tonbo class with all necessary static camera functionalities

- setZoom()/getZoom(): sets/returns the zoom level 
- setGain()/getGain(): sets/returns the gain level
- setBrightness()/getBrightness(): sets/returns the brightness level
- setPanPos()/getPanPos(): sets/returns the pan position, that is the camera rotation angle from the zero position
- setTiltPos()/getTilePos(): sets/returns the tilt position, that is the camera upside down angle 
- setZeroPos(): sets the initial position of the camera (getPanPos() on zero position will return 0 angle)
- getCoordinates(): returns the target (possible fire/smoke pixels) coordinates given the estimated distance and the camera pan position


### To check if image signal is properly transmitted via ffplay:

 Tonbo Static Camera:
  - (optical cam): ffplay "rtsp://192.168.2.233:8554/video0"
  - (thermal cam): ffplay "rtsp://192.168.2.233:8555/video1"

 DJI Quadcopter (only thermal camera signal is transmitted):
  - ffplay "rtmp://127.0.0.1:1935/live/quad" 
  
  
  
