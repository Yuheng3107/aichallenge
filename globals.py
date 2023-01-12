import numpy as np

def initialise():
    global img
    global feedback
    global exerciseEnded
    global runSwitch
    global currentExercise
    global mistakes

    exerciseEnded = False
    feedback = ["Please do the exercise stipulated"]
    img = np.zeros((720, 1280, 3))
    runSwitch = True
    currentExercise = 0
    mistakes = []