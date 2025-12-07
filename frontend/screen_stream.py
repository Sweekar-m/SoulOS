from flask import Blueprint, Response, render_template, request
import cv2
import numpy as np
import mss

screen_stream_blueprint = Blueprint("screen_stream", __name__)

def generate_frames():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        while True:
            img = np.array(sct.grab(monitor))
            frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            # Lower JPEG quality for faster streaming
            _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')


@screen_stream_blueprint.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


