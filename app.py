import json
from flask import Flask, render_template, make_response
from flask_socketio import SocketIO, emit
from node_pipeline import start_pipeline

import globals


app = Flask(__name__)
socketio = SocketIO(app, manage_session=True, cookie={}, monitor_clients=True)

globals.superInitialise()

@app.route('/')
def index():
    """Index route which initialises global variables
    and returns the homepage"""
    print(globals.ISACTIVE)
    if globals.ISACTIVE == False:
        globals.initialise()
        return render_template('./index.html')
    return render_template('lobby.html')
    

@socketio.on('start')
def start():
    """When start button is clicked, WebSocket event is triggered
    which starts the main programme"""
    emit('kickout', broadcast=True)
    start_pipeline()
    
    

@socketio.on('feedback')
def send_feedback():
    """Activated whenever feedback event is called from
    the client and server will send back a feedback event which
    converts the feedback list into JSON
    format which can be parsed by JavaScript to be displayed
    on the front end"""
    data = {
        "repCount": globals.repCount,
        "mainFeedback": globals.mainFeedback,
        "repFeedback": globals.repFeedback,
        "emotionFeedback": globals.emotionFeedback,
    }
    emit('feedback', json.dumps(data))


@socketio.on('endExercise')
def end_exercise():
    """Updates globals that exercise has ended so
    that the peekingduck backend knows to create a summary
    which can be retrieved by front end"""
    if not globals.exerciseEnded:
        globals.exerciseEnded = True
    # Add code to save exercise in a cookie

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

@socketio.on('disconnect')
def kill_peeking_duck():
    """Activated when person disconnects to kill the PeekingDuck Pipeline"""
    if globals.ISACTIVE:
        # Kills PeekingDuck if PeekingDuck is running
        globals.killSwitch = True

@app.route('/lobby')
def send_to_lobby():
    return render_template('lobby.html')

if __name__ == '__main__':
    # ssl_context=('cert.pem', 'key.pem')
    # debug=True
    # allow_unsafe_werkzeug=True
    # gunicorn -w 1 --threads 100 app:app 
    # use this command to run production ready server
    socketio.run(app,  host="0.0.0.0", ssl_context=('cert.pem', 'key.pem'), allow_unsafe_werkzeug=True)
    
