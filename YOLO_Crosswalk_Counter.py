import cv2
import numpy as np
from ultralytics import YOLO


model = YOLO("../Yolo-Weights/AerialHuman.pt")


video_path = "aerialview2.mp4"  # Change the video file name
cap = cv2.VideoCapture(video_path)

# Confidence threshold 
confidence_threshold = 0.1

# ROI
roi = np.array([[1117, 373], [979, 411], [932, 442], [918, 528], [996, 693], [1237, 610]])

# Function to check if a point is inside a polygon
def is_inside_polygon(point, polygon):
    return cv2.pointPolygonTest(polygon, point, False) >= 0

# Open CSV file for writing people count
csv_file_path = "people_in_polygon.csv"

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    # Resize 
    frame = cv2.resize(frame, (1280, 720))

    # Draw the polygon 
    cv2.polylines(frame, [roi], True, (0, 255, 0), 2)

    # YOLO object detection on the entire frame
    results = model(frame, stream=True)

    # Count of people in the ROI
    people_count_in_polygon = 0


    for r in results.xyxy if hasattr(results, 'xyxy') else results:
        for box in r.boxes:
            x1, y1, x2, y2 = box.xyxy[0]

            # Check if the detected object is within
            if is_inside_polygon((int(x1), int(y1)), roi) or is_inside_polygon((int(x2), int(y2)), roi):
                # confidence threshold
                if box.conf[0] >= confidence_threshold:
                    # people count
                    people_count_in_polygon += 1

                    w, h = x2 - x1, y2 - y1
                    pt1 = (int(x1), int(y1))
                    pt2 = (int(x2), int(y2))
                    cv2.rectangle(frame, pt1, pt2, (0, 255, 0), 2)

                    # Displaying confidence and class name
                    display_text = f'{model.names[int(box.cls[0])]} {box.conf[0]:.2f}'
                    cv2.putText(frame, display_text, (max(0, pt1[0]), max(35, pt1[1])),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Opening CSV file for writing and write frame number and people count
    with open(csv_file_path, 'w') as csv_file:
        csv_file.write(f"{cap.get(cv2.CAP_PROP_POS_FRAMES)},{people_count_in_polygon}\n")

    cv2.imshow("Video with Bounding Boxes", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
