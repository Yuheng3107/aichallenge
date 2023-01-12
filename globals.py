import numpy as np

def initialise():
    global img
    global feedback
    global exerciseEnded

    exerciseEnded = False
    feedback = ["Please do the exercise stipulated"]
    img = np.zeros((720, 1280, 3))