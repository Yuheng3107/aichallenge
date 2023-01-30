import json
from flask import Flask, render_template, make_response, redirect
from flask_socketio import SocketIO, emit, send, disconnect
from node_pipeline import start_pipeline

import globals
from numpy import broadcast


app = Flask(__name__)
socketio = SocketIO(app, manage_session=True, cookie={}, monitor_clients=True)

globals.superInitialise()

### WEBPAGE METHODS
##########

@app.route('/')
def index():
    """Index route which initialises global variables
    and returns the homepage"""
    print(f"Connection. PeekingDuck Running: {globals.ISACTIVE}")
    if globals.ISACTIVE == False:
        globals.initialise()
        return render_template('./index.html')
    return redirect('/lobby')  

@app.route('/lobby')
def send_to_lobby():
    return render_template('lobby.html')

@app.route('/errors')
def send_to_errors():
    return render_template('errors.html')

@app.route('/about')
def send_to_about():
    return render_template('about.html')

@socketio.on('start', namespace='/app')
def start():
    """When start button is clicked, WebSocket event is triggered
    which starts the main programme"""
    emit('kickout', broadcast=True)
    start_pipeline()

@socketio.on('disconnect', namespace='/app')
def kill_peeking_duck():
    """
    Listener that listens to disconnect events in the app page
    Activated when person disconnects to kill the PeekingDuck Pipeline
    """
    print('Disconnection.')
    if globals.ISACTIVE:
        # Kills PeekingDuck if PeekingDuck is running
        globals.killSwitch = True
        emit('peekingduckFree', broadcast=True)

@socketio.on('resetServer')
def reset_server():
    kill_peeking_duck()
    emit('forceKickout',broadcast=True)

### UI METHODS (FEEDBACK)
##########

@socketio.on('feedback', namespace='/app')
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


### UI METHODS (BUTTONS)
###########

@socketio.on('endExercise', namespace='/app')
def end_exercise():
    """Updates globals that exercise has ended so
    that the peekingduck backend knows to create a summary
    which can be retrieved by front end"""
    if not globals.exerciseEnded:
        globals.exerciseEnded = True
    # Add code to save exercise in a cookie

@socketio.on('changeExercise', namespace='/app')
def change_exercise(exerciseId):
    globals.currentExercise = int(exerciseId)
    globals.exerciseSelected = True

@socketio.on('changeDifficulty', namespace='/app')
def change_difficulty(difficulty):
    """Function that updates global variable
    for backend to receive when user changes difficulty
     in front end"""
    globals.difficulty = difficulty

### DATA METHODS
##########

@socketio.on('video', namespace='/app')
def handle_video(data):
    globals.url = data['url']

@socketio.on('message')
def handle_message(msg):
    send(msg, broadcast=True)

if __name__ == '__main__':
    # ssl_context=('cert.pem', 'key.pem')
    # debug=True
    # allow_unsafe_werkzeug=True
    # gunicorn -w 1 --threads 100 app:app 
    # use this command to run production ready server
    # ssl_context=('cert.pem', 'key.pem'), 
    socketio.run(app,  host="0.0.0.0", ssl_context=('cert.pem', 'key.pem'), allow_unsafe_werkzeug=True, debug=True)
