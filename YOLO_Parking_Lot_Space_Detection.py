import cv2
import cvzone
from ultralytics import YOLO
import csv
# Load YOLO model
model = YOLO("Yolo-Weights\AerialCarView.pt")

# Open video file
video_path = "parkinglot9.mp4"
cap = cv2.VideoCapture(video_path)

# New frame size
frame_width = 1280
frame_height = 720

# Confidence threshold for YOLO detections
confidence_threshold = 0.1



rois = [[(141, 79), (223, 266)],
[(238, 111), (306, 262)],
[(311, 110), (384, 252)],
[(388, 115), (472, 259)],
[(486, 115), (555, 260)],
[(569, 112), (639, 259)],
[(650, 112), (723, 261)],
[(735, 117), (808, 261)],
[(818, 117), (889, 262)],
[(902, 117), (974, 265)],
[(986, 114), (1056, 266)],
[(1069, 116), (1143, 265)],
[(1156, 120), (1240, 266)],
[(152, 480), (217, 619)],
[(233, 478), (301, 625)],
[(306, 481), (379, 643)],
[(382, 480), (468, 640)],
[(485, 475), (548, 624)],
[(568, 482), (632, 622)],
[(654, 478), (722, 625)],
[(733, 485), (803, 626)],
[(820, 485), (884, 626)],
[(900, 483), (975, 625)],
[(988, 485), (1059, 630)],
[(1069, 484), (1146, 625)],
[(1159, 485), (1229, 627)], ]



# Function to enlarge the ROIs by 20%
def enlarge_roi(roi):
    x1, y1 = roi[0]
    x2, y2 = roi[1]
    width = x2 - x1
    height = y2 - y1
    enlargement_factor = 0.15

    # Enlarge the ROI by 20%
    x1 -= int(width * enlargement_factor)
    y1 -= int(height * enlargement_factor)
    x2 += int(width * enlargement_factor)
    y2 += int(height * enlargement_factor)

    return [(x1, y1), (x2, y2)]

# Enlarge the ROIs
enlarged_rois = [enlarge_roi(roi) for roi in rois]
# Initialize a list to store the status of each ROI (0 = no object, 1 = object detected)
roi_status = [0] * len(enlarged_rois)



roi_dict = {}
for i in roi_status:
    roi_dict[i + 1] = 0



while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    # Resize the frame to the new size
    frame = cv2.resize(frame, (frame_width, frame_height))

    # Perform YOLO object detection on the entire frame
    results = model(frame, stream=True)

    # Draw bounding boxes for detected objects within the enlarged ROIs
    for r in results.xyxy if hasattr(results, 'xyxy') else results:
        for box in r.boxes:
            x1, y1, x2, y2 = box.xyxy[0]

            # Check if the detected object is within any enlarged ROI
            for i, roi in enumerate(enlarged_rois):
                roi_start, roi_end = roi
                if roi_start[0] <= x1 <= roi_end[0] and roi_start[1] <= y1 <= roi_end[1]:
                    # Apply confidence threshold
                    if box.conf[0] >= confidence_threshold:
                        # Bounding Box on the original frame
                        # w, h = x2 - x1, y2 - y1
                        # pt1 = (int(x1), int(y1))
                        # pt2 = (int(x2), int(y2))
                        # cv2.rectangle(frame, pt1, pt2, (0, 255, 0), 2)
                        #
                        # # Display confidence and class name
                        # display_text = f'{model.names[int(box.cls[0])]} {box.conf[0]:.2f}'
                        # cvzone.putTextRect(frame, display_text, (max(0, pt1[0]), max(35, pt1[1])),
                        #                    scale=1, thickness=1)

                        # Update the status of the ROI
                        roi_status[i] = 1

    # Draw rectangles for each original ROI (not enlarged)
    for i, roi in enumerate(rois):
        roi_start, roi_end = roi
        label = f'Area {i + 1}'  # Add a label based on the order in the roi list
        color = (0, 0, 255) if roi_status[i] == 1 else (0, 255, 0)  # Red if object detected, else green
        cv2.rectangle(frame, roi_start, roi_end, color, 2)

        if roi_status[i] == 1:
            roi_dict[i] = 1
        else:
            roi_dict[i] = 0
        with open("empty_spaces.txt", 'w') as file:
            # Iterate through the dictionary items and write them to the file
            for key, value in roi_dict.items():
                file.write(f'{key + 1}:{value}\n')


        # Display label
        cv2.putText(frame, label, (roi_start[0], roi_start[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # Reset the status of all ROIs to 0 for the next frame
    roi_status = [0] * len(enlarged_rois)

    # Display the frame with bounding boxes and original rectangles
    cv2.imshow("Video with Bounding Boxes", frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


