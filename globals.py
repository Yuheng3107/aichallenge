
import numpy as np

def initialise():
    global img
    global repCount
    global mainFeedback
    global repFeedback
    
    global runSwitch
    global currentExercise
    global exerciseSelected
    global exerciseEnded
    
    global emotionsFreq
    global emotions

    img = np.zeros((720, 1280, 3),dtype=np.float32)
    repCount = 0
    mainFeedback = ["Press Start"]
    repFeedback = []
    
    runSwitch = False
    currentExercise = 0
    exerciseSelected = False
    exerciseEnded = False
    emotions = {'angry': 0, 'disgust': 1, 'fear': 2, 'happy': 3, 'sad': 4, 'surprise': 5, 'neutral': 6}
    emotionsFreq = np.zeros(7)
