"""
Node template for creating custom nodes.
"""

from typing import Any, Dict
import numpy as np
import globals
from deepface import DeepFace
from peekingduck.pipeline.nodes.abstract_node import AbstractNode
import asyncio

async def detect_emotion():
    globals.emotion = DeepFace.analyze(globals.img, actions= ['emotion'], enforce_detection=False)
    print(globals.emotion)
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
        """This node takes img data and processes it to detect emotions
        of the user

        Args:
            inputs (dict): Empty Dictionary.

        Returns:
            outputs (dict): Empty Dictionary.
        """
        asyncio.run(detect_emotion())
        
        # result = do_something(inputs["in1"], inputs["in2"])
        # outputs = {"out1": result}
        # return outputs
        return {}
