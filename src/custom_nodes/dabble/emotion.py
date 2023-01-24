"""
TO BE DELETED
"""

from typing import Any, Dict
import numpy as np
import globals
from deepface import DeepFace
from peekingduck.pipeline.nodes.abstract_node import AbstractNode
import threading
    

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
        self.frameCount = 0
        """
        Number of frames that have passed. Emotions are detected every 10 frames.
        """
        self.selectedFrames = np.zeros((100,7))
        """
        Array(X,K) containing the store of frames to be evaluated
            X: Number of frames (selectedFrameCount)
            K: emotions (7)
        """
        #angry, disgust, fear, happy, sad, surprise, neutral
        self.selectedFrameCount = 0
        """
        Number of frames in selectedFrames 
        """

    def detect_emotion(self,):
        # Gets dominant emotion
        try:
            emotions = DeepFace.analyze(globals.img, actions= ['emotion'], enforce_detection=True)['emotion']
            print(emotions)
            self.selectedFrames[self.selectedFrameCount] = list(emotions.values())
            self.selectedFrameCount += 1
            
        except:
            print("No Face")

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:  # type: ignore
        """This node takes img data and processes it to detect emotions
        of the user

        Args:
            inputs (dict): Empty Dictionary.

        Returns:
            outputs (dict): Empty Dictionary.
        """
        
        
        self.frameCount += 1
        if self.frameCount == 10:
            thread = threading.Thread(target=self.detect_emotion, name='thread', daemon=True)
            self.frameCount = 0
            thread.start()

        

        # result = do_something(inputs["in1"], inputs["in2"])
        # outputs = {"out1": result}
        # return outputs
        return {}
