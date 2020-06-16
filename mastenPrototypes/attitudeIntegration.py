from math import pi, sin, cos, atan, sqrt, atan2
import numpy as np
import csv
import random
import savageFunctions as sav

###############################################################################################################

# bruh = np.array([[2,3,4],[1,1,3]])
#
# print(bruh[0,0])
#
# breh = sav.skew((bruh[0,0],bruh[0,1],bruh[0,2]))
#
# print(breh)


def integrateLoop(timeVec,omegaMat,dcm_i,sampleLength):
    #this will take in timeVec
        #timeVec will be the full list of times corresponding to the "measurements" taken
        #time vec should be a column vector of length "sampleLength"
        # this has to be a numpy array
    # omegaMat
        # this will be a matrix with columns (w_x, w_y, w_z)
        # and the rows will represent the time index
        # this has to be a numpy array
    # dcm_i
        # this is the first direction cosine matrix
        # this has to be a numpy array
    # sample length
        # is the number of "measurements"
    checkFirst = False
    for k in (0, sampleLength-1):
        # use that given known state for the first integration
        # otherwise, use the extrapolated value
        if not checkFirst:
            dcm_k_minus = dcm_i
            checkFirst = True
            timeVec[k-1] = 0
        else:
            dcm_k_minus = dcm_k

        Ddcm_k = np.dot(dcm_k_minus,sav.skew((omegaMat[k,0],omegaMat[k,1],omegaMat[k,2]))) #try to use a slice

        dcm_k = Ddcm_k * (timeVec[k]-timeVec[k-1]) + dcm_k_minus

    return dcm_k


# timeVec = np.array([.1,.2,.3,.4]).T
# omegaMat = bruh = np.array([[.2,.3,.6],[.2,.6,.3],[.15,.32,.3],[.01,.17,.3]])
# dcm_i = np.array([[1,0,0],[0,1,0],[0,0,1]])
# sampleLength = 4
# bruhh = integrateLoop(timeVec,omegaMat,dcm_i,sampleLength)
#
# print(bruhh)


def integrateStep(prevDCM, prevState, omega, accel, dt):

    #first things first find the current derivative of the dcm
    d_DCM = np.dot(prevDCM , sav.skew(omega))

    #now integrate to find the current DCM
    DCM = np.dot(d_DCM , dt) + prevDCM

    # rotate acceleration vector from body frame to inertial
    inertialAccel = np.dot(DCM , accel)


    state = np.zeros((9,1))

    state[0] = prevState[0] + prevState[3] * dt + inertialAccel[0] * dt**2 * .5
    state[1] = prevState[1] + prevState[4] * dt + inertialAccel[1] * dt**2 * .5
    state[2] = prevState[2] + prevState[5] * dt + inertialAccel[2] * dt**2 * .5


    state[3] = prevState[3] + inertialAccel[0] * dt
    state[4] = prevState[4] + inertialAccel[1] * dt
    state[5] = prevState[5] + inertialAccel[2] * dt

    state[6] = inertialAccel[0]
    state[7] = inertialAccel[1]
    state[8] = inertialAccel[2]

    return (state, DCM)



# PREV_DCM = np.array([[1,0,0],
#                      [0,1,0],
#                      [0,0,1]])
#
# PREV_STATE = np.array([[0,0,0,0,0,0,0,0,0]]).T
#
# OMEGA = np.array([1,1,1]).T
#
# ACCEL = np.array([1,1,1]).T
#
# dt = .1
#
# print(integrateStep(PREV_DCM,PREV_STATE,OMEGA,ACCEL,dt))