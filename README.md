# static_camera
code of sfeda static camera functionalities

### Init dir includes executable files to start up theasis system.
Open up a terminal and :

1) ./start_docker&hotspot.sh - to start mongodb, memcached, docker and create Theasis hotspot
2) ./start_theasisApp.sh - to start Node.js server application
3) ./start_websocket.sh - to run websocket_client
4) ./start_cam_algo.sh - to run algorithm for smoke/fire detection from static camera and drone thermal camera stream

### image_processing dir includes python files of Smoke Detection algorithm

- Subsense.py
- SmokeDetection.py

### alarmRequests.py includes http request functions:

- newAlarm(latitude,longitude): to introduce a new smoke/fire alarm to the system 
- deleteAlarm(): to delete an unvalidated alarm 
- validateAlarm(): to validate an alarm 
- getQuadCoords(): to get current (with a small latency) quadcopter latitude, longitude 

### To check if image signal is properly transmitted via ffplay:

 Tonbo Static Camera:
  - (optical cam): ffplay "rtsp://192.168.2.233:8554/video0"
  - (thermal cam): ffplay "rtsp://192.168.2.233:8555/video1"

 DJI Quadcopter (only thermal camera signal is transmitted):
  - ffplay "rtmp://127.0.0.1:1935/live/quad" 
  
  
  
