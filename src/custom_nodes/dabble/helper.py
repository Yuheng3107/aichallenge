import numpy as np


def processData(keypoints: np.float64, height: int, width: int):
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

    #make line from 2 points
    def makeLine(point1: np.float64, point2: np.float64):
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
    #midHip-leftHip
    lines[11] = makeLine(midHip,data[11])
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
    
    #calculate angle between 2 lines. note that it takes lines AB & BC to calculate angle ABC
    #this is because line AB is inverted with the negative sign.
    def calcAngle(line1: np.float64, line2: np.float64):
        if (line1[0] == 0. and line1[1] == 0.) or (line2[0] == 0. and line2[1] == 0.):
            return 0.
        cosine_angle = np.dot(-line1, line2) / (np.linalg.norm(-line1) * np.linalg.norm(line2))
        return np.arccos(cosine_angle)
    
    
    #curPose, 0 is invalid data
    curPose = np.zeros(19)
    #leftEar-nose-midShoulder
    curPose[0] = calcAngle(lines[0],lines[2])
    #rightEar-nose-midShoulder
    curPose[1] = calcAngle(lines[1],lines[2])
    #nose-midShoulder-leftShoulder
    curPose[2] = calcAngle(lines[2],lines[3])
    #nose-midShoulder-rightShoulder
    curPose[3] = calcAngle(lines[2],lines[4])
    #midShoulder-leftShoulder-leftElbow
    curPose[4] = calcAngle(lines[3],lines[5])
    #midShoulder-rightShoulder-rightElbow
    curPose[5] = calcAngle(lines[4],lines[6])
    #nose-midShoulder-leftElbow
    curPose[6] = calcAngle(lines[3],lines[5])
    #nose-midShoulder-rightElbow
    curPose[7] = calcAngle(lines[3],lines[6])
    #leftShoulder-leftElbow-leftWrist
    curPose[8] = calcAngle(lines[5],lines[7])
    #rightShoulder-rightElbow-rightWrist
    curPose[9] = calcAngle(lines[6],lines[8])
    #midShoulder-midHip-leftHip
    curPose[10] = calcAngle(lines[10],lines[11])
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
    curPose[17] = calcAngle(lines[9],lines[10])
    #vertical(nose)-nose-midShoulder
    curPose[18] = calcAngle(lines[9],lines[3])

    return curPose