"""
Node template for creating custom nodes.
"""

from typing import Any, Dict, List
import numpy as np
import csv
from peekingduck.pipeline.nodes.abstract_node import AbstractNode
from .helper import processData

class Node(AbstractNode):
    """This is a template class of how to write a node for PeekingDuck.

    Args:
        config (:obj:`Dict[str, Any]` | :obj:`None`): Node configuration.
    """

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)
        self.frames = np.zeros((10,19))
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
    def compareAngles(self, evalPose: np.float64, compareAngleWeights: np.float64):
        angleDifferences = np.zeros(evalPose.shape)
        # remove empty data
        for i, x in enumerate(self.frames):
            if np.sum(x) != 0:
                filledFrames = self.frames[i:]
                break
        # positive is too large, negative is too small 
        differences = np.average(filledFrames, axis=0) - evalPose
        for i, x in enumerate(differences):
            if compareAngleWeights[i] == 0.:
                continue
            # if difference is significant enough
            if x > compareAngleWeights[i]:
                angleDifferences[i] = differences[i]
        return angleDifferences

    
    def giveFeedback(self, angleDifferences: np.float64):
        pass
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
        img = inputs["img"]
        # Keypoints has a shape of (1, 17, 2)
        keypoints = inputs["keypoints"]
        height = img.shape[0]
        width = img.shape[1]
        # Calculates angles in radians of live feed
        curPose = processData(keypoints, height, width)
        
        ## print(curPose)
        testPose = np.array([0.,0.54795029,0.59766692,2.54392573,3.1299541,0.07864504,
        3.1299541,3.06294761,2.77424622,2.79817716,0.91208052,2.22951213,
        1.24551993,1.05832394,1.66790494,0.,0.85814533,2.29384891,1.70588907])
        weights = np.array([0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,1.,0.,1.,0.,1.,1.])
        weights2 = np.array([0,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.1,0.,0.1,0.,0.1,0.1])

        score = self.comparePoses(testPose,curPose,weights)
        
        if score != -1:
            print(f"score: {score}")
        
        if self.selectFrames(score, curPose, 0.25):
            angleDifferences = self.compareAngles(testPose, weights2)
            print(f"angleDifferences: {angleDifferences}")
            ## print(f"frames: {self.frames}")

        # return feedback which will be accessed by view
        return {}




    

   