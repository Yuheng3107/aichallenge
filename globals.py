import numpy as np

def initialise():
    global img
    global feedback
    feedback = []
    img = np.zeros((720, 1280, 3))