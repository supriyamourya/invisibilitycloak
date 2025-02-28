import cv2
import numpy as np
import time

# Step 1: Capture the background
cap = cv2.VideoCapture(0)  # Open webcam
time.sleep(2)  # Allow the camera to adjust

# Capture background
for i in range(30):  # Capture multiple frames for a stable background
    ret, background = cap.read()
background = cv2.flip(background, 1)  # Flip for mirror effect

# Step 2: Detect the cloak color
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Flip for mirror effect
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Convert to HSV color space

    # Define the HSV range for the red color of the cloak
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    # Create masks for detecting red color
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 + mask2

    # Step 3: Refine the mask
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))

    # Step 4: Replace the cloak area with the background
    invisibility = cv2.bitwise_and(background, background, mask=mask)
    inverse_mask = cv2.bitwise_not(mask)
    current = cv2.bitwise_and(frame, frame, mask=inverse_mask)
    combined = cv2.addWeighted(invisibility, 1, current, 1, 0)

    # Display the result
    cv2.imshow("Invisibility Cloak", combined)

    # Break on pressing 'q'
    if cv2.waitKey(40) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
