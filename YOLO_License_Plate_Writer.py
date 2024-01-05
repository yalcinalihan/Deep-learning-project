from ultralytics import YOLO
import cv2
import numpy as np
from sort.sort import *
from util import get_car, read_license_plate, write_csv

results = {}

mot_tracker = Sort()

Yolo_Model = YOLO('../Yolo-Weights/yolov8l.pt')
license_plate_confidence_threshold = 0.45 # Set the initial confidence threshold
license_plate_detector = YOLO("../Yolo-Weights/LicencePlate.pt")


cap = cv2.VideoCapture('./parkinglot8.mp4')

vehicles = [2, 3, 5, 7]  # car, bus, truck, motorbike from coco

frame_nmr = -1
ret = True
while ret:
    frame_nmr += 1
    ret, frame = cap.read()
    try:
        if ret:
            results[frame_nmr] = {}
            # Detect vehicles
            detections = Yolo_Model(frame)[0]
            detections_ = []
            for detection in detections.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = detection
                if int(class_id) in vehicles:
                    detections_.append([x1, y1, x2, y2, score])

                    # Draw bounding box for vehicles
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

            # Track vehicles
            track_ids = mot_tracker.update(np.asarray(detections_))

            license_plates = license_plate_detector(frame)[0]
            for license_plate in license_plates.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = license_plate

                #confidence threshold for license plate detection
                if score >= license_plate_confidence_threshold:
                    # Assign license plate to car
                    xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, track_ids)

                    if car_id != -1:
                        # Crop license plate
                        license_plate_crop = frame[int(y1):int(y2), int(x1): int(x2), :]

                        license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                        _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 64, 255,
                                                                        cv2.THRESH_BINARY_INV)

                        # Read license plate number
                        license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop_thresh)

                        if license_plate_text is not None:
                            results[frame_nmr][car_id] = {'car': {'bbox': [xcar1, ycar1, xcar2, ycar2]},
                                                          'license_plate': {'bbox': [x1, y1, x2, y2],
                                                                            'text': license_plate_text,
                                                                            'bbox_score': score,
                                                                            'text_score': license_plate_text_score}}

                            
                            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
                            # Display license plate text
                            cv2.putText(frame, license_plate_text, (int(x1), int(y1) - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # Display the frame
            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(e)
        continue

write_csv(results, './license_plates.csv')


cap.release()
cv2.destroyAllWindows()
