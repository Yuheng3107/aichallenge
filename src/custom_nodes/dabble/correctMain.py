"""
Node template for creating custom nodes.
"""

from typing import Any, Dict, List
import numpy as np
from peekingduck.pipeline.nodes.abstract_node import AbstractNode
from .helper import processData
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

        """ERROR TRACKING"""
        # angle needs to be smaller
        self.smallErrorCount = np.zeros((100,19))
        # angle needs to be larger
        self.largeErrorCount = np.zeros((100,19))
        # perfect rep counter
        self.perfectReps = 0

        """FRAME SELECTION"""
        self.selectedFrames = np.zeros((100,19))
        self.selectedFrameCount = 0

        """REP COUNTER"""
        globals.repCount = 0
        # inPose tracks if you are currently in evalPose
        self.inPose = False
        # switchPoseCount counts how many frames you have switched pose for in order to account for anomalies
        self.switchPoseCount = 0
        self.invalidFrameCount = 0

        """TO BE IMPORTED FROM NUMPY ARRAYS"""
        self.evalPoses = np.array([[0.,0.98390493,1.51094115,1.6306515,0.26590253,2.81373512
            ,0.26590253,0.32785753,1.02067892,1.59934942,1.35720082,1.78439183
            ,0.79900877,1.33113154,1.22965078,1.52982444,0.90668716,2.49591843
            ,0.26101294]])
        self.angleWeights = np.array([[0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,1.,0.,1.,0.,1.,0.]])
        self.scoreThreshold = 0.2
        self.angleThresholds = np.array([[0,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.1,0.,0.12,0.,0.1,0]])
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
            'midShoulder-midHip-leftHip',
            'midShoulder-midHip-rightHip',
            'leftShoulder-leftHip-leftKnee',
            'Chest and Thigh',
            'leftHip-leftKnee-leftAnkle',
            'Thigh and Leg',
            'nose-midShoulder-midHip',
            'Vertical and Back',
            'vertical(nose)-nose-midShoulder'])  
    
    """UI METHODS"""

    def finishRep(self):
        """
        Called when a rep is finished.
        Gets the feedback for the rep and passes it to front-end, then deletes all frame data of previous rep.
        """
        globals.repCount += 1
        angleDifferences = self.compareAngles(self.evalPoses[globals.currentExercise], self.angleThresholds[globals.currentExercise])
        # repFeedback is an array that contains the feedback for each rep
        globals.repFeedback.append(self.giveFeedback(angleDifferences))
        # reset frames
        self.selectedFrames = np.zeros((100,19))
        self.selectedFrameCount = 0
        return None
    
    def changeExercise(self):
        """
        Called when a new exercise begins.
        Resets all exercise-related variables and then resumes running rep detection.
        """    
        # reset frame-related variables
        self.selectedFrames = np.zeros((100,19))
        self.selectedFrameCount = 0
        self.frameCount = 0
        # reset feedback-related variables
        self.smallErrorCount = np.zeros(19)
        self.largeErrorCount = np.zeros(19)
        self.perfectReps = 0

        globals.repCount = 0
        # check for invalid exercise
        if globals.currentExercise >= self.angleWeights.shape[0]:
            globals.currentExercise = 0
        # start exercise
        globals.runSwitch = True
        globals.mainFeedback = ["Exercise Begin"]
        return None
    
    
    def endExercise(self):
        """
        Called when the current exercise ends.
        Blacks out image, stops running rep detection, and calls for a feedback summary
        """   
        globals.img = np.zeros((720, 1280, 3))
        # turn off run
        globals.runSwitch = False
        # no reps detected
        if globals.repCount == 0:
            globals.mainFeedback = ["No Reps Detected"]
            return None
        globals.mainFeedback = self.summariseFeedback(self.smallErrorCount,self.largeErrorCount,self.perfectReps)
        return None

    """COMPUTATIONAL METHODS"""

   
    def comparePoses(self, evalPose: np.float64, curPose: np.float64, angleWeights: np.float64):
        """
        Called every frame while rep detection is active.
        Used to determine if user is currently in a certain pose.
        Args:
            evalPose (np array(19 float)): the ideal pose to be compared against.
            curPose (np array(19 float)): the current pose detected by the camera.

        Returns:
            score (float): a score between 0 and 1, 0 being completely similar and 1 being completely different.
                -1 if curPose is missing crucial angle data.
        """    
        # for data security 
        score = 0.
        
        angleWeightSum = np.sum(angleWeights)
        if angleWeightSum == 0:
            return -1
        for i,x in enumerate(curPose):
            if angleWeights[i] == 0:
                continue
            if x == 0:
                # Check if peekingDuck missed out any useful 
                # keypoints, i.e no value but still have weight
                if angleWeights[i] != 0:
                    # Declare the frame invalid
                    return -1
                continue
            # explanation of formula:
                # abs(x-evalPose[i])/np.pi: diff betwn 2 angles on a scale of 0 to 1, 1 being 180 degrees
                # angleWeights[i]/angleWeightSum: weighted value of the current angle difference
            score += (abs(x-evalPose[i])/np.pi) * (angleWeights[i]/angleWeightSum)
        return score

    
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

    # returns np.arr(19) of differences, 0 is no significant difference
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
        for i, x in enumerate(differences):
            if angleThresholds[i] == 0.:
                continue
            # if difference is significant enough
            if abs(x) > angleThresholds[i]:
                angleDifferences[i] = differences[i]
        return angleDifferences

    def giveFeedback(self, angleDifferences: np.float64):
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
        # hasError tracks if there is an error
        hasError = False
        for i, difference in enumerate(angleDifferences):
            if difference == 0.:
                continue
            hasError = True
            if (difference > 0):
                # angle needs to be smaller, as it is larger than ideal pose
                # 0 - 18 is angle needs to be smaller
                self.smallErrorCount[i] += 1
                feedback += f"Angle between {self.glossary[i]} needs to be smaller. "
            else:
                # angle needs to be greater, as it is smaller than ideal pose
                # 19 to 37 is angle needs to be larger
                self.largeErrorCount[i] += 1
                feedback += f"Angle between {self.glossary[i]} needs to be larger. "
        if hasError == False:
            # 38 is perfect rep
            self.perfectReps += 1
            feedback += "Perfect!"
        return feedback

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
            feedback.append(f"Angle between {self.glossary[i]} needed to be smaller {count} times. ")
        for i,count in enumerate(largeErrorCount):
            #none of that error
            if count == 0:
                continue
            feedback.append(f"Angle between {self.glossary[i]} needed to be larger {count} times. ")
        feedback.append(f"You did {perfectReps} reps perferctly. ")
        return feedback


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
            # add 1 to frameCount
            
            # Calculates angles in radians of live feed
            curPose = processData(keypoints, globals.img.shape[0], globals.img.shape[1])
            score = self.comparePoses(self.evalPoses[globals.currentExercise],curPose, self.angleWeights[globals.currentExercise]) 
            
            """FRAME STATUS"""
            frameStatus = self.selectFrames(score, curPose, self.scoreThreshold)

            # switching from in pose state to rest state
            if self.inPose == True:
                # if currently in pose state but person in a rest frame
                if frameStatus == 0:
                    self.switchPoseCount += 1
                    # if 5 rest frames in a row
                    if self.switchPoseCount > 5:
                        # transition into rest state
                        self.inPose = False
                        self.switchPoseCount = 0
                        self.finishRep()
                        
                # reset switchPoseCount
                if frameStatus == 1:
                    self.switchPoseCount = 0

            # switching from rest state to in pose state
            if self.inPose == False:
                # if currently in rest state but person in a pose frame
                if frameStatus == 1:
                    self.switchPoseCount += 1
                    # if 5 pose frames in a row
                    if self.switchPoseCount > 3:
                        # transition into pose state
                        self.inPose = True
                        self.switchPoseCount = 0
                # reset switchPoseCount
                if frameStatus == 0:
                    self.switchPoseCount = 0

            if frameStatus == 2:
                globals.mainFeedback = ["Frames filled up"]
            
            # check for not in frame
            if frameStatus == -1:
                self.invalidFrameCount += 1
                if self.invalidFrameCount > 10:
                    globals.mainFeedback = ["PUT UR ASS IN THE IMAGE"]
            else:
                self.invalidFrameCount = 0
            
          
            """DEBUG"""
            ## print(f"curPose: {curPose}")
            ## if score != -1:
                ## print(f"score: {score}")
                ## pass
            ## print(f"angleDifferences: {angleDifferences}")   
            ## print(self.selectedFrameCount)
        
        return {}
