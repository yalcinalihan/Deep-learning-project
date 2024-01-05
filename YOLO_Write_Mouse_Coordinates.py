import time
from ultralytics import YOLO
import cv2

# Initialize variables to store mouse click coordinates
click_count = 0
click_coordinates = []

def mouse_callback(event, x, y, flags, param):
    global click_count, click_coordinates

    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"[{x}, {y}],")
        click_coordinates.append((x, y))
        click_count += 1

        if click_count == 2:  # changed to 4
            write_to_file(click_coordinates)
            click_count = 0
            click_coordinates = []


def write_to_file(coordinates):
    with open("clicks.txt", "a") as file:
        file.write(f"[{coordinates[0]}, {coordinates[1]}], \n")


model = YOLO("../Yolo-Weights/yolov8l.pt")


video_path = "aerialview2.mp4"
cap = cv2.VideoCapture(video_path)


cv2.namedWindow("Video")
cv2.setMouseCallback("Video", mouse_callback)


while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (1280, 720))
    if not ret:
        break

    cv2.imshow("Video", frame)


    if cv2.waitKey(0) != -1:
        break

# Continue with the rest of the video frames
while cap.isOpened():
    ret, frame = cap.read()
    frame = cv2.resize(frame, (1280, 720))
    if not ret:
        break


    results = model(frame)


    cv2.imshow("Video", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
