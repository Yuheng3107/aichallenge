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

@socketio.on('start')
def start():
    """When start button is clicked, WebSocket event is triggered
    which starts the main programme"""
    main()

@app.route('/video_feed')
def video_feed():
    """Route that updates video frames using the global
    img variable"""
    return Response(gen(),
    mimetype='multipart/x-mixed-replace; boundary=frame')


@socketio.on('feedback')
def send_feedback():
    """Activated whenever feedback event is called from
    the client and server will send back a feedback event which
    converts the feedback list into JSON
    format which can be parsed by JavaScript to be displayed
    on the front end"""
    data = {
        "repCount": globals.repCount,
        "summary": globals.mainFeedback,
        "repFeedback": globals.repFeedback,
        "stressFeedback": globals.stressFeedback,
    }
    emit('feedback', json.dumps(data))


@socketio.on('endExercise')
def end_exercise():
    """Updates globals that exercise has ended so
    that the peekingduck backend knows to create a summary
    which can be retrieved by front end"""
    if not globals.exerciseEnded:
        globals.exerciseEnded = True

@socketio.on('changeExercise')
def change_exercise(exerciseId):
    globals.currentExercise = int(exerciseId)
    globals.exerciseSelected = True

@socketio.on('changeDifficulty')
def change_difficulty(difficulty):
    """Function that updates global variable
    for backend to receive when user changes difficulty
     in front end"""
    globals.difficulty = difficulty


@socketio.on('video')
def handle_video(data):
    globals.url = data['url']


if __name__ == '__main__':
    # ssl_context=('cert.pem', 'key.pem')
    # debug=True
    # allow_unsafe_werkzeug=True
    # gunicorn -w 1 --threads 100 app:app 
    # use this command to run production ready server
    socketio.run(app,  host="0.0.0.0", ssl_context=('cert.pem', 'key.pem'), allow_unsafe_werkzeug=True)
    

