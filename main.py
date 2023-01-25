from pathlib import Path
from peekingduck.pipeline.nodes.model import posenet
from src.custom_nodes.input import webcam
from src.custom_nodes.dabble import correctMain
from peekingduck.pipeline.nodes.draw import poses
# from peekingduck.pipeline.nodes.output import media_writer, screen
from peekingduck.runner import Runner


def main():
    # Custom Nodes
    webcam_node = webcam.Node(pkd_base_dir=Path.cwd() / "src" / "custom_nodes")
    processing_node = correctMain.Node(pkd_base_dir=Path.cwd() / "src" / "custom_nodes")
    
# Change source to file name to parse file
    sources = [[0],
        ["Training_Data/Squats/Good_Pose/Side_View1.mp4","Training_Data/Squats/Bad_Pose/Butt/Side_View.mp4","Training_Data/Squats/Bad_Pose/Knee/Side_View2.mp4"],
        ["Training_Data/Squats/Good_Pose/Front_View2.mp4","Training_Data/Squats/Good_Pose/Front_View2.mp4","Training_Data/Squats/Good_Pose/Front_View4.mp4","Training_Data/Squats/Good_Pose/Front_View4.mp4","Training_Data/Squats/Bad_Pose/Knee/Front_View1.mp4"],
        ["Training_Data/Push_Up/Good_Pose/Side_View1.mp4","Training_Data/Push_Up/Bad_Pose1/Side_View.mp4","Training_Data/Push_Up/Bad_Pose2/Side_View.mp4"],
        ["Training_Data/Squats/Sentimental/Front_View5.mp4","Training_Data/Squats/Sentimental_Neutral/Front_View1.mp4"]]


    # Add threading=True to arguments in visual.Node constructor to
    # enable threading
    posenet_node = posenet.Node(max_pose_detection=1)
    poses_node = poses.Node()
    # screen_node = screen.Node()
    # media_writer_node = media_writer.Node(output_dir=str(.cwd() / "results"))
    runner = Runner(
        nodes=[
            webcam_node,
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