
import numpy as np

def initialise():
<<<<<<< HEAD

    global url
    """url thats stores jpeg of current frame"""
=======
    
### UI Variables
>>>>>>> main
    global img
    global exerciseSelected
    """True when button to select exercise is pressed"""
    global exerciseEnded
    """True when button to end exercise is pressed"""

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
    global stressFeedback
    """Emotion Feedback"""
    global difficulty
    """Experience level of person exercising, either 
    Beginner or Expert, default is Beginner"""
<<<<<<< HEAD
    url = None
=======


>>>>>>> main
    img = np.zeros((720, 1280, 3),dtype=np.float32)
    exerciseSelected = False
    exerciseEnded = False

    repCount = 0
    runSwitch = False
    currentExercise = 0

    mainFeedback = ["Press Start"]
    repFeedback = []
    stressFeedback = []
    difficulty = "Beginner"

