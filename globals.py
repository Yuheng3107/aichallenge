
import numpy as np

def initialise():
    global img
    global repCount
    global mainFeedback
    """General Feedback + Summary Feedback"""
    global repFeedback
    """Rep Feedback"""
    
    global runSwitch
    """True when exercise is running"""
    global currentExercise
    """number from 0 to N representing the ID of the exercise"""
    global exerciseSelected
    """True when button to select exercise is pressed"""
    global exerciseEnded
    """True when button to end exercise is pressed"""
    global emotionsFreq
    global emotions
    global isStressed

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
    isStressed = False