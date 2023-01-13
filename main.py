from pathlib import Path
from turtle import pos

from peekingduck.pipeline.nodes.input import visual
from peekingduck.pipeline.nodes.model import posenet
from src.custom_nodes.dabble import correctMain
from peekingduck.pipeline.nodes.draw import poses
# from peekingduck.pipeline.nodes.output import media_writer, screen
from peekingduck.runner import Runner

def main():
    processing_node = correctMain.Node(pkd_base_dir=Path.cwd() / "src" / "custom_nodes")
    visual_node = visual.Node(source=0)
    posenet_node = posenet.Node(max_pose_detection=1)
    poses_node = poses.Node()
    
    # screen_node = screen.Node()
    # media_writer_node = media_writer.Node(output_dir=str(Path.cwd() / "results"))

    runner = Runner(
        nodes=[
            visual_node,
            posenet_node,
            processing_node,
            poses_node,
            # screen_node,
            # media_writer_node
        ]
    )



    runner.run()
    


if __name__ == "__main__":
    main()