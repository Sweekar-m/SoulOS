import mss
import numpy as np
import cv2

def capture_screen():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        img = np.array(sct.grab(monitor))
        frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        resized_frame = cv2.resize(frame, (960, 540))  # Reduce resolution to speed up
        return resized_frame