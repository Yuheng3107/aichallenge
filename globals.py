import numpy as np

def initialise():
    global img
    global repCount
    global feedback
    
    global runSwitch
    global currentExercise
    global exerciseSelected
    global exerciseEnded
    
    
    img = np.zeros((720, 1280, 3))
    repCount = 0
    feedback = ["Press Start"]
    
    runSwitch = False
    currentExercise = 0
    exerciseSelected = False
    exerciseEnded = False
