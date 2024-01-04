import cv2
import cvzone
from ultralytics import YOLO

model = YOLO("../Yolo-Weights/AerialCarView.pt")

video_path = "parkinglot4.mp4"
cap = cv2.VideoCapture(video_path)

frame_width = 1280
frame_height = 720

confidence_threshold = 0.1

rois = [
    [(46, 48), (161, 263)],
    [(136, 41), (250, 258)],
    [(235, 45), (344, 258)],
    [(333, 54), (435, 258)],
    [(431, 59), (528, 254)],
    [(522, 57), (618, 258)],
    [(614, 57), (708, 252)],
    [(705, 60), (801, 249)],
    [(792, 57), (895, 251)],
    [(894, 57), (984, 254)],
    [(986, 57), (1076, 254)],
    [(1078, 62), (1173, 259)],
    [(1171, 60), (1259, 251)],
    [(67, 508), (161, 699)],
    [(159, 510), (252, 699)],
    [(250, 507), (343, 702)],
    [(343, 511), (436, 701)],
    [(434, 507), (527, 702)],
    [(526, 509), (616, 700)],
    [(617, 510), (709, 702)],
    [(708, 507), (800, 701)],
    [(799, 513), (892, 701)],
    [(891, 511), (979, 700)],
    [(982, 507), (1072, 701)],
    [(1073, 509), (1163, 701)],
    [(1165, 510), (1255, 702)],
]

def enlarge_roi(roi):
    x1, y1 = roi[0]
    x2, y2 = roi[1]
    width = x2 - x1
    height = y2 - y1
    enlargement_factor = 0.15

    x1 -= int(width * enlargement_factor)
    y1 -= int(height * enlargement_factor)
    x2 += int(width * enlargement_factor)
    y2 += int(height * enlargement_factor)

    return [(x1, y1), (x2, y2)]

enlarged_rois = [enlarge_roi(roi) for roi in rois]

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.resize(frame, (frame_width, frame_height))

    for roi in rois:
        roi_start, roi_end = roi
        cv2.rectangle(frame, roi_start, roi_end, (0, 255, 0), 2)

    results = model(frame, stream=True)

    for r in results.xyxy if hasattr(results, 'xyxy') else results:
        for box in r.boxes:
            x1, y1, x2, y2 = box.xyxy[0]

            for roi in enlarged_rois:
                roi_start, roi_end = roi
                if roi_start[0] <= x1 <= roi_end[0] and roi_start[1] <= y1 <= roi_end[1]:
                    if box.conf[0] >= confidence_threshold:
                        w, h = x2 - x1, y2 - y1
                        pt1 = (int(x1), int(y1))
                        pt2 = (int(x2), int(y2))
                        cv2.rectangle(frame, pt1, pt2, (0, 255, 0), 2)

                        display_text = f'{model.names[int(box.cls[0])]} {box.conf[0]:.2f}'
                        cvzone.putTextRect(frame, display_text, (max(0, pt1[0]), max(35, pt1[1])),
                                           scale=1, thickness=1)

    cv2.imshow("Video with Bounding Boxes", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
