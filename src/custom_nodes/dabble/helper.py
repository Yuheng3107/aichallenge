import numpy as np

"""
FRAME METHODS
These methods are called every frame
"""
def processData(keypoints: np.float64, height: int, width: int):
    """
    Called every frame while rep detection is active.
    Used to convert keypoint data into angle data
        Args:
            keypoints (ndarray(19,dtype=float)): keypoints detected by PeekingDuck
            height (int): height of img

        Returns:
            curPose(ndarray(19,dtype=float)): angle data of the pose
    """
    
    if (keypoints.shape != (1, 17, 2)):
        return np.zeros(19)
    #for datasec purposes, 0 is invalid data
    data = np.zeros((17,2)) 
    for i,x in enumerate(keypoints[0]):
        if x[0] == -1.:
            continue
        data[i,0] = x[0]*(width - 1)
        data[i,1] = x[1]*(height - 1)
    #array of lines, 0,0 is invalid data
    lines = np.zeros((19,2))
    midShoulder = (data[5] + data[6])/2
    midHip = (data[11] + data[12])/2

    
    def makeLine(point1: np.float64, point2: np.float64):
        """
        Returns:
            output (np array(2 float)): line from point1 to point2
                (0,0) if the points cannot be calculated due to missing keypoint
        """
        if (point1[0] == 0. and point1[1] == 0.) or (point2[0] == 0. and point2[1] == 0.):
            return np.zeros(2)
        return point2-point1

    #leftEar-nose
    lines[0] = makeLine(data[3],data[0])
    #rightEar-nose
    lines[1] = makeLine(data[4],data[0])
    #nose-midShoulder
    lines[2] = makeLine(data[0],midShoulder)

    #midShoulder-leftShoulder
    lines[3] = makeLine(midShoulder,data[5])
    #midShoulder-rightShoulder
    lines[4] = makeLine(midShoulder,data[6])
    #leftShoulder-leftElbow
    lines[5] = makeLine(data[5],data[7])
    #rightShoulder-rightElbow
    lines[6] = makeLine(data[6],data[8])
    #leftElbow-leftWrist
    lines[7] = makeLine(data[7],data[9])
    #rightElbow-rightWrist
    lines[8] = makeLine(data[8],data[10])

    #vertical
    lines[9] = np.array([0,1],dtype=float)

    #midShoulder-midHip
    lines[10] = makeLine(midShoulder,midHip)
    #rightHip-rightAnkle
    lines[11] = makeLine(data[12],data[16])
    #midHip-rightHip
    lines[12] = makeLine(midHip,data[12])
    #leftShoulder-leftHip
    lines[13] = makeLine(data[5],data[11])
    #rightShoulder-rightHip
    lines[14] = makeLine(data[6],data[12])

    #leftHip-leftKnee
    lines[15] = makeLine(data[11],data[13])
    #rightHip-rightKnee
    lines[16] = makeLine(data[12],data[14])
    #leftKnee-leftAnkle
    lines[17] = makeLine(data[13],data[15])
    #rightKnee-rightAnkle
    lines[18] = makeLine(data[14],data[16])
    
    def calcAngle(line1: np.ndarray, line2: np.ndarray):
        """
        returns: 
            angle (float): angle between line1 and line2
                0 if the angle cannot be calculated due to missing line
        """
        if (line1[0] == 0. and line1[1] == 0.) or (line2[0] == 0. and line2[1] == 0.):
            return 0.
        cosine_angle = np.dot(-line1, line2) / (np.linalg.norm(-line1) * np.linalg.norm(line2))
        return np.arccos(cosine_angle)
    
    def calcLine(line1:np.ndarray, line2: np.ndarray):
        """
        returns: 
            ratio (float): ratio of line1 to line2
                0 if the points cannot be calculated due to missing line
        """
        if (line1[0] == 0. and line1[1] == 0.) or (line2[0] == 0. and line2[1] == 0.):
            return 0.
        return np.linalg.norm(line1)/np.linalg.norm(line2)
    
    #curPose, 0 is invalid data
    curPose = np.zeros(19)
    
    #vertical-rightHip-rightAnkle
    curPose[2] = calcAngle(lines[9],lines[11])
    #nose-midShoulder-rightShoulder 
    curPose[3] = calcAngle(lines[2],lines[4])
    #midShoulder-leftShoulder-leftElbow
    curPose[4] = calcAngle(lines[3],lines[5])
    #midShoulder-rightShoulder-rightElbow
    curPose[5] = calcAngle(lines[4],lines[6])
    #nose-midShoulder-leftElbow
    curPose[6] = calcAngle(lines[2],lines[5])
    #nose-midShoulder-rightElbow
    curPose[7] = calcAngle(lines[2],lines[6])
    #leftShoulder-leftElbow-leftWrist
    curPose[8] = calcAngle(lines[5],lines[7])
    #rightShoulder-rightElbow-rightWrist
    curPose[9] = calcAngle(lines[6],lines[8])
    #arm-forearm ratio
    curPose[10] = calcLine(lines[6],lines[8])
    #midShoulder-midHip-rightHip
    curPose[11] = calcAngle(lines[10],lines[12])
    #leftShoulder-leftHip-leftKnee
    curPose[12] = calcAngle(lines[13],lines[15])
    #rightShoulder-rightHip-rightKnee
    curPose[13] = calcAngle(lines[14],lines[16])
    #leftHip-leftKnee-leftAnkle
    curPose[14] = calcAngle(lines[15],lines[17])
    #rightHip-rightKnee-rightAnkle
    curPose[15] = calcAngle(lines[16],lines[18])
    #nose-midShoulder-midHip
    curPose[16] = calcAngle(lines[3],lines[10])
    #vertical-midHip-midShoulder
    curPose[17] = calcAngle(lines[9],np.negative(lines[10]))
    #vertical(nose)-nose-midShoulder
    curPose[18] = calcAngle(lines[9],lines[3])

    #Avg(shoulder-hip-knee)
    curPose[0] = (curPose[12]+curPose[13])/2
    #Avg(hip-knee-ankle)
    curPose[1] = (curPose[14]+curPose[15])/2
    return curPose

def comparePoses(evalPose: np.ndarray, curPose: np.ndarray, angleWeights: np.ndarray):
    """
    Called every frame while rep detection is active.
    Used to determine if user is currently in a certain pose.
    Args:
        evalPose (ndarray(19,dtype=float)): the ideal pose to be compared against.
        curPose (ndarray(19,dtype=float)): the current pose detected by the camera.

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