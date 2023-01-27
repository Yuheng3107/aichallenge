"""
correctMain.py
    - Rep Counting
    - Detect & Give Feedback for:
        - Key Poses
        - Rep Time
        - Emotions
helper.py
    - Calculating Key Angles
    - Comparing: 
        - Key Poses
        - Rep Time
        - Emotions
"""
from typing import Any, Dict, List
import time

import numpy as np

from peekingduck.pipeline.nodes.abstract_node import AbstractNode
from deepface import DeepFace
import cv2

import threading

from .helper import processData, comparePoses, compareAngles, compareTime, compareEmotions
import globals

class Node(AbstractNode):
    """This is a template class of how to write a node for PeekingDuck.

    Args:
        config (:obj:`Dict[str, Any]` | :obj:`None`): Node configuration.
    """

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        # initialize/load any configs and models here
        # configs can be called by self.<config_name> e.g. self.filepath
        # self.logger.info(f"model loaded with configs: config")

        super().__init__(config, node_path=__name__, **kwargs)
        globals.mainFeedback = ["Loading..."]

        self.resetAll()

        """REP COUNTER"""
        self.inPose = False
        """tracks if user is currently in key pose"""
        self.switchPoseCount = 0
        """counts how many frames you have switched pose for in order to account for anomalies"""

        # TO BE IMPORTED FROM NUMPY ARRAYS
        self.evalPoses = np.array([
            [0.,0.,0.,0.,1.75,0.,0.,0.,0.44,0.,0.],
            [0.,0.,0.,0.,0.,2.375,0.,2.264,0.,0.,0.],
            [0.,0.,0.,0.,2.825,0.,2.832,0.,1.583,0.,1.7]],dtype=np.float32)
        
        """
        Array(N,K) containing the correct poses
            N: number of exercises
            K: key angles (11)
        """

        self.angleWeights = np.array([
            [0.,0.,0.,0.,1.,0.,0.,0.,1.,0.,0.],
            [0.,0.,0.,0.,0.,1.,0.,1.,0.,0.,0.],
            [0.,0.,0.,0.,0.,0.,0.,0.,1.,0.,10.]],dtype=np.float32)
        
        """
        Array(N,K) containing the weights that each angle should have in evaluation
            N: number of exercises
            K: key angles (11)
        """

        self.scoreThresholds = np.array([0.19,0.17,0.06],dtype=np.float32)
        """
        Array(N) containing the Score Thresholds.
            N: number of exercises
            Score refers to the similarity of the user's pose to the correct pose.
                0 is completely similar, 1 is completely different.
        """

        self.angleThresholds = np.array([
            [0.,0.,0.,0.,0.14,0.,0.,0.,0.13,0.,0.],
            [0.,0.,0.,0.,0.,0.33,0.,0.4,0.,0.,0.],
            [0.,0.,0.,0.,0.,0.,0.,0.,0.08,0.,0.25]],dtype=np.float32)
        """
        Array(N,K) containing the differences in angle required for feedback to be given
            N: number of exercises
            K: key angles (11)
        """

        self.evalRepTime = np.array([3.5,3.5,2.5],dtype=np.float32)
        """
        Array(N) containing the minimum ideal rep times
            N: number of exercises
        """

        self.emotionThresholds = np.array([30,30,50],dtype=np.float32)
        """
        Arary(4) containing the thresholds for the various emotions
            Angry, Neutral, Sad, Disgust
        """

        self.glossary = np.array(
            #Side Squats
            [[['',''],['',''],['',''],['',''],
            ['Butt not low enough ','Butt too low '],
            ['',''],['',''],['',''],
            ['Leaning forward too much ','Back too straight '],
            ['',''],['','']],
            #Front Squats
            [['',''],['',''],['',''],['',''],['',''],
            ['Knees collapse inwards. ','Feet may be too wide apart. '],
            ['',''],
            ['Bending down too little. ','Bending down too much. '],
            ['',''],['',''],['','']],
            #Side Push-ups
            [['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],
            ['Back too straightened ','Back sagging '],
            ['',''],
            ['legs not parallel with ground ','Legs too parallel with ground ']]])
        """
        Array(N) containing the text descriptions of each angle
            N: number of exercises
        """
        if globals.displayVideoOnBackend:
            cv2.destroyAllWindows()
        

### RESET METHODS
### These methods reset variables 
    
    def resetFrames(self):
        """
        Resets the stored angle data for that rep.
            Called: when a rep is finished.
        """
        ### EXERCISE VARIABLES
        self.selectedFrames = np.zeros((200,11),dtype=np.float32)
        """
        Array(X,K) containing the store of frames to be evaluated
            X: Maximum number of frames the buffer stores (maximum selectedFrameCount size)
            K: key angles (11)
        """
        self.selectedFrameCount = 0
        """X - Number of frames in selectedFrames """

        ### EMOTION VARIABLES
        self.frameCount = 0
        """Frame Count for Emotions"""

        self.selectedEmotionFrames = np.zeros((100,7),dtype=np.float32)
        """
        Array(X,K) containing the store of frames to be evaluated
            X: Maximum number of frames buffer stores (maximum selectedEmotionFrameCount size)
            K: No. of emotions (7 possible emotions), angry, disgust, fear, happy, sad, surprise, neutral
        """

        self.selectedEmotionFrameCount = 0
        """X - Number of frames in selectedEmotionFrames"""

    def resetAll(self):
        """
        Resets all exercise-related variables.
            Called: when new exercise begins.
        """
        self.resetFrames()

        # reset angle-related variables
        self.smallErrorCount = np.zeros(11,dtype=int)
        """
        Array(K) contains the count of reps where angle K is too small
            K: key angles (11)
        """

        self.largeErrorCount = np.zeros(11,dtype=int)
        """
        Array(K) containing the count of reps where angle K is too large
            K: key angles (11)
        """

        self.repTimeError = 0
        """Count of reps where rep time is too short"""

        self.repStartTime = 0
        """Timer to keep track of when the current rep started"""

        self.perfectReps = 0
        """Count of perfect reps"""
 
        self.invalidFrameCount = 0
        """Count of frames where user is not fully visible and key angles are missing"""

        globals.repCount = 0

### EXERCISE METHODS
### These methods are called once per exercise.

    def changeExercise(self):
        """
        Resets all exercise-related variables and then resumes running rep detection.
            Called: when new exercise begins. 
        """    
        self.resetAll()
        # change pose state
        self.inPose = False
        self.switchPoseCount = 0
        # check for invalid exercise
        if globals.currentExercise >= self.angleWeights.shape[0]:
            globals.currentExercise = 0
        # start exercise
        globals.runSwitch = True
        globals.mainFeedback = ["Exercise Begin"]
        return None
    
    def endExercise(self):
        """
        Blacks out image, stops running rep detection, and calls for a feedback summary
            Called: when exercise is finished. 
        """   
        globals.img = np.zeros((720, 1280, 3),dtype=np.float32)
        # turn off run
        globals.runSwitch = False
        # no reps detected
        if globals.repCount == 0:
            globals.mainFeedback = ["No Reps Detected"]
            return None
        globals.mainFeedback = self.summariseFeedback(self.smallErrorCount,self.largeErrorCount,self.perfectReps)
        return None

    def summariseFeedback(self,smallErrorCount: np.ndarray, largeErrorCount: np.ndarray, perfectReps: int):
        """
        Used to convert the rep feedback into a feedback summary for the user.
            Called: when exercise is finished. 

            Args:
                smallErrorCount (Array(11)[int]): number of times angle was too small
                largeErrorCount (Array(11)[int]): number of times angle was too large
                perfectReps (int): number of perfect reps (no errors)

            Returns:
                feedback (list (string)): errors made in rep
        """
        feedback = []
        for i,count in enumerate(smallErrorCount):
            #none of that error
            if count == 0:
                continue
            feedback.append(f" {self.glossary[globals.currentExercise,i,0]} {count} times")
        for i,count in enumerate(largeErrorCount):
            #none of that error
            if count == 0:
                continue
            feedback.append(f" {self.glossary[globals.currentExercise,i,1]} {count} times")
        if self.repTimeError != 0:
            feedback.append(f" Rep times were too short {self.repTimeError} times")
        feedback.append(f" {perfectReps} perfect reps.")
        return feedback

### REP METHODS
### These methods are called once per rep.

    def finishRep(self):
        """
        Changes inPose to being in rest pose, gets the feedback for the rep, then deletes all frame data of the rep.
            Called: when rep is finished.
        """
        repTime = time.time() - self.repStartTime
        #anomaly, rep time too short
        if repTime < 1.5:
            return None

        globals.repCount += 1
        
        ### Rep feedback
        timeDifference = compareTime(self.evalRepTime[globals.currentExercise],repTime)
        angleDifferences = compareAngles(self.evalPoses[globals.currentExercise], self.angleThresholds[globals.currentExercise],self.selectedFrames,self.selectedFrameCount)

        globals.repFeedback.append(self.giveFeedback(angleDifferences, timeDifference))
        """array that contains the feedback for each rep"""

        ### Emotion feedback
        emotionAverage = compareEmotions(self.selectedEmotionFrames,self.selectedEmotionFrameCount)
        emotionFeedback, currentEmotion = self.emotionFeedback(emotionAverage,self.emotionThresholds)
        if currentEmotion != 0:
            globals.emotionFeedback = emotionFeedback
            globals.currentEmotion = currentEmotion
        print(f"Emotions: {emotionAverage}")
        self.resetFrames()

        # change pose state
        self.inPose = False
        self.switchPoseCount = 0

        return None

    def middleOfRep(self):
        """
        Changes inPose to being in key pose.
            Called: when user enters the key pose (at the middle of the rep).
        """
        # timer
        self.repStartTime = time.time()
        # change pose state
        self.inPose = True
        self.switchPoseCount = 0
        return None 

    def giveFeedback(self, angleDifferences: np.ndarray, timeDifference:bool):
        """
        Used to process angle data into text feedback to feed to front-end
            Called: when rep is finished.

            Args:
                angleDifferences (Array(11)[float]): angle differences, positive is too large, negative is too small, 0 is no significant difference
                timeDifference (bool): time difference, 1 is too short, 0 is no errors
                    
            Returns:
                feedback (string): errors made in rep
        """
        feedback = f"Rep {globals.repCount}: "

        #check for no frames
        if angleDifferences[0] == -99:
            feedback += "No Frames Detected"
            return feedback
        angleDifferences /= np.pi

        # hasError tracks if there is any feedback
        hasError = False
        for i, difference in enumerate(angleDifferences):
            if difference == 0.:
                continue
            hasError = True
            if (difference > 0):
                # angle needs to be smaller, as it is larger than ideal pose
                self.smallErrorCount[i] += 1
                feedback += self.glossary[globals.currentExercise,i,0]
            else:
                # angle needs to be greater, as it is smaller than ideal pose
                self.largeErrorCount[i] += 1
                feedback += self.glossary[globals.currentExercise,i,1]

        if timeDifference == 1:
            # time error
            hasError = True
            self.repTimeError += 1
            feedback += "Rep time was too short. "

        if hasError == False:
            # perfect rep
            self.perfectReps += 1
            feedback += "Perfect!"
        return feedback

    def emotionFeedback(self,emotionAverage:np.ndarray,emotionThreshold:np.ndarray):
        """
        Used to process emotion data into text feedback to feed to front-end
            Called: when rep is finished.

            Args:
                emotionAverage (Array(7)[float]): emotion confidence, 100 is maximum confidence, 0 is no confidence
                emotionThreshold (float): threshold beyond which emotions are considered significant
                    
            Returns:
                feedback (string): emotions displayed in rep & related feedback
                currentEmotion (int): ID of emotion
        """
        # check for no Face
        if emotionAverage[0] == -99:
            feedback = "No Face Detected"
            currentEmotion = -1
            return feedback, currentEmotion

        feedback = ""
        currentEmotion = 0

        ### angry, disgust, fear, happy, sad, surprise, neutral
        # if fearful/sad for some reason, idek
        if emotionAverage[2] + emotionAverage[4] > emotionThreshold[2]:
            feedback += "Stress detected. "
            currentEmotion += 2

        # if angry/happy, exercise is rigorous (grimace is identified by programme as happy)
        if emotionAverage[0] + emotionAverage[3] > emotionThreshold[0]:
            feedback += "Fatigue detected. "
            currentEmotion += 1

            if globals.difficulty == "Beginner":
                feedback += "Consider resting to prevent injury. "
            if globals.difficulty == "Expert":
                feedback += "Continue to train to failure for maximum results. "
        
        if currentEmotion != 0:
            return feedback, currentEmotion

        # if neutral, recommend continue
        if emotionAverage[6] > emotionThreshold[1]:
            feedback = "No Fatigue detected. Continue training. "
            currentEmotion = 4

        return feedback, currentEmotion


### FRAME METHODS
### These methods are called every frame

    def shouldSelectFrames(self, score, scoreThreshold):
        """
        Used to determine whether to select a frame to be used for evaluation of errors.
            Called: every frame while rep detection is active.

            Args:
                score (float): score returned by comparePoses, 0 being completely similar and 1 being completely different.
                scoreThreshold (float): the threshold within which score has to be for the frame to be selected.

            Returns:
                output (int): 1 if selected, 0 if not selected, 2 if selectedFrames is full, -1 if invalid
        """

        # error catch for invalid frame
        if score == -1:
            return -1
        # check if selectedFrames is full
        if self.selectedFrameCount == self.selectedFrames.shape[0]-1:
            return 2
        # test if score is lesser than threshold
        if score < scoreThreshold:
            return 1
        return 0

    def checkPose(self, curPose:np.ndarray, frameStatus:int):
        """
        Used to change between user being in a key pose and rest pose. If user is in key pose, add valid frames to selectedFrames.
            Called: every frame while rep detection is active.

            Args:
                curPose (Array(11)[float]): the current pose detected by the camera.
                frameStatus (int):  
        """
        if frameStatus == -1:
            return -1
        if frameStatus == 2:
            return 2
        # switching from in key pose to rest pose
        if self.inPose == True:
            # add frame if not invalid
            self.selectedFrames[self.selectedFrameCount] = curPose
            self.selectedFrameCount += 1

            # if currently in key pose but person in a rest pose
            if frameStatus == 0:
                self.switchPoseCount += 1
                # if 5 rest frames in a row
                if self.switchPoseCount > 10:
                    # transition into rest pose
                    self.finishRep()
                    
            # reset switchPoseCount
            if frameStatus == 1:
                self.switchPoseCount = 0

        # switching from rest pose to in key pose
        if self.inPose == False:
            # if currently in rest pose but person in a key pose
            if frameStatus == 1:
                self.switchPoseCount += 1
                # if 5 pose frames in a row
                if self.switchPoseCount > 4:
                    # transition into key pose
                    self.middleOfRep()

            # reset switchPoseCount
            if frameStatus == 0:
                self.switchPoseCount = 0
        return None

### EMOTIONS METHODS
### These methods are for emotion detection

    def detectEmotion(self):
        """
        Runs face analysis if there is a face in frame, then adds the results to selectedEmotionFrames.
            Called: every 5 frames while rep detection is active. 
        """
        # Gets dominant emotion
        try:
            emotions = DeepFace.analyze(globals.img, actions= ['emotion'], enforce_detection=True)['emotion']
            self.selectedEmotionFrames[self.selectedEmotionFrameCount] = list(emotions.values())
            self.selectedEmotionFrameCount += 1
            
        except:
            pass

### RUN

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:  # type: ignore
        """
        This node evaluates the similarity between the current pose (curPose)
        and the crucial pose (evalPose) to decide whether or not to select the frame.

        If it selects the frame, it will then compare the current pose to ideal pose, 
        then store the angleDifferences to be processed when the rep is completed.

        It also evaluates the emotions of the user to determine level of workout.

        Args:
            inputs (dict): Dictionary with keys "img", "keypoints".

        Returns:
            outputs (dict): empty.
        """
        # Added predefined global because it doesn't work on some OS i.e macOS
        if globals.displayVideoOnBackend:
            cv2.imshow("image",globals.img)
            cv2.waitKey(1)
        
        ### UI METHODS
        if globals.currentExercise == -1:
            globals.mainFeedback = ["Please Select Exercise."]

        if globals.exerciseSelected:
            self.changeExercise()
            globals.exerciseSelected = False

        if globals.exerciseEnded:
            self.endExercise()
            globals.exerciseEnded = False

        ### COMPUTATIONAL METHODS
        if globals.runSwitch:
            # Keypoints has a shape of (1, 17, 2)
            keypoints = inputs["keypoints"]
            # Calculates angles in radians of live feed
            curPose = processData(keypoints, globals.img.shape[0], globals.img.shape[1])
            score = comparePoses(self.evalPoses[globals.currentExercise],curPose, self.angleWeights[globals.currentExercise]) 
            
            # FRAME STATUS
            frameStatus = self.shouldSelectFrames(score, self.scoreThresholds[globals.currentExercise])

            #default message
            globals.mainFeedback = ["Exercise in progress"]

            if frameStatus == 2:
                globals.mainFeedback = ["Frames filled up"]
            
            # check for not in frame
            if frameStatus == -1:
                self.invalidFrameCount += 1
                if self.invalidFrameCount > 6:
                    globals.mainFeedback = ["Please position yourself in the image"]
            else:
                self.invalidFrameCount = 0
                self.checkPose(curPose,frameStatus)
            
        ### EMOTION METHODS
            self.frameCount += 1
            if self.frameCount == 5:
                thread = threading.Thread(target=self.detectEmotion, name='thread', daemon=True)
                self.frameCount = 0
                thread.start()

            """DEBUG"""
            # print(f"curPose: {', '.join(str(angle) for angle in curPose)}")
            print(f"score: {score}")
            # print(f"test: {curPose[10]}")
            ## print(f"angleDifferences: {angleDifferences}")   
            ## print(self.selectedFrameCount)
        print(f"shape:{globals.img.shape}")
        
        return {}
