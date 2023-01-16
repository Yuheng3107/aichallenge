from fileinput import filename
from pathlib import Path
from turtle import pos

from peekingduck.pipeline.nodes.input import visual
from peekingduck.pipeline.nodes.model import posenet
from src.custom_nodes.dabble import correctMain
from src.custom_nodes.dabble import emotion
from peekingduck.pipeline.nodes.draw import poses
# from peekingduck.pipeline.nodes.output import media_writer, screen
from peekingduck.runner import Runner

def main():
    processing_node = correctMain.Node(pkd_base_dir=Path.cwd() / "src" / "custom_nodes")
    emotion_node = emotion.Node(pkd_base_dir=Path.cwd() / "src" / "custom_nodes")
    # Change source to file name to parse file
    """
    0
    "Training_Data\Good_Pose\Side_View.mp4"
    "Training_Data\Bad_Pose\Butt\Side_View.mp4"
    "Training_Data\Good_Pose\Front_View.mp4"
    "Training_Data\Bad_Pose\Knee\Front_View1.mp4"

    """
    visual_node = visual.Node(source="Training_Data\Good_Pose\Front_View1.mp4")
    posenet_node = posenet.Node(max_pose_detection=1)
    poses_node = poses.Node()
    
    # screen_node = screen.Node()
    # media_writer_node = media_writer.Node(output_dir=str(Path.cwd() / "results"))

    runner = Runner(
        nodes=[
            visual_node,
            posenet_node,
            processing_node,
            emotion_node,
            poses_node,
            # screen_node,
            # media_writer_node
        ]
    )



    runner.run()
    


if __name__ == "__main__":
    main()