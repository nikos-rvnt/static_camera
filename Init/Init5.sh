ffmpeg -i "rtsp://192.168.2.233:8554/video0" -i "rtsp://192.168.2.233:8555/video1" -i "rtmp://127.0.0.1:1935/live/quad" -filter_complex "[0:v:0][1:v:0][2:v:0]vstack=inputs=3" -f avi - | ffplay -
