import mss
import cv2
import numpy as np
from ultralytics import YOLO

# Load YOLOv8 model
model = YOLO("yolov8n.pt")  # Replace with your trained YOLOv8 model if needed

def detect_airplanes(frame):
    """
    Run YOLOv8 object detection on a given frame.

    Args:
        frame (np.array): The image frame from the screen.

    Returns:
        frame (np.array): The frame with bounding boxes drawn.
    """
    # Perform inference
    results = model(frame, conf=0.5)  # Adjust confidence threshold if needed

    # Get detections
    detections = results[0].boxes.data.cpu().numpy()  # Bounding boxes, confidence, and class ID
    for detection in detections:
        x_min, y_min, x_max, y_max, confidence, class_id = detection
        label = f"Airplane: {confidence:.2f}"

        # Draw bounding box
        cv2.rectangle(frame, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)
        cv2.putText(frame, label, (int(x_min), int(y_min) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return frame

def monitor_screen(region):
    """
    Monitor a specific part of the screen and run YOLO airplane detection.

    Args:
        region (tuple): The region of the screen to monitor (left, top, right, bottom).
    """
    print(f"Monitoring screen region: {region}")

    try:
        with mss.mss() as sct:
            monitor = {"top": region[1], "left": region[0], "width": region[2] - region[0], "height": region[3] - region[1]}

            while True:
                # Capture the screen
                screenshot = sct.grab(monitor)

                # Convert the screenshot to a NumPy array
                frame = np.array(screenshot)

                # Convert BGRA to BGR (for OpenCV compatibility)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

                # Run YOLO detection on the frame
                frame = detect_airplanes(frame)

                # Display the monitored region with detections
                cv2.imshow("Screen Monitor with YOLOv8 Detection", frame)

                # Break the loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("Exiting screen monitor.")
                    break
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
    finally:
        cv2.destroyAllWindows()

# Define the region to monitor (left, top, right, bottom)
region_to_monitor = (629, 190, 1053, 931)

# Start monitoring
monitor_screen(region=region_to_monitor)
