# Lyon Foster
# ***Not the property of Masten Space Systems***
# 5/22/20




from math import pi, sin, cos, atan, sqrt, atan2
import numpy as np
import csv
import random



##############################################################################################################
def skew(v):
    # argument is a 3x1 column vector
    # returns the skew symetric 'first half of the cross product matrix' of that vector
    # so if you have 'V x W'
    # you would input 'V'
    # and this function returns 'V x'
    # reference: Savage 3.2.1-1

    vCross = np.array([[0, -v[2], v[1]],
                       [v[2], 0, -v[0]],
                       [-v[1], v[0], 0]])
    # vCross = [[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]]

    return vCross


##############################################################################################################
def euler2dcm(phi,theta,psi):
    # Inputs are pitch(theta), yaw(psi), and roll(phi) in radians
    # can be used as a body to Earth coordinate transform

    C11 = cos(theta) * cos(psi)
    C12 = -cos(phi) * sin(psi) + sin(phi) * sin(theta) * cos(psi)
    C13 = sin(phi) * sin(psi) + cos(phi) * sin(theta) * cos(psi)

    C21 = cos(theta) * sin(psi)
    C22 = cos(phi) * cos(psi) + sin(phi) * sin(theta) * sin(psi)
    C23 = -sin(phi) * cos(psi) + cos(phi) * sin(theta) * sin(psi)

    C31 = -sin(theta)
    C32 = sin(phi) * cos(theta)
    C33 = cos(phi) * cos(theta)

    dcm = np.array([
        [C11, C12, C13],
        [C21, C22, C23],
        [C31, C32, C33]
    ])

    return dcm


##############################################################################################################
def dcm2euler(dcm):
    # dcm[i-1,j-1]

    # theta = atan( (-dcm[2,0]) / (sqrt(dcm[2,1]^2 + dcm[2,2]^2)) )
    # input is a direction cosine matrix
    # output in radians

    psi = atan2(dcm[1, 0], dcm[0, 0])
    phi = atan2(dcm[2, 1], dcm[2, 2])

    if dcm[2, 0] ** 2 < 1:
        theta = - atan2(dcm[2, 0], sqrt(1 - dcm[2, 0] ** 2))
    else:
        theta = - atan2(dcm[2, 0], 0)

    euler = np.array([theta, psi, phi])
    return euler


##############################################################################################################
def retRand(precision):
    # I didn't feel like looking for a function that returned non integer random numbers so I made this.
    # precision is the number of decimal places you'd like your random number to be
    # these numbers are between 0 and 1
    return (random.randrange(0, precision, 1)) / precision


##############################################################################################################


# creating an output csv with a bunch of random numbers as the inputs to roll pitch and yaq
def euler2dcmCSV(desiredRowsOfCSV):
    with open('euler2dcm.csv', 'w', newline='') as e2d:
        e2dWriter = csv.writer(e2d, dialect='excel')
        headers = zip(['phi'], ['psi'], ['theta'],
                      ['dcm(1,1)'], ['dcm(1,2)'], ['dcm(1,3)'],
                      ['dcm(2,1)'], ['dcm(2,2)'], ['dcm(2,3)'],
                      ['dcm(3,1)'], ['dcm(3,2)'], ['dcm(3,3)'])
        for header in headers:  # putting the headers in teh csv
            e2dWriter.writerow(header)
        for i in range(0, desiredRowsOfCSV):
            # want to control the random numbers I put in
            a = retRand(1000)
            b = retRand(1000)
            c = retRand(1000)
            print(str(euler2dcm(a, b, c)[0, 0]))  # check first column of csv against this printout
            dcm = euler2dcm(a, b, c)
            # dcm_list = dcm.ravel()
            rows = zip([str(a)], [str(b)], [str(c)], [str(dcm[0, 0])], [str(dcm[0, 1])], [str(dcm[0, 2])],
                       [str(dcm[1, 0])], [str(dcm[1, 1])], [str(dcm[1, 2])],
                       [str(dcm[2, 0])], [str(dcm[2, 1])], [str(dcm[2, 2])])
            for row in rows:
                e2dWriter.writerow(row)


##############################################################################################################

def dcm2eulerCSV(desiredRowsOfCSV):
    with open('dcm2euler.csv', 'w', newline='') as d2e:
        d2eWriter = csv.writer(d2e, dialect='excel')
        headers = zip(['dcm(1,1)'], ['dcm(1,2)'], ['dcm(1,3)'],
                      ['dcm(2,1)'], ['dcm(2,2)'], ['dcm(2,3)'],
                      ['dcm(3,1)'], ['dcm(3,2)'], ['dcm(3,3)'],
                      ['phi'], ['psi'], ['theta']
                      )

        for header in headers:
            d2eWriter.writerow(header)

        for k in range(0, desiredRowsOfCSV):
            a = retRand(1000)
            b = retRand(1000)
            c = retRand(1000)

            d = retRand(1000)
            e = retRand(1000)
            f = retRand(1000)

            g = retRand(1000)
            h = retRand(1000)
            i = retRand(1000)

            dcm = np.array([[a, b, c],
                            [d, e, f],
                            [g, h, i]
                            ])

            rows = zip([str(dcm[0, 0])], [str(dcm[0, 1])], [str(dcm[0, 2])],
                       [str(dcm[1, 0])], [str(dcm[1, 1])], [str(dcm[1, 2])],
                       [str(dcm[2, 0])], [str(dcm[2, 1])], [str(dcm[2, 2])],
                       [str(dcm2euler(dcm)[0])], [str(dcm2euler(dcm)[1])], [str(dcm2euler(dcm)[2])]
                       )
            for row in rows:
                d2eWriter.writerow(row)


##############################################################################################################

def csvREAD(filename, rowsData, colsData):
    # This function reads in the data and spits out a numpy array of the data
    # be sure to pass it the number of rows and columns of data not including the header

    with open(filename, newline='') as e2d:
        e2dReader = csv.reader(e2d, delimiter=',', dialect='excel')  # ,quoting = csv.QUOTE_NONNUMERIC)

        csvASarray = np.zeros((rowsData, colsData))

        next(e2dReader, None)

        i = 0
        for row in e2dReader:
            csvASarray[i, :] = np.array(row)
            i = i + 1

    csvASarray = csvASarray.astype(np.float)

    return csvASarray


########################################################################################################


def compareFuctions(filename,options,rowsData,colsData,precision):
    # Input the file name of the csv to be compared
    # options should be either 'euler2dcm' or 'dcm2euler' depending on which way you go
    # rowsData is the rows of data from the csv not including the header
    # colsData in the columns of data from the csv not including the header
    # Precision is how many decimal places you'd like the csv to be compared to
        # for example if you enter 3, then .2341 == .2342
    # the return type is a boolean--either true, the csv matches the functions to the specified precision
    #                               or false, it does not

    #this is for a throw at the bottom
    class bcolors:
        FAIL = '\033[91m'

    array = csvREAD(filename,rowsData,colsData)

    if(options == 'euler2dcm'):
        # the first 3 columns are the input

        inputs = array[:,0:3]

        outputs = np.zeros((rowsData,9))
        for i in range(0,rowsData,1):
            outputs[i,:] = np.reshape( euler2dcm(inputs[i,0],inputs[i,1],inputs[i,2]), 9)

        checkAgainst = array[:,3:12]

        checkSame = (np.around(outputs, precision) == np.around(checkAgainst, precision)).all()
        if not checkSame:
            print('From CSV')
            print(checkAgainst[0,:])
            print('From Function')
            print(outputs[0,:])

    elif(options == 'dcm2euler'):

        inputs = array[:, 0:9]

        outputs = np.zeros((rowsData, 3))
        for i in range(0, rowsData, 1):
            outputs[i, :] = np.reshape(dcm2euler(np.array([[inputs[i, 0], inputs[i, 1], inputs[i, 2]],
                                                          [inputs[i, 3], inputs[i, 4], inputs[i, 5]],
                                                          [inputs[i, 6], inputs[i, 7], inputs[i, 8]]])), 3)

        checkAgainst = array[:, 9:12]

        checkSame = (np.around(outputs, precision) == np.around(checkAgainst, precision)).all()
        if not checkSame:
            print('From CSV')
            print(checkAgainst[1:12,:])
            print('From Function')
            print(outputs[1:12,:])

    else:
        print(f"{bcolors.FAIL}compareFunctions accepts 'euler2dcm' or 'dcm2euler' as options{bcolors.ENDC}")

    return checkSame


########################################################################################################

print(compareFuctions('euler2dcm_sn.csv','euler2dcm',100,12,2))
