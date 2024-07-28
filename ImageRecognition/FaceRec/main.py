import cv2
import time
from src.trainer import Trainer
import paho.mqtt.client as mqtt
import time


def test():
    from src.faceDetect import FaceDetector
    from src.faceAlignMent import FaceAlignment
    from src.faceIdentification import FaceIdentifier

    video = cv2.VideoCapture(0)
    face_detector = FaceDetector()  # Create Face detector
    face_alignment = FaceAlignment()
    face_identifier = FaceIdentifier()

    broker = "pi.local"
    port = 1883
    topic = "2173"

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully to broker")
        else:
            print(f"Failed to connect, return code {rc}")

    def on_disconnect(client, userdata, rc):
        print(f"Disconnected with return code {rc}")

    def publish_message(client, topic, message):
        try:
            client.publish(topic, message, qos=0, retain=True)
            print(f"Message '{message}' published to topic '{topic}'")
        except Exception as e:
            print(f"Failed to publish message: {e}")

    # Tạo một instance của client
    client = mqtt.Client()

    # Đăng ký callback cho các sự kiện
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect(broker, port, 60)

    # Initialize variables for FPS calculation
    prev_frame_time = time.time()
    while True:
        ret, frame = video.read()
        fps = 0
        if not ret:
            break
        # frame = cv2.resize(frame, (1080, 720))

        # Perform face detection and identification
        faces_cropped, x, y = face_detector.detect_face(frame)
        # if len(faces_cropped) > 0:
        #     face_name = face_identifier.result_name(faces_cropped[0])
        # print(face_name)
        for i in range(len(faces_cropped)):
            x_min, x_max = x[i]
            y_min, y_max = y[i]
            w = faces_cropped[i].shape[1] // 2
            h = faces_cropped[i].shape[0] // 2
            ymin = 0 if (y_min - h) < 0 else (y_min - h)
            xmin = 0 if (x_min - w) < 0 else (x_min - w)
            ymax = frame.shape[0] if (y_max + h) > frame.shape[0] else (y_max + h)
            xmax = frame.shape[1] if (x_max + w) > frame.shape[1] else (x_max + w)
            face_ = frame[ymin:ymax, xmin:xmax, :]

            alpha = face_alignment.align_face(faces_cropped[i])
            height, width = face_.shape[:2]
            center = (width / 2, height / 2)
            rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=alpha, scale=1)
            face_2 = cv2.warpAffine(src=face_, M=rotate_matrix, dsize=(width, height))

            faces_cropped_, x_, y_ = face_detector.detect_face(
                face_2
            )  # Second face detection
            if len(faces_cropped_) == 0:
                break
            else:
                for i in range(len(faces_cropped_)):
                    face_name = face_identifier.result_name(faces_cropped_[i])
                    if face_name != "Fake images" and face_name != "Unable to identify":
                        publish_message(client, topic, "ON")
                    print(face_name)
                    # cv2.imshow("face", faces_cropped_[0])

                    cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 1)
                    cv2.putText(
                        frame,
                        face_name,
                        (x_min, y_min),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (255, 0, 0),
                        2,
                    )

        #   Calculate FPS
        # new_frame_time = time.time()
        # fps = 1 / (new_frame_time - prev_frame_time)
        # prev_frame_time = new_frame_time

        # cv2.putText(
        #     frame,
        #     f"FPS: {fps:.2f}",
        #     (10, 30),
        #     cv2.FONT_HERSHEY_SIMPLEX,
        #     0.7,
        #     (255, 0, 0),
        #     2,
        # )

        # Display the frame
        cv2.imshow("frame", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


if __name__ == "__main__":
    test()
