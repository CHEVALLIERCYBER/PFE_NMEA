
#------------------------------------------------------------------------
#
# @Creators : EV2 CHEVALLIER & EV2 LEBIGRE
#
# @Date : 07.11.20
# @Location : École Navale / Chaire de Cyberdéfense des systèmes navals
# @Project : End of studies project
# @Subject : # Détection temps-réel d’anomalies cyber # sur un réseau NMEA par l’utilisation de # techniques d’apprentissage automatique.
#            # Detection of cyber anomalies in real time on NMEA network by using machine learning
#------------------------------------------------------------------------
# @Title : real_time_detection
#------------------------------------------------------------------------
# @Description : This code is the final version of the detection program that we created. It detects, in real time,
# anomalies in NMEA data that are provided on port 5005 (you can can change the port at the start)
#
# This program uses files RMC_45min_dataset.json and RPM_45min_dataset.json as training data set
# (specify the access path at the start).
# To get the classification of the program, you just have to use variables spoof_detect_distance and
# spoof_detect_heading, if one is TRUE, a spoofing is detected by the program.
#
#
# A try of a detection on engine NMEA RPM data is in comment lines
#------------------------------------------------------------------------

import numpy as np
import pynmea2
import json
import math
import socket
from sklearn import preprocessing
from sklearn import svm


##################################################################################################

# loading of train set data, enter access path
train_dataRMC = open('')
train_dataRPM = open('')

# port used
UDP_IPrec = "127.0.0.1" # IP adress
UDP_PORTrec = 5005  # entry socket (bridge command)

#################################################################################################



# Heading computation (three latitudes and three longitude are needed to process the heading)
def heading(l_phi, l_g):
    epsilon = 10 ** (-13)
    list_heading_calculated = []
    for i in range(len(l_phi) - 1):

        if abs(l_phi[i + 1] - l_phi[i]) < epsilon and l_g[i + 1] <= l_g[i]:
            heading_calculated = 90
            list_heading_calculated.append(heading_calculated)

        elif abs(l_phi[i + 1] - l_phi[i]) < epsilon and l_g[i + 1] > l_g[i]:
            heading_calculated = 270
            list_heading_calculated.append(heading_calculated)

        elif l_phi[i + 1] >= l_phi[i] and abs(l_g[i + 1] - l_g[i]) < epsilon:
            heading_calculated = 0
            list_heading_calculated.append(heading_calculated)

        elif l_phi[i + 1] < l_phi[i] and abs(l_g[i + 1] - l_g[i]) < epsilon:
            heading_calculated = 180
            list_heading_calculated.append(heading_calculated)

        else:

            a = (180. / math.pi) * abs(math.atan(
                math.cos(0.5 * (l_phi[i + 1] + l_phi[i])) * (l_phi[i + 1] - l_phi[i]) / (l_g[i + 1] - l_g[i])))

            if l_phi[i + 1] > l_phi[i] and l_g[i + 1] < l_g[i]:
                heading_calculated = 90 - a
                list_heading_calculated.append(heading_calculated)

            elif l_phi[i + 1] > l_phi[i] and l_g[i + 1] > l_g[i]:
                heading_calculated = 270 + a
                list_heading_calculated.append(heading_calculated)

            elif l_phi[i + 1] < l_phi[i] and l_g[i + 1] > l_g[i]:
                heading_calculated = 270 - a
                list_heading_calculated.append(heading_calculated)

            else:  # l_phi[i+1]>l_phi[i] and l_g[i+1]<l_g[i]:
                heading_calculated = 90 + a
                list_heading_calculated.append(heading_calculated)
    return list_heading_calculated


# distance computation
def distance(phi1, phi0, g1, g0):
    return np.sqrt(
        (float(phi1) - float(phi0)) ** 2 + ((float(g1) - float(g0)) / ((float(phi1) + float(phi0)) / 2)) ** 2)


def diff_list(list):
    list_diff = []
    for i in range(1, len(list) - 1):
        list_diff.append(list[i] - list[i - 1])
    return list_diff


# loading and preprocessing of RMC data for training
def load_and_process_RMC(file):
    list_phi = []
    list_g = []
    list_t = []
    list_v = []
    result = [[]]
    for line in file:
        data = json.loads(line)
        list_phi.append(float(data["lat"]))
        list_g.append(float(data["lon"]))
        list_t.append(float(data["timestamp"]))
        list_v.append(float(data["spd_over_grnd"]))
    result.append(list_phi)
    result.append(list_g)
    result.append(list_t)
    result.append(list_v)
    result.pop(0)
    dist = [0, 0]
    for i in range(1, len(result[0]) - 1):
        dist.append(distance(result[0][i], result[0][i - 1], result[1][i], result[1][i - 1]))
    matrix1 = np.zeros((len(dist), 2))
    listecap = heading(list_phi, list_g)
    diffecap = diff_list(listecap)
    for i in range(0, len(dist) - 1):
        matrix1[i][0] = (result[3][i])
        matrix1[i][1] = dist[i]
    i = 0
    end = len(matrix1) - 1
    # preprocessing of training data : outliers are deleted
    while i < end:
        if matrix1[i][1] > 7:
            matrix1 = np.delete(matrix1, i, 0)
            end = end - 1
        i = i + 1
    matrix2 = np.zeros((len(diffecap), 2))
    for i in range(0, len(diffecap) - 1):
        matrix2[i][0] = (result[3][i])
        matrix2[i][1] = diffecap[i]

    return matrix1, matrix2


def load_and_process_RPM (file):
    list_rpm_eng1 = []
    list_rpm_eng2 = []
    for line in file:
        data = json.loads(line)
        if data["engine_no"] == "1":
            list_rpm_eng1.append(float(data["speed"]))
        else:
            list_rpm_eng2.append(float(data["speed"]))
    diffeng1=[]
    diffeng2=[]
    for i in range(0, len(list_rpm_eng1)-2):
        diffeng1.append(list_rpm_eng1[i]-list_rpm_eng1[i+1])
    for i in range(0, len(list_rpm_eng2)-2):
        diffeng2.append(list_rpm_eng2[i]-list_rpm_eng2[i+1])
    matrix1 = np.zeros((len(diffeng2), 1))
    matrix2 = np.zeros((len(diffeng1), 1))
    for i in range(0, len(diffeng1) - 1):
        matrix1[i][0] = diffeng1[i]
    for i in range(0, len(diffeng2) - 1):
        matrix2[i][0] = diffeng2[i]
    return matrix1 ,matrix2




# normalization
dataRMC = load_and_process_RMC(train_dataRMC)
dataRPM = load_and_process_RPM(train_dataRPM)

X_train = dataRMC[0]
X_traincap = dataRMC[1]
X_trainRMC = dataRPM[0]

scaler_distance = preprocessing.StandardScaler().fit(X_train)  # definition du "normalisateur" pour la distance
scaler_heading = preprocessing.StandardScaler().fit(X_traincap)  # definition du "normalisateur" pour les caps
scaler_RPM = preprocessing.StandardScaler().fit(X_trainRMC)  # definition du "normalisateur" pour les caps
X_train = preprocessing.scale(X_train)
X_traincap = preprocessing.scale(X_traincap)
X_trainRMC = preprocessing.scale(X_trainRMC)

# definition of estimator
clf = svm.OneClassSVM(nu=0.007, kernel="rbf", gamma=0.7)
clf.fit(X_train)
clfcap = svm.OneClassSVM(nu=0.02, kernel="rbf", gamma=0.5)
clfcap.fit(X_traincap)
clfeng = svm.OneClassSVM(nu=0.007, kernel="rbf", gamma=0.5)
clfeng.fit(X_trainRMC)


print("UDP receive IP: %s" % UDP_IPrec)
print("UDP receive port: %s" % UDP_PORTrec)
sockrec = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockrec.bind((UDP_IPrec, UDP_PORTrec))

differed_start_RMC = 3  # number of RMC data before test (must be at least 3)
differed_strat_RPM = 2  # number of RMC data before test (must be at least 3)
n_data_RMC = 0
n_data_RPM = 0
data_test_RMC = []  # list of current RMC data to test
data_test_RPM = []  # list of current RPM data to test

try:
    while True:

        # reception of data, parsing
        data = sockrec.recvfrom(1024)
        data = data[0].decode("utf-8")
        message = pynmea2.parse(data)

        # test for RPM data
        # if message.sentence_type == "RMC":
        #     n_data_RPM = n_data_RPM + 1
        #     data_test_RPM.append(message.data[2])
        # if message.sentence_type == "RMC" and n_data_RMC >= differed_strat_RPM - 1:
        #     n_data_RPM = n_data_RPM + 1
        #     data_test_RPM.append(message.data[2])
        #     diffRPM = float(data_test_RPM[0])-float(data_test_RPM[1])
        #     y_pred_test_distance = clfeng.predict(scaler_RPM.transform([[diffRPM]]))
        #     if y_pred_test_distance == -1:
        #         spoofingdetectengine = True
        #         print("Tout va bien pour le moteur")
        #     else:
        #         spoofingdetectengine = False
        #         print("Leurrage détécté  moteur !")

        # test for RMC data
        # initialization
        if message.sentence_type == "RMC":
            n_data_RMC = n_data_RMC + 1
        if message.sentence_type == "RMC" and n_data_RMC == differed_start_RMC - 2:
            data_test_RMC.append(message.data[2])
            data_test_RMC.append(message.data[4])
        if message.sentence_type == "RMC" and n_data_RMC == differed_start_RMC - 1:
            data_test_RMC.append(message.data[2])
            data_test_RMC.append(message.data[4])

        # add current data
        if message.sentence_type == "RMC" and n_data_RMC >= differed_start_RMC:
            data_test_RMC.append(message.data[2])
            data_test_RMC.append(message.data[4])
            distancepoint = distance(data_test_RMC[2], data_test_RMC[4], data_test_RMC[3], data_test_RMC[5])
            capinit = heading([float(data_test_RMC[0]), float(data_test_RMC[2])],
                          [float(data_test_RMC[1]), float(data_test_RMC[3])])
            capfin = heading([float(data_test_RMC[2]), float(data_test_RMC[4])], [float(data_test_RMC[3]), float(data_test_RMC[5])])
            difference_heading = float(capfin[0]) - float(capinit[0])
            X_test_distance = [[message.data[6], distancepoint]]
            X_test_heading = [[message.data[6], difference_heading]]

            # prediction on current data
            y_pred_test_distance = clf.predict(scaler_distance.transform(X_test_distance))
            y_pred_test_heading = clfcap.predict(scaler_heading.transform(X_test_heading))

            if y_pred_test_distance == -1 and y_pred_test_heading == -1:
                spoof_detect_heading = True
                spoof_detect_distance = True  # le point est une anomalie de distance et heading
                print('Spoofing detected, distance and heading !')
            elif y_pred_test_heading == -1 and y_pred_test_distance == 1:
                spoof_detect_distance = False
                spoof_detect_heading = True  # le point est une anomalie de heading
                print('Spoofing detected, heading !')
            elif y_pred_test_heading == 1 and y_pred_test_distance == -1:
                spoof_detect_distance = True
                spoof_detect_heading = False  # le point est une anomalie de distance
                print('Spoofing detected, distance !')
            else:
                spoof_detect_distance = False  # le point est bon
                spoof_detect_heading = False
                print('Everything is find for position...')


            # delete old data
            data_test_RMC.pop(0)
            data_test_RMC.pop(0)

except KeyboardInterrupt:
    raise
