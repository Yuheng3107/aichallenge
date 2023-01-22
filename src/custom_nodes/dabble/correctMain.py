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
        self.inPose = False
        """tracks if user is currently in key pose"""
        self.switchPoseCount = 0
        """counts how many frames you have switched pose for in order to account for anomalies"""

        # TO BE IMPORTED FROM NUMPY ARRAYS
        self.evalPoses = np.array([
            [0.0, 0.952426511314597, 2.0818875347174255, 1.3261204168307046, 0.6510736076524215, 2.399780721413044, 1.7346640543047198, 1.8333375840614206, 1.2664824256986646, 1.4384466286939788, 2.0818875347174255, 2.0276985464000967, 1.3271852367315855, 1.5392637179332127, 1.5331312146560117, 1.7207831542430525, 1.1049912979851086, 0.6039362393981718, 0.6735110882987303],
            [0.8334788287216585, 0.8329121004864121, 2.6238186548003744, 1.7955992943832724, 2.7837564294698547, 2.8104897880637982, 1.1570675859069883, 1.7602495274132577, 2.342429783867427, 1.6203743040026384, 2.626934103373849, 1.619022159869291, 
            2.58, 2.58, 2.55, 2.55, 
            1.6289927162507163, 0.04868708794174172, 1.6755387686585748],
            [0.6058237024724928, 0.8123420743245175, 1.829549427133411, 2.0250307847777487, 1.3227682033775756, 1.7756211818839254, 1.489401843315995, 1.8554985864833229, 1.6837441947257807, 2.0342313248855284, 1.1849714674830139, 1.9566211861067795, 2.6026996590121736, 2.9722683357046935, 2.1003751559196173, 3.0103488009021446, 1.0330164821889676, 1.4256641627881548, 1.690139665954699]])
        """
        Array(N,K) containing the correct poses
            N: number of exercises
            K: key angles (19)
        """

        self.angleWeights = np.array([
            [0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,1.,0.,1.,0.,1.,0.],
            [0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,1.,1.,1.,1.,0.,0.,0.],
            [0.,0.,10.,0.,0.,1.,0.,0.,0.,1.,0.,0.,0.,1,0.,1.,0.,1.,0.]])
        """
        Array(N,K) containing the weights that each angle should have in evaluation
            N: number of exercises
            K: key angles (19)
        """

        self.scoreThresholds = np.array([0.2,0.09,0.1])
        """
        Array(N) containing the Score Thresholds.
            N: number of exercises
            Score refers to the similarity of the user's pose to the correct pose.
                0 is completely similar, 1 is completely different.
        """

        self.angleThresholds = np.array([
            [0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.12,0.,0.12,0.,0.12,0],
            [0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.06,0.06,0.1,0.1,0.,0.,0.],
            [0.,0.,0.,0.,0.,0.1,0.,0.,0.,0.1,0.,0.,0.,0.1,0.,0.1,0.,0.1,0.]])
        """
        Array(N,K) containing the differences in angle required for feedback to be given
            N: number of exercises
            K: key angles (19)
        """

        self.evalRepTime = np.array([2,2,2])
        """
        Array(N) containing the minimum ideal rep times
            N: number of exercises
        """

        self.glossary = np.array(
            #Side Sqats
            [[['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],
            ['Butt not low enough ','Butt too low '],
            ['',''],
            ['Butt not low enough ','Butt too low '],
            ['',''],
            ['Back not straight enough ','Back too straight '],
            ['','']],
            #Front Squats
            [['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],
            ['Bending down too little ','Bending down too much '],
            ['Bending down too little ','Bending down too much '],
            ['Knees collapse inwards ','Bending down too much. Feet may be too wide apart. '],
            ['Knees collapse inwards ','Bending down too much. Feet may be too wide apart. '],
            ['',''],['',''],['','']],
            #Side Push-ups
            [['',''],['',''],['',''],['',''],['',''],
            ['Arms not wide enough ','Arms too wide '],
            ['',''],['',''],['',''],
            ['Arms not wide enough ','Arms too wide '],
            ['',''],['',''],['',''],
            ['Back too straight ','Back not straight enough '],
            ['',''],
            ['Knees too straightened ','Knees not straightened enough '],
            ['',''],
            ['Back too parllel with ground ','Back not parallel with ground '],
            ['','']]]
            )
        """
        Array(N) containing the text descriptions of each angle
            N: number of exercises
        """


### RESET METHODS
### These methods reset variables 
    
    def resetFrames(self):
        """
        Called when a rep is finished.
        Resets the stored angle data for that rep.
        """
        #frame stuff
        self.selectedFrames = np.zeros((200,19))
        """
        Array(X,K) containing the store of frames to be evaluated
            X: Number of frames (selectedFrameCount)
            K: key angles (19)
        """
        self.selectedFrameCount = 0
        """
        Number of frames in selectedFrames 
        """

    def resetAll(self):
        """
        Called when the a new exercise begins.
        Resets all exercise-related variables.
        """
        self.resetFrames()

        # reset angle-related variables
        self.smallErrorCount = np.zeros(19)
        """
        Array(K) containing the count of reps where angle K is too small
            K: key angles (19)
        """

        self.largeErrorCount = np.zeros(19)
        """
        Array(K) containing the count of reps where angle K is too large
            K: key angles (19)
        """

        self.repTimeError = 0
        """
        Count of reps where rep time is too short
        """

        self.repStartTime = 0
        """
        Timer to keep track of when the current rep started
        """

        self.perfectReps = 0
        """
        Count of perfect reps
        """
 
        self.invalidFrameCount = 0
        """
        Count of frames where user is not fully visible and key angles are missing
        """
        globals.repCount = 0



### EXERCISE METHODS
### These methods are called once per exercise.

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

    def summariseFeedback(self,smallErrorCount: np.ndarray, largeErrorCount: np.ndarray, perfectReps: int):
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
            feedback.append(f" {self.glossary[globals.currentExercise,i,0]} {count} times")
        for i,count in enumerate(largeErrorCount):
            #none of that error
            if count == 0:
                continue
            feedback.append(f" {self.glossary[globals.currentExercise,i,0]} {count} times")
        if self.repTimeError != 0:
            feedback.append(f" Rep times were too short {self.repTimeError} times")
        feedback.append(f" {perfectReps} perferct reps.")
        return feedback

### REP METHODS
### These methods are called once per rep.

    def finishRep(self):
        """
        Called when a rep is finished.
            Changes inPose to being in rest pose,
            gets the feedback for the rep and passes it to front-end,
            deletes all frame data of previous rep.
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

    def compareAngles(self, evalPose: np.ndarray[np.float64], angleThresholds: np.ndarray[np.float64]):
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
        x = np.average(filledselectedFrames,axis=0)
        print(f"curPose: {', '.join(str(angle) for angle in x)}")
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

    def giveFeedback(self, angleDifferences: np.ndarray[np.float64], timeDifference):
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

### FRAME METHODS
### These methods are called every frame

    def shouldSelectFrames(self, score, scoreThreshold):
        """
        Called every frame while rep detection is active.
        Used to determine whether to select a frame to be used for evaluation of errors.
        Args:
            score (float): score returned by comparePoses, 0 being completely similar and 1 being completely different.
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
            return 1
        return 0

    def checkPose(self, curPose:np.ndarray[np.float64], frameStatus:int):
        """
        Called every frame while rep detection is active.
        Used to change between user being in a key pose and rest pose. If user is in key pose, add valid frames to selectedFrames.
            Args:
                curPose (np array(19 float)): the current pose detected by the camera.
                frameStatus (int):  
        """
        if frameStatus == -1:
            return -1
        # switching from in key pose to rest pose
        if self.inPose == True:
            # add frame if not invalid
            self.selectedFrames[self.selectedFrameCount] = curPose
            self.selectedFrameCount += 1

            # if currently in key pose but person in a rest pose
            if frameStatus == 0:
                self.switchPoseCount += 1
                # if 5 rest frames in a row
                if self.switchPoseCount > 5:
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
        return None

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
            # Image data will be passed directly to globals.img
            # globals.img = inputs["img"]
            # Keypoints has a shape of (1, 17, 2)
            keypoints = inputs["keypoints"]
            
            # Calculates angles in radians of live feed
            curPose = processData(keypoints, globals.img.shape[0], globals.img.shape[1])
            score = comparePoses(self.evalPoses[globals.currentExercise],curPose, self.angleWeights[globals.currentExercise]) 
            
            """FRAME STATUS"""
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
            
          
            """DEBUG"""
            ## print(f"curPose: {', '.join(str(angle) for angle in curPose)}")
            print(f"score: {score}")
            ## print(f"angleDifferences: {angleDifferences}")   
            ## print(self.selectedFrameCount)
        
        return {}
