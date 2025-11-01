import cv2
import numpy as np
import threading
import time
from ultralytics import YOLO
import random
#from pymodbus.client import ModbusTcpClient

# =========================
# ⚙️ Biến toàn cục
# =========================
frame = None
obj = False
detecting = True
show_window = True

# =========================
# 🚀 Khởi tạo YOLO TensorRT
# =========================
model_path = "best.engine"
object_detect = YOLO(model_path, task='detect')

# =========================
# 🏷️ Tên lớp và màu sắc
# =========================
class_names = {0: "1", 1: "NG", 2: "Object3", 3: "Object4", 4: "Object5"}
color_map = {
    0: (0, 255, 0),
    1: (0, 0, 255),
    2: (0, 0, 255),
    3: (255, 255, 0),
    4: (0, 255, 255)
}

# =========================
# 🎥 Thread đọc camera
# =========================
def read_camera():
    global frame, detecting

    gst_str = (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, "
        "format=(string)NV12, framerate=(fraction)30/1 ! "
        "nvvidconv flip-method=0 ! "
        "video/x-raw, width=(int)1280, height=(int)720, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
    )

    cap = cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)
    if not cap.isOpened():
        print("❌ Không thể kết nối CSI camera!")
        exit()

    while detecting:
        success, frame_temp = cap.read()
        if success:
            # Resize và xoay
            frame1 = cv2.rotate(cv2.resize(frame_temp, (1280, 720)), cv2.ROTATE_180)
            # Giữ alpha = 1.0 để không quá sáng, giảm tải GPU
            frame = cv2.convertScaleAbs(frame1, alpha=1.0, beta=0)

    cap.release()

# =========================
# 🧠 Thread YOLO Detect
# =========================
def detect_objects():
    global obj, detecting, frame

    while detecting:
        if frame is not None:
            # Sao chép frame để tránh xung đột đọc/ghi
            frame_copy = frame.copy()

            # Chạy YOLO trên bản sao
            results = object_detect(frame_copy, conf=0.4, imgsz=640)
            detections = results[0].boxes

            # Kiểm tra có class 0 hay không
            obj = 0 in detections.cls.tolist()

            # Vẽ bounding boxes
            for box, cls, conf in zip(
                detections.xyxy.int().tolist(),
                detections.cls.tolist(),
                detections.conf.tolist()
            ):
                x1, y1, x2, y2 = box
                color = color_map.get(int(cls), (random.randint(0,255), random.randint(0,255), random.randint(0,255)))
                label = f"{class_names.get(int(cls), str(cls))}: {conf:.2f}"
                cv2.rectangle(frame_copy, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame_copy, label, (x1, y1 - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # Gán lại frame đã vẽ xong
            frame = frame_copy

        # Giảm tải CPU, tránh block camera
        time.sleep(0.05)

# =========================
# 💡 Giao diện điều khiển
# =========================
cv2.namedWindow('Control Panel', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Control Panel', 300, 100)
cv2.imshow('Control Panel', np.zeros((100, 300, 3), dtype=np.uint8))

# =========================
# 🧵 Khởi động các thread
# =========================
thread_camera = threading.Thread(target=read_camera, daemon=True)
thread_yolo = threading.Thread(target=detect_objects, daemon=True)

thread_camera.start()
thread_yolo.start()

# =========================
# 🧭 Vòng lặp chính hiển thị
# =========================
while True:
    if frame is not None and show_window:
        cv2.imshow("Object Detection", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        print("🛑 Thoát chương trình...")
        detecting = False
        break

    elif key == ord('r'):
        print("📴 Tắt camera và phát hiện")
        detecting = False
        frame = None

    elif key == ord('w'):
        show_window = not show_window
        if not show_window:
            cv2.destroyWindow("Object Detection")
        print(f"🔧 Trạng thái hiển thị: {'BẬT' if show_window else 'TẮT'}")

cv2.destroyAllWindows()
