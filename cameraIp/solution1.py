import cv2
import os

# Set OpenCV's FFmpeg capture options to use UDP transport
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;0"

# URL of the RTSP stream
rtsp_url = "rtsp://admin:Matkhau123@192.168.1.10:554/onvif1"

# Open the RTSP stream
cap = cv2.VideoCapture(rtsp_url)

# Check if the stream was opened successfully
if not cap.isOpened():
    print("Cannot open RTSP stream")
    exit()

# Read and display each frame from the stream
while True:
    ret, frame = cap.read()
    if not ret:
        print("Cannot receive frame from stream")
        break

    cv2.imshow("RTSP Stream", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
