"""
Node template for creating custom nodes.
"""

from typing import Any, Dict, List
import time
import numpy as np
from peekingduck.pipeline.nodes.abstract_node import AbstractNode
from .helper import processData, comparePoses
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
        globals.mainFeedback = ["Please Select Exercise"]

        self.resetAll()

        """REP COUNTER"""
        # inPose tracks if you are currently in evalPose
        self.inPose = False
        # switchPoseCount counts how many frames you have switched pose for in order to account for anomalies
        self.switchPoseCount = 0

        """TO BE IMPORTED FROM NUMPY ARRAYS"""
        self.evalPoses = np.array([[0.,0.97758846,1.29457385,0.69776272,2.34189554,0.53291666
            ,0.41126802,1.30916096,1.43501846,2.0414656,1.10012705,1.63351656
            ,1.59583319,0.97556597,0.,1.8165275,1.08770129,0.53107237
            ,0.71953291],
            [2.60624252,1.85682613,1.85174129,2.18443126,2.04166497,0.70646575
            ,0.69706771,1.21146002,1.26237227,1.45134487,1.69024778,2.21142086
            ,2.29314475,1.36090297,2.10783731,2.34847681,1.63807976,0.10311005
            ,1.53496971]])
        self.angleWeights = np.array([[0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,1.,0.,0.,1.,0.,1.,0.],[0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,1.,1.,0.,1.,1.,0.,0.,0.,0.]])
        self.scoreThresholds = np.array([0.2,0.08])
        self.angleThresholds = np.array([[0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.1,0.,0.,0.1,0.,0.1,0],[0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.05,0.05,0.,0.08,0.08,0.,0.,0.,0.]])
        self.evalRepTime = np.array([2,2])
        # Probably will read glossary from csv in the end
        # Glossary will map angle_id to corresponding angle
        self.glossary = np.array(['leftEar-nose-midShoulder',
            'rightEar-nose-midShoulder',
            'nose-midShoulder-leftShoulder',
            'nose-midShoulder-rightShoulder',
            'midShoulder-leftShoulder-leftElbow',
            'midShoulder-rightShoulder-rightElbow',
            'nose-midShoulder-leftElbow',
            'nose-midShoulder-rightElbow',
            'leftShoulder-leftElbow-leftWrist',
            'rightShoulder-rightElbow-rightWrist',
            'Chest - Left Thigh',
            'Chest - Right Thigh',
            'Chest - Thigh',
            'Left Thigh - Leg',
            'Right Thigh - Leg',
            'Thigh - Leg',
            'nose-midShoulder-midHip',
            'Vertical - Back',
            'vertical(nose)-nose-midShoulder'])

    """
    RESET METHODS
    These methods reset variables
    """  
    
    def resetFrames(self):
        """
        Called when a rep is finished.
        Resets the stored angle data for that rep.
        """
        #frame stuff
        self.selectedFrames = np.zeros((200,19))
        self.selectedFrameCount = 0

    def resetAll(self):
        """
        Called when the a new exercise begins.
        Resets all exercise-related variables.
        """
        self.resetFrames()

        # reset angle-related variables
        self.smallErrorCount = np.zeros(19)
        self.largeErrorCount = np.zeros(19)
        # reset timer-related variables
        self.repTimeError = 0
        self.repStartTime = 0
        # reset perfect reps
        self.perfectReps = 0

        # reset user out of frame count
        self.invalidFrameCount = 0
        globals.repCount = 0


    """
    EXERCISE METHODS
    These methods are called once per exercise.
    """

    def changeExercise(self):
        """
        Called when a new exercise begins.
        Resets all exercise-related variables and then resumes running rep detection.
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
        Called when the exercise is finished.
        Blacks out image, stops running rep detection, and calls for a feedback summary
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

    def summariseFeedback(self,smallErrorCount: np.float64, largeErrorCount: np.float64, perfectReps):
        """
        Called when the exercise is finished.
        Used to convert the rep feedback into a feedback summary for the user.
            Args:
                smallErrorCount (np array(19 int)): number of times angle was too small
                largeErrorCount (np array(19 int)): number of times angle was too large
                perfectReps (int): number of perfect reps (no errors)
                    
            Returns:
                feedback (list (string)): errors made in rep
        """
        feedback = []
        for i,count in enumerate(smallErrorCount):
            #none of that error
            if count == 0:
                continue
            feedback.append(f" {self.glossary[i]} angle needed to be smaller {count} times")
        for i,count in enumerate(largeErrorCount):
            #none of that error
            if count == 0:
                continue
            feedback.append(f" {self.glossary[i]} angle needed to be larger {count} times")
        if self.repTimeError != 0:
            feedback.append(f" Rep times were too short {self.repTimeError} times")
        feedback.append(f" {perfectReps} perferct reps.")
        return feedback

    
    """
    REP METHODS
    These methods are called once per rep.
    """

    def finishRep(self):
        """
        Called when a rep is finished.
        Changes inPose to being in rest pose
        Gets the feedback for the rep and passes it to front-end, then deletes all frame data of previous rep.
        """
        globals.repCount += 1
        # timer
        repTime = time.time() - self.repStartTime
        timeDifference = self.compareTime(self.evalRepTime[globals.currentExercise],repTime)
        # angles
        angleDifferences = self.compareAngles(self.evalPoses[globals.currentExercise], self.angleThresholds[globals.currentExercise])
        # repFeedback is an array that contains the feedback for each rep
        globals.repFeedback.append(self.giveFeedback(angleDifferences, timeDifference))
        # reset frames
        self.resetFrames()
        # change pose state
        self.inPose = False
        self.switchPoseCount = 0

        return None

    def middleOfRep(self):
        """
        Called when user enters the key pose (at the middle of the rep).
        Changes inPose to being in key pose.
        """
        # timer
        self.repStartTime = time.time()
        # change pose state
        self.inPose = True
        self.switchPoseCount = 0
        return None

    def compareAngles(self, evalPose: np.float64, angleThresholds: np.float64):
        """
        Called when a rep is finished.
        Used to compare between ideal and observed angles in user's pose
            Args:
                evalPose (np array(19 float)): the ideal pose to be compared against.
                curPose (np array(19 float)): the current pose detected by the camera.
                angleThresholds (np array(19 float)): the threshold of angle differences

            Returns:
                angleDifferences (np array(19 float)): angle differences, positive is too large, negative is too small, 0 is no significant difference    
        """
        angleDifferences = np.zeros(evalPose.shape) 
        # check for 0 frames
        if self.selectedFrameCount == 0:
            return np.array([-99])
        # remove empty data
        filledselectedFrames = self.selectedFrames[0:self.selectedFrameCount]
        # positive is too large, negative is too small 
        differences = np.average(filledselectedFrames, axis=0) - evalPose

        """
        CREATING NEW EXERCISES
        """
        print(np.average(filledselectedFrames,axis=0))
        print(differences)

        for i, x in enumerate(differences):
            if angleThresholds[i] == 0.:
                continue
            # if difference is significant enough
            if abs(x) > angleThresholds[i]:
                angleDifferences[i] = differences[i]
        return angleDifferences
    
    def compareTime(self, evalTime, repTime):
        """
        Called when a rep is finished
        Evaluates if rep time is too short
        """
        if repTime < evalTime:
            # rep time is too short
            return 1
        return 0

    def giveFeedback(self, angleDifferences: np.float64, timeDifference):
        """
        Called when a rep is finished.
        Used to convert angle data into text feedback to feed to front-end
            Args:
                angleDifferences (np array(19 float)): angle differences, positive is too large, negative is too small, 0 is no significant difference
                    
            Returns:
                feedback (string): errors made in rep
        """
        #check for error in compareAngles
        feedback = f"Rep {globals.repCount}: "
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
                feedback += f"{self.glossary[i]} angle needs to be smaller. "
            else:
                # angle needs to be greater, as it is smaller than ideal pose
                self.largeErrorCount[i] += 1
                feedback += f"{self.glossary[i]} angle needs to be larger. "

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

    """
    FRAME METHODS
    These methods are called every frame
    """

    def selectFrames(self, score, curPose: np.float64, scoreThreshold):
        """
        Called every frame while rep detection is active.
        Used to determine whether to select a frame to be used for evaluation of errors. If selected, frame is added to selectedFrames array.
        Args:
            score (float): score returned by comparePoses, 0 being completely similar and 1 being completely different.
            curPose (np array(19 float)): the current pose detected by the camera.
            scoreThreshold (float): the threshold within which score has to be for the frame to be selected.

        Returns:
            output (int): 1 if frame is selected, 0 if frame is not selected 
                2 if selectedFrames is full, -1 if frame is invalid
        """

        # error catch for invalid frame
        if score == -1:
            return -1
        # check if selectedFrames is full
        if self.selectedFrameCount == self.selectedFrames.shape[0]-1:
            return 2
        # test if score is lesser than threshold
        if score < scoreThreshold:
            self.selectedFrames[self.selectedFrameCount] = curPose
            self.selectedFrameCount += 1
            return 1
        return 0

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:  # type: ignore
        """
        This node evaluates the similarity between the current pose (curPose)
        and the crucial pose (evalPose) to decide whether or not to select the frame.

        If it selects the frame, it will then compare the current pose to ideal pose, 
        then store the angleDifferences to be processed when the rep is completed.

        Args:
            inputs (dict): Dictionary with keys "img", "keypoints".

        Returns:
            outputs (dict): empty.
        """


        """UI METHODS"""
        if globals.exerciseSelected:
            self.changeExercise()
            globals.exerciseSelected = False

        if globals.exerciseEnded:
            self.endExercise()
            globals.exerciseEnded = False

        """COMPUTATIONAL METHODS"""
        if globals.runSwitch:
            globals.img = inputs["img"]
            # Keypoints has a shape of (1, 17, 2)
            keypoints = inputs["keypoints"]
            
            # Calculates angles in radians of live feed
            curPose = processData(keypoints, globals.img.shape[0], globals.img.shape[1])
            score = comparePoses(self.evalPoses[globals.currentExercise],curPose, self.angleWeights[globals.currentExercise]) 
            
            """FRAME STATUS"""
            frameStatus = self.selectFrames(score, curPose, self.scoreThresholds[globals.currentExercise])

            # switching from in key pose to rest pose
            if self.inPose == True:
                
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
                    if self.switchPoseCount > 6:
                        # transition into key pose
                        self.middleOfRep()

                # reset switchPoseCount
                if frameStatus == 0:
                    self.switchPoseCount = 0

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
            
          
            """DEBUG"""
            ## print(f"curPose: {curPose}")
            ## print(f"score: {score}")
            ## print(f"angleDifferences: {angleDifferences}")   
            ## print(self.selectedFrameCount)
        
        return {}
