import cv2
import os

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;0"


# URL của luồng RTSP
rtsp_url = "rtsp://admin:Matkhau123@192.168.1.10:554/onvif1"

# Mở luồng RTSP
cap = cv2.VideoCapture(rtsp_url)

# Kiểm tra xem luồng có được mở thành công không
if not cap.isOpened():
    print("Không thể mở luồng RTSP")
    exit()

# Đọc và hiển thị từng khung hình từ luồng
while True:
    ret, frame = cap.read()
    if not ret:
        print("Không thể nhận khung hình từ luồng")
        break

    cv2.imshow("RTSP Stream", frame)

    # Nhấn 'q' để thoát
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
