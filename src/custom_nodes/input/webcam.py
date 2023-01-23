"""
Node template for creating custom nodes.
"""

from typing import Any, Dict
import globals
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
        """This node takes globals.img which provides image from the front end and
        puts it in the data pool for the PeekingDuck Posenet Model to use as inputs.

        Args:
            inputs (dict): Empty Dictionary.

        Returns:
            outputs (dict): Dictionary with keys "img".
        """

        # result = do_something(inputs["in1"], inputs["in2"])
        # outputs = {"out1": result}
        # return outputs
        return {"img": globals.img}
