"""
correctMain.py
    - Rep Counting
    - Detect & Give Feedback for:
        - Key Poses
        - Rep Time
        - Emotions
helper.py
    - Calculating Key Angles
    - Comparing: 
        - Key Poses
        - Rep Time
        - Emotions
"""

import numpy as np

### REP METHODS
### These methods are called once per rep.

def compareAngles(evalPose: np.ndarray, angleThresholds: np.ndarray, selectedFrames: np.ndarray, selectedFrameCount: np.ndarray):
    """
    Calculates the difference between ideal and observed angles in user's pose
        Called: when rep is finished.

        Args:
            evalPose (Array(11)[float]): the ideal pose to be compared against.
            curPose (Array(11)[float]): the current pose detected by the camera.
            angleThresholds (Array(11)[float]): the threshold of angle differences
            selectedFrames (Array(X,11)[float]): Array containing the store of frames to be evaluated
            selectedFrameCount: X - Number of frames in selectedFrames 

        Returns:
            angleDifferences (Array(11)[float]): angle differences, positive is too large, negative is too small, 0 is no significant difference    
    """
    angleDifferences = np.zeros(evalPose.shape,dtype=np.float32) 
    # check for 0 frames
    if selectedFrameCount == 0:
        return np.array([-99])
    # remove empty data
    filledSelectedFrames = selectedFrames[0:selectedFrameCount]
    # positive is too large, negative is too small 
    differences = np.average(filledSelectedFrames, axis=0)

    """
    CREATING NEW EXERCISES
    """
    print(f"curPose: {', '.join(str(angle) for angle in differences)}")
    
    differences -= evalPose
    print(differences)

    for i, x in enumerate(differences):
        if angleThresholds[i] == 0.:
            continue
        # if difference is significant enough
        if abs(x) > angleThresholds[i]:
            angleDifferences[i] = differences[i]
    return angleDifferences

def compareTime(evalTime:np.float32, repTime:np.float32):
    """
    Evaluates if rep time is too short
        Called: when rep is finished
    """
    if repTime < evalTime:
        # rep time is too short
        return 1
    return 0


def compareEmotions(selectedEmotionFrames,selectedEmotionFrameCount):
    """
    Averages out the emotions detected.
        Called: when rep is finished.

        Args:
            selectedEmotionFrames (Array(X,7)[float]): Array containing the store of frames to be evaluated
            selectedEmotionFrameCount: X - Number of frames in selectedEmotionFrames 

        Returns:
            emotionAverage (Array(7)[float]): Array containing the average emotion confidences
    """
    # check for 0 frames
    if selectedEmotionFrameCount == 0:
        return np.array([-99])
    # remove empty data
    filledselectedFrames = selectedEmotionFrames[0:selectedEmotionFrameCount]

    emotionAverage = np.average(filledselectedFrames, axis=0)
    return emotionAverage

### FRAME METHODS
### These methods are called every frame

def processData(keypoints: np.ndarray, height: int, width: int):
    """
    Used to convert keypoint data into angle data
        Called: every frame while rep detection is active.

        Args:
            keypoints (Array(11)[float]): keypoints detected by PeekingDuck
            height (int): height of img

        Returns:
            curPose(Array(11)[float]): angle data of the pose
    """
    
    if (keypoints.shape != (1, 17, 2)):
        return np.zeros(11,dtype=np.float32)
    # for datasec purposes, 0 is invalid data
    data = np.zeros((17,2),dtype=np.float32) 
    for i,x in enumerate(keypoints[0]):
        if x[0] == -1.:
            continue
        data[i,0] = x[0]*(width - 1)
        data[i,1] = x[1]*(height - 1)
    
    def makeLine(point1: np.float32, point2: np.float32):
        """
        Returns:
            output (np array(2 float)): line from point1 to point2, (0,0) if the points cannot be calculated due to missing keypoint
        """
        if (point1[0] == 0. and point1[1] == 0.) or (point2[0] == 0. and point2[1] == 0.):
            return np.zeros(2,dtype=np.float32)
        return point2-point1

    # array of lines, 0,0 is invalid data
    lines = np.zeros((12,2),dtype=np.float32)

    # vertical
    lines[0] = np.array([0,1],dtype=float)

    # leftShoulder-leftElbow
    lines[1] = makeLine(data[5],data[7])
    # rightShoulder-rightElbow
    lines[2] = makeLine(data[6],data[8])
    # leftElbow-leftWrist
    lines[3] = makeLine(data[7],data[9])
    # rightElbow-rightWrist
    lines[4] = makeLine(data[8],data[10])

    # leftShoulder-leftHip
    lines[5] = makeLine(data[5],data[11])
    # rightShoulder-rightHip
    lines[6] = makeLine(data[6],data[12])

    # leftHip-leftKnee
    lines[7] = makeLine(data[11],data[13])
    # rightHip-rightKnee
    lines[8] = makeLine(data[12],data[14])
    # leftKnee-leftAnkle
    lines[9] = makeLine(data[13],data[15])
    # rightKnee-rightAnkle
    lines[10] = makeLine(data[14],data[16])
    # rightHip-rightAnkle
    lines[11] = makeLine(data[12],data[16])

    def calcAngle(line1: np.ndarray, line2: np.ndarray):
        """
        returns: 
            angle (float): angle between line1 and line2, 0 if the angle cannot be calculated due to missing line
        """
        if (line1[0] == 0. and line1[1] == 0.) or (line2[0] == 0. and line2[1] == 0.):
            return 0.
        cosine_angle = np.dot(-line1, line2) / (np.linalg.norm(-line1) * np.linalg.norm(line2))
        return np.arccos(cosine_angle)
    
    def calcAvg(angle1: np.float32, angle2: np.float32):
        """
        returns: 
            angle (float): ratio of line1 to line2
                0 if the points cannot be calculated due to missing line
        """
        if angle1 == 0 or angle2 == 0:
            return 0.
        return (angle1+angle2)/2
    
    # curPose, 0 is invalid data
    curPose = np.zeros(11,dtype=np.float32)

    # rightHip-rightShoulder-rightElbow
    curPose[0] = calcAngle(-lines[6],lines[2])
    # Avg(hip-shoulder-elbow)
    curPose[1] = calcAvg(curPose[0],calcAngle(-lines[5],lines[1]))
    # rightShoulder-rightElbow-rightWrist
    curPose[2] = calcAngle(lines[2],lines[4])
    # Avg(shoulder-elbow-wrist)
    curPose[3] = calcAvg(curPose[2],calcAngle(lines[1],lines[3]))

    # rightShoulder-rightHip-rightKnee
    curPose[4] = calcAngle(lines[6],lines[8])
    # Avg(shoulder-hip-knee)
    curPose[5] = calcAvg(curPose[4],calcAngle(lines[5],lines[7]))
    # rightHip-rightKnee-rightAnkle
    curPose[6] = calcAngle(lines[8],lines[10])
    # Avg(hip-knee-ankle)
    curPose[7] = calcAvg(curPose[6],calcAngle(lines[7],lines[9]))
    # vertical-rightHip-rightShoulder
    curPose[8] = calcAngle(lines[0],-lines[6])
    # Avg(vertical-hip-shoulder)
    curPose[9] = calcAvg(curPose[8],calcAngle(lines[0],-lines[5]))
    # vertical-rightHip-rightAnkle
    curPose[10] = calcAngle(lines[0],lines[11])

    return curPose

def comparePoses(evalPose: np.ndarray, curPose: np.ndarray, angleWeights: np.ndarray):
    """
    Used to determine if user is currently in a certain pose.
        Called: every frame while rep detection is active.

        Args:
            evalPose (Array(11)[float]): the ideal pose to be compared against.
            curPose (Array(11)[float]): the current pose detected by the camera.

        Returns:
            score (float): a score between 0 and 1, 0 being completely similar and 1 being completely different.
                -1 if curPose is missing crucial angle data.
    """    
    # for data security 
    score = 0.
    
    angleWeightSum = np.sum(angleWeights)
    if angleWeightSum == 0:
        return -1
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