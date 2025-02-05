import mss
import cv2
import numpy as np

def monitor_screen(region):
    """
    Monitor a specific part of the screen with improved frame rate.

    Args:
        region (tuple): The region of the screen to monitor (left, top, right, bottom).
    """
    print(f"Monitoring screen region: {region}")
    try:
        with mss.mss() as sct:
            # Define the monitor region
            monitor = {"top": region[1], "left": region[0], "width": region[2] - region[0], "height": region[3] - region[1]}

            while True:
                # Capture the screen
                screenshot = sct.grab(monitor)

                # Convert the screenshot to a NumPy array
                frame = np.array(screenshot)

                # Convert BGRA to BGR (for OpenCV compatibility)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

                # Display the monitored region
                cv2.imshow("Screen Monitor", frame)

                # Break the loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("Exiting screen monitor.")
                    break
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
    finally:
        cv2.destroyAllWindows()

# Define the region to monitor (left, top, right, bottom)
# Example: Monitor the specific part of the screen
region_to_monitor = (629, 190, 1053, 931)

# Start monitoring
monitor_screen(region=region_to_monitor)
