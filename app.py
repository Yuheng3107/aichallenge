import numpy as np
import cv2
from flask import Flask, render_template
from requests import Response
from main import main
app = Flask(__name__)

def initialise():
    global img
    img = np.zeros((720, 1280, 3))

def gen():
    while True:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n\r\n')
@app.route("/")
def index():
    return render_template('./index.html')

@app.route("/start")
def start():
    initialise()
    main()

@app.route("/video_feed")
def video_feed():
    ret, img = cv2.imencode('.jpeg', img)
    img = img.tobytes()
    return Response(gen(),
    mimetype='multipart/x-mixed-replace; boundary=frame')
