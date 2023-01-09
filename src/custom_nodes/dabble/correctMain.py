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

        # initialize/load any configs and models here
        # configs can be called by self.<config_name> e.g. self.filepath
        # self.logger.info(f"model loaded with configs: config")

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:  # type: ignore
        """This node imports the evalPose and angleWeights score,
        then determines whether the rep is in the start or middle
        position

        It does so by evaluating both the start and the middle at
        the same time, if start_score > mid_score (deviation from ideal score)
        it is start state, else if mid > start, it is in middle state

        node will process the score, compare the poses to ideal pose,
        then give feedback to the user 
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
        

        
        # return outputs
        return {}

    def comparePoses(self, evalPose: np.float64, curPose: np.float64, angleWeights: np.float64):
        #for data security 
        score = 0.
        angleWeightSum = np.sum(angleWeights)
        print(angleWeightSum)
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

    

   