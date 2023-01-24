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
            [1.5101271591974472, 1.4980141223917764, 2.9744070804606664, 0.6972723789351448, 0.4837195830264868, 2.2550842191658105, 0.4871277398325121, 0.48601296839902186, 0.9368117346906317, 1.5589928996090603, 2.1477453057967852, 1.7910356640090987, 1.336984596535936, 1.6832697218589587, 1.383993753712914, 1.6120344910706403, 1.9967021465554933, 0.4398586657270065, 1.6390865609852177],
            [2.5,2.4, 2.883816780362668, 1.8643469259111198, 2.997754635400291, 2.855449311474785, 1.1334077094891724, 1.578203583796112, 0.7839790321590494, 0.7821727442271517, 2.3850600370725807, 1.5656631300702746, 
            2.327, 2.327, 2.3, 2.3, 
            1.5596841017654897, 0.056053968019371674, 1.6157380697848598],
            [0.21767780038645262, 0.6919961585571482, 1.6839704162412432, 1.8539293248147957, 0.7079075377200521, 2.538111518193272, 1.8733032890931085, 1.983687965530557, 1.7986515332534698, 1.6412894658311044, 1.8598794860142835, 2.2558652786473097, 2.9200727069178956, 2.82527497539771, 2.6791168732640616, 2.8319761199989966, 0.9351479597160647, 1.5825368441775987, 1.0007917106164417]])
        """
        Array(N,K) containing the correct poses
            N: number of exercises
            K: key angles (19)
        """

        self.angleWeights = np.array([
            [0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,1.,0.,0.,0.,1.,0.],
            [1.,1.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.],
            [0.,0.,10.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,1.,0.,1.,0.,1.,0.]])
        """
        Array(N,K) containing the weights that each angle should have in evaluation
            N: number of exercises
            K: key angles (19)
        """

        self.scoreThresholds = np.array([0.2,0.14,0.06])
        """
        Array(N) containing the Score Thresholds.
            N: number of exercises
            Score refers to the similarity of the user's pose to the correct pose.
                0 is completely similar, 1 is completely different.
        """

        self.angleThresholds = np.array([
            [0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.14,0.,0.,0.,0.13,0],
            [0.12,0.15,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.],
            [0.,0.,0.1,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.18,0.,0.2,0.,0.16,0.]])
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
            ['',''],['',''],['',''],
            ['Back not straight enough ','Back too straight '],
            ['','']],
            #Front Squats
            [['Bending down too little. ','Bending down too much. '],['Knees collapse inwards. ','Bending down too much. Feet may be too wide apart. '],
            ['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['','']],
            #Side Push-ups
            [['',''],['',''],
            ['Legs too parallel with ground','legs not parallel with ground'],
            ['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],['',''],
            ['Back too straight ','Back not straight enough '],
            ['',''],
            ['Knees too straightened ','Knees too bent '],
            ['',''],
            ['Back too straightened ','Back sagging '],
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
                smallErrorCount (ndarray(19,dtype=int)): number of times angle was too small
                largeErrorCount (ndarray(19,dtype=int)): number of times angle was too large
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

    def compareAngles(self, evalPose: np.ndarray, angleThresholds: np.ndarray):
        """
        Called when a rep is finished.
        Used to compare between ideal and observed angles in user's pose
            Args:
                evalPose (ndarray(19,dtype=float)): the ideal pose to be compared against.
                curPose (ndarray(19,dtype=float)): the current pose detected by the camera.
                angleThresholds (ndarray(19,dtype=float)): the threshold of angle differences

            Returns:
                angleDifferences (ndarray(19,dtype=float)): angle differences, positive is too large, negative is too small, 0 is no significant difference    
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
        print(f"test: {x[10]}")

        for i, x in enumerate(differences):
            if angleThresholds[i] == 0.:
                continue
            # if difference is significant enough
            if abs(x) > angleThresholds[i]:
                angleDifferences[i] = differences[i]
        return angleDifferences
    
    def compareTime(self, evalTime:np.float64, repTime:np.float64):
        """
        Called when a rep is finished
        Evaluates if rep time is too short
        """
        if repTime < evalTime:
            # rep time is too short
            return 1
        return 0

    def giveFeedback(self, angleDifferences: np.ndarray, timeDifference:bool):
        """
        Called when a rep is finished.
        Used to convert angle data into text feedback to feed to front-end
            Args:
                angleDifferences (ndarray(19,dtype=float)): angle differences, positive is too large, negative is too small, 0 is no significant difference
                timeDifference (bool): time difference, 1 is too short, 0 is no errors
                    
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

        Returns:()
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

    def checkPose(self, curPose:np.ndarray, frameStatus:int):
        """
        Called every frame while rep detection is active.
        Used to change between user being in a key pose and rest pose. If user is in key pose, add valid frames to selectedFrames.
            Args:
                curPose (ndarray(19,dtype=float)): the current pose detected by the camera.
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
                if self.switchPoseCount > 5:
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
            # Image data will be passed directly to globals.img in app.py
            # Keypoints has a shape of (1, 17, 2)
            keypoints = inputs["keypoints"]
            globals.img = inputs["img"]
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
            # print(f"curPose: {', '.join(str(angle) for angle in curPose)}")
            # print(f"score: {score}")
            # print(f"test: {curPose[10]}")
            ## print(f"angleDifferences: {angleDifferences}")   
            ## print(self.selectedFrameCount)
            # print(f"shape:{globals.img.shape}")
        
        return {}
