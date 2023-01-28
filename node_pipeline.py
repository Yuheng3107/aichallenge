from pathlib import Path
from peekingduck.pipeline.nodes.model import posenet
from src.custom_nodes.input import webcam
from src.custom_nodes.dabble import correctMain
from peekingduck.pipeline.nodes.output import media_writer, screen
from peekingduck.runner import Runner

import globals

def start_pipeline():
    # Custom Nodes

    webcam_node = webcam.Node(pkd_base_dir=Path.cwd() / "src" / "custom_nodes")
    processing_node = correctMain.Node(pkd_base_dir=Path.cwd() / "src" / "custom_nodes")
    posenet_node = posenet.Node(max_pose_detection=1)
    runner = Runner(
        nodes=[
            webcam_node,
            posenet_node,
            processing_node
        ]
    )
    runner.run()
    print("PeekingDuck Stopped")
    globals.ISACTIVE = False

if __name__ == "__main__":
    start_pipeline()