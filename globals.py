
import numpy as np

def initialise():
    
### UI Variables
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
    global emotionFeedback
    """Emotion Feedback"""
    global difficulty
    """Experience level of person exercising, either 
    Beginner or Expert, default is Beginner"""


    img = np.zeros((720, 1280, 3),dtype=np.float32)
    exerciseSelected = False
    exerciseEnded = False

    repCount = 0
    runSwitch = False
    currentExercise = 0

    mainFeedback = ["Press Start"]
    repFeedback = []
    emotionFeedback = []
    difficulty = "Beginner"

