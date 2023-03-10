
import numpy as np
import sys
def superInitialise():
    global ISACTIVE
    
    ### Sever Setting variables
    global displayVideoOnBackend

    ISACTIVE = False
    displayVideoOnBackend = True
    if sys.platform == "darwin":
        displayVideoOnBackend = False
def initialise():

### UI Variables
    global url
    global img
    global exerciseSelected
    """True when button to select exercise is pressed"""
    global exerciseEnded
    """True when button to end exercise is pressed"""
    global killSwitch
    """Switch to kill PeekingDuck"""
    global isKilled
    """Verify if PeekingDuck successfully killed"""
### Exercise Variables
    global repCount
    global runSwitch
    """True when exercise is running"""
    global currentExercise
    """number from 0 to N representing the ID of the exercise"""


### Feedback Variables
    global mainFeedback
    """General Feedback + Summary Feedback"""
    global repFeedback
    """Rep Feedback"""
    global emotionFeedback
    """Emotion Feedback"""
    global currentEmotion
    """
    ID of emotion detected.
        -1: no face
        0: no emotion
        1: fatigue
        2: stress
        3: stress & fatigue
        4: neutral
    """
    global difficulty
    """Experience level of person exercising, either 
    Beginner or Expert, default is Beginner"""
    url = None
    img = np.zeros((720, 1280, 3),dtype=np.float32)
    exerciseSelected = False
    exerciseEnded = False


    repCount = 0
    runSwitch = False
    currentExercise = -1

    mainFeedback = ["Press Start"]
    repFeedback = []
    emotionFeedback = ""
    difficulty = "Beginner"
    killSwitch = False
    isKilled = False
    
