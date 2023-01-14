
import cv2
import json
from flask import Flask, render_template, Response, request
from flask_socketio import SocketIO, emit
import globals
from main import main

app = Flask(__name__)
socketio = SocketIO(app)


def gen():
    """Generator function which yields img frames 
    to be displayed in the front-end"""
    while True:
        
        ret, jpeg = cv2.imencode('.jpeg', globals.img)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
def index():
    """Index route which initialises global variables
    and returns the homepage"""
    globals.initialise()
    return render_template('./index.html')

@app.route('/start')
def start():
    """When start button is clicked, GET request (AJAX)
    is sent to this route to get the peekingduck pipeline
    running"""
    main()

@app.route('/video_feed')
def video_feed():
    """Route that updates video frames using the global
    img variable"""
    return Response(gen(),
    mimetype='multipart/x-mixed-replace; boundary=frame')

"""
@app.route('/feedback')
def send_feedback():

    return json.dumps(globals.feedback)
"""

@socketio.on('feedback')
def send_feedback():
    """Activated whenever feedback event is called from
    the client and server will send back a feedback event which
    converts the feedback list into JSON
    format which can be parsed by JavaScript to be displayed
    on the front end"""
    emit('feedback', json.dumps(globals.feedback))


@app.route('/endExercise')
def end_exercise():
    if not globals.exerciseEnded:
        globals.exerciseEnded = True
    return ""

"""
Deprecated
@app.route('/changeExercise', methods= ['POST'])
def change_exercise():
    
    exerciseId = request.form["exerciseId"]
    globals.currentExercise = int(exerciseId)
    globals.exerciseSelected = True
    # Sends post request which returns "" to dummy iframe
    # This circumvents the issue of form redirect
    return ""
"""

@socketio.on('changeExercise')
def change_exercise(exerciseId):
    globals.currentExercise = int(exerciseId)
    globals.exerciseSelected = True



if __name__ == '__main__':
    socketio.run(app)
