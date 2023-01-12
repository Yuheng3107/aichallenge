"""
Node template for creating custom nodes.
"""

from typing import Any, Dict, List
import numpy as np
import csv
from peekingduck.pipeline.nodes.abstract_node import AbstractNode
from .helper import processData
import globals
class Node(AbstractNode):
    """This is a template class of how to write a node for PeekingDuck.

    Args:
        config (:obj:`Dict[str, Any]` | :obj:`None`): Node configuration.
    """

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)
        self.frames = np.zeros((10,19))
        self.frame_count = 0
        # initialize/load any configs and models here
        # configs can be called by self.<config_name> e.g. self.filepath
        # self.logger.info(f"model loaded with configs: config")

    def comparePoses(self, evalPose: np.float64, curPose: np.float64, angleWeights: np.float64):
        #for data security 
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

    # shifts selectFrames and adds curPose to the back of the array
        # returns True if frame is selected, False if frame is not selected
    def selectFrames(self, score, curPose: np.float64, scoreThreshold):
        #error catch for invalid frame
        if score == -1:
            return False
        # test if score is lesser than threshold
        if score < scoreThreshold:
            self.frames[:-1] = self.frames[1:]
            # replace the last entry with curPose
            self.frames[self.frames.shape[0]-1] = curPose
            return True
        return False

    # returns np.arr(19) of differences, 0 is no significant difference
    def compareAngles(self, evalPose: np.float64, angleThresholds: np.float64):
        angleDifferences = np.zeros(evalPose.shape)
        # remove empty data
        for i, x in enumerate(self.frames):
            if np.sum(x) != 0:
                filledFrames = self.frames[i:]
                break
        # positive is too large, negative is too small 
        differences = np.average(filledFrames, axis=0) - evalPose
        for i, x in enumerate(differences):
            if angleThresholds[i] == 0.:
                continue
            # if difference is significant enough
            if abs(x) > angleThresholds[i]:
                angleDifferences[i] = differences[i]
        return angleDifferences

    
    def giveFeedback(self, angleDifferences: np.float64):
        feedback = []
        # Probably will read glossary from csv in the end
        # Glossary will map angle_id to corresponding angle
        glossary = ['leftEar-nose-midShoulder',
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
 'rightShoulder-rightHip-rightKnee',
 'leftHip-leftKnee-leftAnkle',
 'rightHip-rightKnee-rightAnkle',
 'nose-midShoulder-midHip',
 'vertical(midShoulder)-midShoulder-midHip',
 'vertical(nose)-nose-midShoulder']

        threshold = 0.05 # set deviation threshold from ideal pose
        for angle_id, difference in enumerate(angleDifferences):
            if difference == 0.:
                continue
            elif (abs(difference/np.pi) > threshold):
                if (difference/np.pi > 0):
                    # angle needs to be smaller, as it is larger than ideal pose
                    feedback.append(f"{glossary[angle_id]} needs to be smaller")
                else:
                    # angle needs to be greater, as it is smaller than ideal pose
                    feedback.append(f"{glossary[angle_id]} needs to be larger")
        return feedback


        # gives feedback to a view, so returns json data which can be accessed from datapool

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:  # type: ignore
        """This node imports the evalPose and angleWeights score,
        then determines whether the rep is in the start or middle
        position

        It does so by evaluating both the start and the middle at
        the same time, if start_score > mid_score (deviation from ideal score)
        it is start state, else if mid > start, it is in middle state

        node will process the score, compare the poses to ideal pose,
        then give angleDifferences to the user 
        Args:
            inputs (dict): Dictionary with keys "img", "keypoints".

        Returns:
            outputs (dict): empty.
        """
        
        self.frame_count += 1
        globals.img = inputs["img"]
        # Keypoints has a shape of (1, 17, 2)
        keypoints = inputs["keypoints"]
        height = globals.img.shape[0]
        width = globals.img.shape[1]
        # Calculates angles in radians of live feed
        curPose = processData(keypoints, height, width)
        
        ## print(f"curPose: {curPose}")
        testPose = np.array([0.,0.98390493,1.51094115,1.6306515,0.26590253,2.81373512
            ,0.26590253,0.32785753,1.02067892,1.59934942,1.35720082,1.78439183
            ,0.79900877,1.33113154,1.22965078,1.52982444,0.90668716,2.49591843
            ,0.26101294])
        
        weights = np.array([0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,1.,0.,1.,0.,1.,0.])
        weights2 = np.array([0,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.1,0.,0.1,0.,0.1,0])

        score = self.comparePoses(testPose,curPose,weights)
        
        if score != -1:
            pass
            # print(f"score: {score}")
        
        if self.selectFrames(score, curPose, 0.1):
            angleDifferences = self.compareAngles(testPose, weights2)
            # now feedback is global variable which can be accessed by view in app.py
            globals.feedback = self.giveFeedback(angleDifferences)
            # print(f"angleDifferences: {angleDifferences}")
            ## print(f"frames: {self.frames}")
        
        return {}





    

   