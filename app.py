from flask import Flask, render_template
from main import main
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('./index.html')

@app.route("/video")
def play_video():
    main()