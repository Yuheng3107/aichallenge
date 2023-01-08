"""
Node template for creating custom nodes.
"""

from typing import Any, Dict, List
import numpy as np
import csv
from peekingduck.pipeline.nodes.abstract_node import AbstractNode


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
        """This node does ___.

        Args:
            inputs (dict): Dictionary with keys "img", "keypoints".

        Returns:
            outputs (dict): empty.
        """
        img = inputs["img"]
        # Keypoints has a shape of (1, 17, 2), since we only 
        # detecting one person can take first index, so now 
        # it has shape of (17,2)
        keypoints = inputs["keypoints"]
        print(keypoints)
        print(keypoints.shape)
        
        # return outputs
        return {}
    def comparePoses(self, evalPose: np.float64, curPose: np.float64, angleWeights: np.float64):
        # Compares current pose to ideal pose using weighted angles

        # Output: Output: float between 0 to 1, representing closeness of the 2 poses.
        pass
    