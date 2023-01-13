
import cv2
import json
from flask import Flask, render_template, Response, request
import globals
from main import main
app = Flask(__name__)



def gen():
    while True:
        
        ret, jpeg = cv2.imencode('.jpeg', globals.img)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
def index():
    globals.initialise()
    return render_template('./index.html')

@app.route('/start')
def start():
    
    main()

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/feedback')
def send_feedback():
    return json.dumps(globals.feedback)

@app.route('/endExercise')
def end_exercise():
    if not globals.exerciseEnded:
        globals.exerciseEnded = True
    return render_template('./index.html')

@app.route('/changeExercise', methods= ['POST'])
def changeExercise():
    exerciseId = request.form["exerciseId"]
    globals.currentExercise = exerciseId
    globals.exerciseSelected = True
    return ""

if __name__ == '__main__':
    app.run()
