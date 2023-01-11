import numpy as np
import cv2
from flask import Flask, render_template, Response

from main import main
app = Flask(__name__)

def initialise():
    global img
    img = np.zeros((720, 1280, 3))

def gen(img):
    while True:
        ret, jpeg = cv2.imencode('.jpeg', img)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
@app.route('/')
def index():
    initialise()
    return render_template('./index.html')

@app.route('/start')
def start():
    
    main()

@app.route('/video_feed')
def video_feed():
    global img
    return Response(gen(img),
    mimetype='multipart/x-mixed-replace; boundary=frame')
