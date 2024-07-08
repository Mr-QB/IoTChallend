import cv2
import time
start_time = time.time()
from src.faceDetect import FaceDetector
from src.faceIdentification import FaceIdentifier


video = cv2.VideoCapture(0)
face_detector = FaceDetector()  # Create Face detector
face_identifier = FaceIdentifier()

# Initialize variables for FPS calculation
prev_frame_time = time.time()
end_time = time.time()
while True:
    print("boot time: {}".format(str(end_time-start_time)))
    ret, frame = video.read()
    fps = 0
    if not ret:
        break
    
    # Perform face detection and identification
    faces_cropped, x, y = face_detector.detect_face(frame)
    
    for i in range(len(faces_cropped)):
        x_min, x_max = x[i]
        y_min, y_max = y[i]
        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 1)
        
        face_name = face_identifier.result_name(faces_cropped[i])
        cv2.putText(frame, face_name, (x_min, y_min), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # Calculate FPS
    new_frame_time = time.time()
    fps = 1/(new_frame_time-prev_frame_time) 
    prev_frame_time = new_frame_time
    
    cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    
    # Display the frame
    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release video capture and close all windows
video.release()
cv2.destroyAllWindows()
