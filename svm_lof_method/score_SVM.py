# ------------------------------------------------------------------------
#
# @Creators : EV2 CHEVALLIER & EV2 LEBIGRE
#
# @Date : 07.11.20
# @Location : École Navale / Chaire de Cyberdéfense des systèmes navals
# @Project : End of studies project
# @Subject : # Détection temps-réel d’anomalies cyber # sur un réseau NMEA par l’utilisation de # techniques d’apprentissage automatique.
#            # Detection of cyber anomalies in real time on NMEA network by using machine learning
# ------------------------------------------------------------------------
# @Titre : Score_SVM
# ------------------------------------------------------------------------
# @Description :
# This code is used to determine the score of a program that uses one evaluator for distances and for for headings
# Those two evaluators have the best parameters (determined with programs matrix_score_distance and matrix_score_heading)
# NMEA must be provided in real time, on port 5005 (you can modify the port).
#
# This program uses files RMC_45min_dataset.json and RPM_45min_dataset.json as training data
# (specify the access path at the start).
#
# You can can modify the type of spoofing and orther test parameters
# ------------------------------------------------------------------------

##################################################################################################

# loading of train set data, enter access path
train_dataRMC = open('n')

# ports used
UDP_IPrec = "127.0.0.1"  # entry IP
UDP_IPenv = "127.0.0.1"  # exit IP
UDP_PORTrec = 5005  # entry socket  (bridge command)
UDP_PORTenv = 10110  # exit socket  (open CPN)

# Parameters
number_to_test = 100  # number of NMEA sentences to test
frequencebrouil = 0.10  # frequency of spoofing
differate_start = 3  # number of sentences before the start of test (must be at least 3)


# type of spofing used
def spoofing(old_lat, old_long):
    offsetlat = float(0.0045 * np.random.random_sample(1) + 0.005)
    offsetlong = float(0.0045 * np.random.random_sample(1) + 0.005)

    modif = float(old_lat) + offsetlat
    new_lat = str(modif)
    modif = float(old_long) + offsetlong
    new_long = str(modif)

    return new_lat, new_long


#################################################################################################


import numpy as np
import pynmea2
import json
import math
import socket
from sklearn import preprocessing
from sklearn import svm


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

dataRMC = load_and_process_RMC(train_dataRMC)
X_train_distance = dataRMC[0]
X_train_heading = dataRMC[1]
scaler_distance = preprocessing.StandardScaler().fit(X_train_distance)  # definition du "normalisateur" pour la distance
scaler_heading = preprocessing.StandardScaler().fit(X_train_heading)  # definition du "normalisateur" pour les caps

X_train_distance = preprocessing.scale(X_train_distance)
X_train_heading = preprocessing.scale(X_train_heading)

# definition of evaluator and training
evaluator_distance = svm.OneClassSVM(nu=0.007, kernel="rbf", gamma=0.7)
evaluator_distance.fit(X_train_distance)
evaluator_heading = svm.OneClassSVM(nu=0.02, kernel="rbf", gamma=0.5)
evaluator_heading.fit(X_train_heading)

print("UDP receive IP: %s" % UDP_IPrec)
print("UDP target IP: %s" % UDP_IPenv)
print("UDP receive port: %s" % UDP_PORTrec)
print("UDP target port: %s" % UDP_PORTenv)
sockrec = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockenv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockrec.bind((UDP_IPrec, UDP_PORTrec))


RMC_sentence_number = 0
test_data = []
score = 0
false_detec = 0

# booléen permetant d'identifier une trame suivant l'application d'un offset (comme la distance est calculée entre
# deux points, le brouillage entraine 2 sautes de distance, une avec le point précédent et une avec le point suivant)
modif_next_sentence = False
modif_next_sentence_two = False

try:
    while RMC_sentence_number < number_to_test:

        # reception des données, parsing
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

            alea = float(np.random.random_sample(1))
            if alea > 0.5:
                offsetlat = float(0.005)
                offsetlong = 0
            else:
                offsetlat = 0
                offsetlong = float(0.005)

            if np.random.random_sample(1) < frequencebrouil:
                #modification
                message.data[2], message.data[4] = spoofing(message.data[2], message.data[4])

                spoof_true_distance = True
                spoof_true_heading = True
                modif_next_sentence = True
                print('Spoofing')
            elif modif_next_sentence:
                print("Spoofing just stop")
                spoof_true_distance = True
                spoof_true_heading = True
                modif_next_sentence = False
                modif_next_sentence_two = True
            elif modif_next_sentence_two:

                print("Second sentence after spoofing")
                spoof_true_heading = True
                spoof_true_distance = False
                modif_next_sentence_two = False
            else:
                print('No spoofing...')
                spoof_true_heading = False
                spoof_true_distance = False

            # sentence analysis

            test_data.append(message.data[2])
            test_data.append(message.data[4])
            distance_sentence = distance(test_data[2], test_data[4], test_data[3], test_data[5])
            first_heading = heading([float(test_data[0]), float(test_data[2])],
                          [float(test_data[1]), float(test_data[3])])
            last_heading = heading([float(test_data[2]), float(test_data[4])], [float(test_data[3]), float(test_data[5])])
            diff_heading = float(last_heading[0]) - float(first_heading[0])
            X_sentence_dist = [[message.data[6], distance_sentence]]
            X_sentence_head = [[message.data[6], diff_heading]]
            prediction_distance = evaluator_distance.predict(scaler_distance.transform(X_sentence_dist))
            prediction_heading = evaluator_heading.predict(scaler_heading.transform(X_sentence_head))

            if prediction_distance == -1 and prediction_heading == -1:
                spoof_detec_heading = True
                spoof_detec_distance = True
                print('Spoofing detected, distance and heading')
            elif prediction_heading == -1 and prediction_distance == 1:
                spoof_detec_distance = False
                spoof_detec_heading = True
                print('Spoofing detected, heading !')
            elif prediction_heading == 1 and prediction_distance == -1:
                spoof_detec_distance = True
                spoof_detec_heading = False
                print('Spoofing detected, distance !')
            else:
                spoof_detec_distance = False
                spoof_detec_heading = False
                print('Everything is find')
            # Verification pour scoring de la validité du resulat
            if not (((not spoof_detec_distance and not spoof_detec_heading) and (spoof_true_heading or spoof_true_distance)) or (
                    (not spoof_true_distance and not spoof_true_heading) and (spoof_detec_distance or spoof_detec_heading))):
                score = score + 1
            elif (spoof_detec_distance and not spoof_true_distance) or (spoof_detec_heading and not spoof_true_heading):
                print('False detection...')
                false_detec = false_detec + 1

            # mise en memoire des données des points pour calcul de la prochaine distance
            test_data.pop(0)
            test_data.pop(0)

        # conversion en hexadecimal et envoie au socket de sortie
        data = bytes(str(message), 'utf-8')
        sockenv.sendto(data, (UDP_IPenv, UDP_PORTenv))

except KeyboardInterrupt:
    score = (score / (RMC_sentence_number - 2)) * 100  # calcul du score : pourcentage de trame bien identifiées
    print(score)
    raise

print('On ' + str(RMC_sentence_number - 2) + ' sentences tested ')
print('sentences correctly classified : ' + str(score))
print('for ' + str(false_detec) + ' false detections')
score = (score / (RMC_sentence_number - 2)) * 100  # calcul du score : pourcentage de trame bien identifiées
print('Score is ' + str(score) + ' % ')
