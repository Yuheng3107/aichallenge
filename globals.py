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
    global emotion

    img = np.zeros((720, 1280, 3),dtype=np.float32)
    repCount = 0
    mainFeedback = ["Press Start"]
    repFeedback = []
    
    runSwitch = False
    currentExercise = 0
    exerciseSelected = False
    exerciseEnded = False
    emotion = "no emotions detected"
