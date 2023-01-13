import numpy as np

def initialise():
    global img
    global feedback
    
    global runSwitch
    global currentExercise
    global exerciseSelected
    global exerciseEnded
    
    
    img = np.zeros((720, 1280, 3))
    feedback = ["Please do the exercise stipulated"]
    
    runSwitch = True
    currentExercise = 0
    exerciseSelected = False
    exerciseEnded = False
