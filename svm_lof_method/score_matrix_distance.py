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
# @Titre : Score matrix distance
#------------------------------------------------------------------------
# @Description :
#This code is used to determine the best estimator to classify distance data
# NMEA must be provided in real time, on port 5005 (you can modify the port).
#
# This program uses files RMC_45min_dataset.json and RPM_45min_dataset.json as training data
# (specify the access path at the start).
#
# You can can modify the type of spoofing and orther test parameters
#------------------------------------------------------------------------

import numpy as np
import pynmea2
import json
import math
import socket
from sklearn import preprocessing
from sklearn import svm
from sklearn.neighbors import LocalOutlierFactor


##################################################################################################

# loading of train set data, enter access path
train_dataRMC = open('')
train_dataRPM = open('')

# ports used
UDP_IPrec = "127.0.0.1" # entry IP
UDP_IPenv = "127.0.0.1" # exit IP
UDP_PORTrec = 5005  # entry socket  (bridge command)
UDP_PORTenv = 10110  # exit socket  (open CPN)

# Parameters
number_to_test = 100 #number of NMEA sentences to test
frequencebrouil = 0.10  # frequency of spoofing
differate_start = 3  # number of sentences before the start of test (must be at least 3)

#type of spofing used
def spoofing (old_lat,old_long):

    offsetlat = float(0.0045 * np.random.random_sample(1) + 0.005)
    offsetlong = float(0.0045 * np.random.random_sample(1) + 0.005)

    modif = float(old_lat) + offsetlat
    new_lat = str(modif)
    modif = float(old_long) + offsetlong
    new_long = str(modif)

    return new_lat, new_long

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

#Evaluation of the current estimator
def testeval (est_dist, est_head, X_dist, X_head, true_spoof, scaler) :
    prediction_distance = est_dist.predict(scaler.transform(X_dist))  # prediction (apres normalisation)

    if prediction_distance == -1:
        spoof_detec = True
    else:
        spoof_detec = False
    if spoof_detec == true_spoof:
        score_sentence = 1
    else:
        score_sentence = 0
    if spoof_detec and not true_spoof:
        miss = 1
    else:
        miss = 0

    return score_sentence, miss


# normalisation
dataRMC = load_and_process_RMC(train_dataRMC)
X_train_distance = dataRMC[0]
X_train_heading = dataRMC[1]
scaler_distance = preprocessing.StandardScaler().fit(X_train_distance)  # definition du "normalisateur" pour la distance
scaler_heading = preprocessing.StandardScaler().fit(X_train_heading)  # definition du "normalisateur" pour les caps

X_train_distance = preprocessing.scale(X_train_distance)
X_train_heading = preprocessing.scale(X_train_heading)

evaluateur = []
estimator_name = []

estimator_name.append("SVM distance type : linear ")
listetypekernel = ["linear", "poly", "rbf", "sigmoid"]
for kernel in listetypekernel:
    print(kernel)
    for i in range(1, 10):
        for j in range(1, 10):
            print(i)
            clf_distance = svm.OneClassSVM(nu=0.01 * i, kernel=kernel, gamma=0.1 * j)
            clf_distance.fit(X_train_distance)
            clf_heading = svm.OneClassSVM(nu=0.007, kernel="rbf", gamma=0.7)
            clf_heading.fit(X_train_heading)
            evaluateur.append([clf_distance, clf_heading])
            estimator_name.append(
                "SVM distance type : " + kernel + " nu = " + str(round(0.01 * i, 3)) + " gamma = " + str(
                    round(0.1 * j, 2)))
for i in range(20):
    for j in range(1, 20):
        clf_distance = LocalOutlierFactor(n_neighbors=i + 10, novelty=True, contamination=0.01 * j)
        clf_distance.fit(X_train_distance)
        clf_heading = LocalOutlierFactor(n_neighbors=20, novelty=True, contamination=0.1)
        clf_heading.fit(X_train_heading)
        evaluateur.append([clf_distance, clf_heading])
        estimator_name.append("LOF distance n = " + str(round(i + 10, 1)) + "contamination = " + str(round(0.01 * j, 2)))

# list of score for each estimator
score_estimator = [0] * len(evaluateur)
miss_estimator = [0] * len(evaluateur)

print("UDP receive IP: %s" % UDP_IPrec)
print("UDP target IP: %s" % UDP_IPenv)
print("UDP receive port: %s" % UDP_PORTrec)
print("UDP target port: %s" % UDP_PORTenv)

# creation of sockets
sockrec = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockenv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockrec.bind((UDP_IPrec, UDP_PORTrec))

test_data = []  # list of curent data
RMC_sentence_number = 0  # number of RMC sentences

# variables used to indicate the sentence just after the end of spoofing (because distance and heading are calculated with 3 consecutive sentences)
# the 3 next classifications are affected by the spoofing as well even it is finished
modif_next_sentence = False
modif_next_sentence_two = False

try:
    while RMC_sentence_number < number_to_test:

        # parsing of data
        data = sockrec.recvfrom(1024)
        data = data[0].decode("utf-8")
        message = pynmea2.parse(data)

        # Initialization
        if message.sentence_type == "RMC":
            RMC_sentence_number = RMC_sentence_number + 1
        if message.sentence_type == "RMC" and RMC_sentence_number == differate_start - 2:
            test_data.append(message.data[2])
            test_data.append(message.data[4])
        if message.sentence_type == "RMC" and RMC_sentence_number == differate_start - 1:
            test_data.append(message.data[2])
            test_data.append(message.data[4])

        # Spoofing
        if message.sentence_type == "RMC" and RMC_sentence_number >= differate_start:
            print(RMC_sentence_number)
            if np.random.random_sample(1) < frequencebrouil:

                message.data[2], message.data[4] = spoofing(message.data[2], message.data[4])

                spoof_distance = True
                spoof_heading = True
                modif_next_sentence = True
                print('Spoofing')
            elif modif_next_sentence:
                # modif_next_sentence)
                print("Spoofing just stopped")
                spoof_distance = True
                spoof_heading = True
                modif_next_sentence = False
                modif_next_sentence_two = True
            elif modif_next_sentence_two:
                print("Second RMC sentence after spoofing")
                spoof_heading = True
                spoof_distance = False
                modif_next_sentence_two = False
            else:
                print('No spoofing')
                spoof_heading = False
                spoof_distance = False

                # sentence analysis and scoring

            test_data.append(message.data[2])
            test_data.append(message.data[4])
            distance_sentence = distance(test_data[2], test_data[4], test_data[3], test_data[5])
            first_heading = cap([float(test_data[0]), float(test_data[2])],
                                [float(test_data[1]), float(test_data[3])])
            last_heading = cap([float(test_data[2]), float(test_data[4])], [float(test_data[3]), float(test_data[5])])
            diff_heading = float(last_heading[0]) - float(first_heading[0])
            X_sentence_dist = [[message.data[6], distance_sentence]]
            X_sentence_head = [[message.data[6], diff_heading]]

            # scoring for each estimator
            for i in range(0, len(evaluateur)):
                scoring = testeval(evaluateur[i][0], evaluateur[i][1], X_sentence_dist, X_sentence_head, spoof_distance, scaler_distance)
                score_estimator[i] = score_estimator[i] + scoring[0]
                miss_estimator[i] = miss_estimator[i] + scoring[1]

            # delete old data
            test_data.pop(0)
            test_data.pop(0)

        # data to exit socket
        data = bytes(str(message), 'utf-8')
        sockenv.sendto(data, (UDP_IPenv, UDP_PORTenv))

except KeyboardInterrupt:
    raise

name_best = ""
best_score = score_estimator[0]
for i in range(len(score_estimator)):
    if score_estimator[i] > best_score:
        best_score = score_estimator[i]
        name_best = estimator_name[i]
    print(estimator_name[i] + " - " + str(score_estimator[i] * 100 / (RMC_sentence_number - 2)) + "% for " + str(
        miss_estimator[i] * 100 / (RMC_sentence_number - 2)) + "% positive miss")
print(name_best + " is the best estimator with a score of " + str(best_score * 100 / (RMC_sentence_number - 2)))
