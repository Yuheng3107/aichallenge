"""
Node template for creating custom nodes.
"""

from typing import Any, Dict
import globals
from peekingduck.pipeline.nodes.abstract_node import AbstractNode
from peekingduck.pipeline.nodes.input.utils.read import VideoNoThread
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
        """This node takes globals.url which provides url to a jpeg from the front end which is read by
        the VideoThread which reads the image and puts it in the data pool for the PeekingDuck Posenet Model to use as inputs.

        Args:
            inputs (dict): Empty Dictionary.

        Returns:
            outputs (dict): Dictionary with keys "img".
        """

        # result = do_something(inputs["in1"], inputs["in2"])
        # outputs = {"out1": result}
        # return outputs
        if globals.url:
            # Gets a VideoNoThread, threading doesn't seem to work well
            cap = VideoNoThread(globals.url, False)
            success, img = cap.read_frame()
            if success:
                globals.img = img
            else:
                print("No image to read")
            
            
        # Need img to be in data pool for posenet model to work
        return {"img": globals.img}
