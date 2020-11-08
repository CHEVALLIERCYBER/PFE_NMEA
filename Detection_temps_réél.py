
#------------------------------------------------------------------------

#

# @Auteurs : EV2 CHEVALLIER & EV2 LEBIGRE

#

# @Date : 07.11.20

# @Lieu : École Navale / Chaire de Cyberdéfense des systèmes navals

# @Cadre : Projet de Fin d'Études

# @Sujet : # Détection temps-réel d’anomalies cyber # sur un réseau NMEA par l’utilisation de # techniques d’apprentissage automatique.

#

#------------------------------------------------------------------------

# @Titre : Detection temps réél finale

#------------------------------------------------------------------------

# @Description : Ce code est la version finale du programme de détection que nous avons créé. Il détecte en temps réél
#les anomalies des trames NMEA fournies en entrée, sur le port 5005.

# En sortie, pour recuperer la classification faite par le programme, il suffit de recuperer les booléen brouildetec et
# brouildeteccap, si l'un est vrai, un leurrage est détecté par le programme

#Une tentative de détection d'anomalies moteur sur les trames RPM est présente en commentaire

#------------------------------------------------------------------------


import numpy as np
import pynmea2
import json
import math
import socket
from sklearn import preprocessing
from sklearn import svm



# calcul du cap (il faut trois latitude et trois longitude minimum pour calculer)
def cap(l_phi, l_g):
    epsilon = 10 ** (-13)
    capcalcul = []
    for i in range(len(l_phi) - 1):

        if abs(l_phi[i + 1] - l_phi[i]) < epsilon and l_g[i + 1] <= l_g[i]:
            cv = 90
            capcalcul.append(cv)

        elif abs(l_phi[i + 1] - l_phi[i]) < epsilon and l_g[i + 1] > l_g[i]:
            cv = 270
            capcalcul.append(cv)

        elif l_phi[i + 1] >= l_phi[i] and abs(l_g[i + 1] - l_g[i]) < epsilon:
            cv = 0
            capcalcul.append(cv)

        elif l_phi[i + 1] < l_phi[i] and abs(l_g[i + 1] - l_g[i]) < epsilon:
            cv = 180
            capcalcul.append(cv)

        else:

            a = (180. / math.pi) * abs(math.atan(
                math.cos(0.5 * (l_phi[i + 1] + l_phi[i])) * (l_phi[i + 1] - l_phi[i]) / (l_g[i + 1] - l_g[i])))

            if l_phi[i + 1] > l_phi[i] and l_g[i + 1] < l_g[i]:
                cv = 90 - a
                capcalcul.append(cv)

            elif l_phi[i + 1] > l_phi[i] and l_g[i + 1] > l_g[i]:
                cv = 270 + a
                capcalcul.append(cv)

            elif l_phi[i + 1] < l_phi[i] and l_g[i + 1] > l_g[i]:
                cv = 270 - a
                capcalcul.append(cv)

            else:  # l_phi[i+1]>l_phi[i] and l_g[i+1]<l_g[i]:
                cv = 90 + a
                capcalcul.append(cv)
    return capcalcul


# calcul distance
def distance(phi1, phi0, g1, g0):
    return np.sqrt(
        (float(phi1) - float(phi0)) ** 2 + ((float(g1) - float(g0)) / ((float(phi1) + float(phi0)) / 2)) ** 2)


def diffliste(liste):
    listediff = []
    for i in range(1, len(liste) - 1):
        listediff.append(liste[i] - liste[i - 1])
    return listediff


# mise en forme des données RMC, preprocessing
def loadnprocessRMC(file):
    list_phi = []
    list_g = []
    list_t = []
    list_v = []
    resultat = [[]]
    for line in file:
        trame = json.loads(line)
        list_phi.append(float(trame["lat"]))
        list_g.append(float(trame["lon"]))
        list_t.append(float(trame["timestamp"]))
        list_v.append(float(trame["spd_over_grnd"]))
    resultat.append(list_phi)
    resultat.append(list_g)
    resultat.append(list_t)
    resultat.append(list_v)
    resultat.pop(0)
    dist = [0, 0]
    for i in range(1, len(resultat[0]) - 1):
        dist.append(distance(resultat[0][i], resultat[0][i - 1], resultat[1][i], resultat[1][i - 1]))
    matrix1 = np.zeros((len(dist), 2))
    listecap = cap(list_phi, list_g)
    diffecap = diffliste(listecap)
    for i in range(0, len(dist) - 1):
        matrix1[i][0] = (resultat[3][i])
        matrix1[i][1] = dist[i]
    i = 0
    fin = len(matrix1) - 1
    # preprocessing du data train : suppression des points abérants
    while i < fin:
        if matrix1[i][1] > 7:
            matrix1 = np.delete(matrix1, i, 0)
            fin = fin - 1
        i = i + 1
    matrix2 = np.zeros((len(diffecap), 2))
    for i in range(0, len(diffecap) - 1):
        matrix2[i][0] = (resultat[3][i])
        matrix2[i][1] = diffecap[i]

    return matrix1, matrix2


def loadnprocessRPM (file):
    list_rpm_eng1 = []
    list_rpm_eng2 = []
    for line in file:
        trame = json.loads(line)
        if trame["engine_no"] == "1":
            list_rpm_eng1.append(float(trame["speed"]))
        else:
            list_rpm_eng2.append(float(trame["speed"]))
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



# chargement des données du train set
train_dataRMC = open('C:/Users/tlebi/Desktop/PFE/RMCbien.json')
train_dataRPM = open('C:/Users/tlebi/Desktop/PFE/RPMbien.json')

# normalisation
dataRMC = loadnprocessRMC(train_dataRMC)
dataRPM = loadnprocessRPM(train_dataRPM)

X_train = dataRMC[0]
X_traincap = dataRMC[1]
X_trainRMC = dataRPM[0]

scaler = preprocessing.StandardScaler().fit(X_train)  # definition du "normalisateur" pour la distance
scaler1 = preprocessing.StandardScaler().fit(X_traincap)  # definition du "normalisateur" pour les caps
scalerRPM = preprocessing.StandardScaler().fit(X_trainRMC)  # definition du "normalisateur" pour les caps
X_train = preprocessing.scale(X_train)
X_traincap = preprocessing.scale(X_traincap)
X_trainRMC = preprocessing.scale(X_trainRMC)

# definition du modèle et entrainement
clf = svm.OneClassSVM(nu=0.007, kernel="rbf", gamma=0.7)
clf.fit(X_train)
clfcap = svm.OneClassSVM(nu=0.02, kernel="rbf", gamma=0.5)
clfcap.fit(X_traincap)
clfeng = svm.OneClassSVM(nu=0.007, kernel="rbf", gamma=0.5)
clfeng.fit(X_trainRMC)


# definition des ports
UDP_IPrec = "127.0.0.1"
UDP_PORTrec = 5005  # socket entrée (bridge command)

print("UDP receive IP: %s" % UDP_IPrec)
print("UDP receive port: %s" % UDP_PORTrec)


# création des socket d'entrée et sortie
sockrec = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sockrec.bind((UDP_IPrec, UDP_PORTrec))

departdiff = 3  # compteur de trame avant debut du test
departdiffRPM = 2
ntrameRMC = 0  # compteur de trame
ntrameRPM = 0
donneestest = []  # liste contenant les données en cours, à tester
donneestestRPM = []  # liste contenant les données RPM en cours, à tester

try:
    while True:

        # reception des données, parsing
        data = sockrec.recvfrom(1024)
        data = data[0].decode("utf-8")
        message = pynmea2.parse(data)

        #test pour donnée RPM
        # if message.sentence_type == "RMC":
        #     ntrameRPM = ntrameRPM + 1
        #     donneestestRPM.append(message.data[2])
        # if message.sentence_type == "RMC" and ntrameRMC >= departdiffRPM - 1:
        #     ntrameRPM = ntrameRPM + 1
        #     donneestestRPM.append(message.data[2])
        #     diffRPM = float(donneestestRPM[0])-float(donneestestRPM[1])
        #     y_pred_test = clfeng.predict(scalerRPM.transform([[diffRPM]]))
        #     if y_pred_test == -1:
        #         brouildetecmoteur = True
        #         print("Tout va bien pour le moteur")
        #     else:
        #         brouildetecmoteur = False
        #         print("Leurrage détécté  moteur !")

        # test pour donnée RMC
        # sequence de comptage des première trames, initialisation des données
        if message.sentence_type == "RMC":
            ntrameRMC = ntrameRMC + 1
        if message.sentence_type == "RMC" and ntrameRMC == departdiff - 2:
            donneestest.append(message.data[2])
            donneestest.append(message.data[4])
        if message.sentence_type == "RMC" and ntrameRMC == departdiff - 1:
            donneestest.append(message.data[2])
            donneestest.append(message.data[4])
        # modification de trame, brouillage avec un offset de latitude et longitude
        if message.sentence_type == "RMC" and ntrameRMC >= departdiff:
            donneestest.append(message.data[2])
            donneestest.append(message.data[4])
            distancepoint = distance(donneestest[2], donneestest[4], donneestest[3], donneestest[5])
            capinit = cap([float(donneestest[0]), float(donneestest[2])],
                          [float(donneestest[1]), float(donneestest[3])])
            capfin = cap([float(donneestest[2]), float(donneestest[4])], [float(donneestest[3]), float(donneestest[5])])
            diffcap = float(capfin[0]) - float(capinit[0])
            X_test = [[message.data[6], distancepoint]]
            X_testcap = [[message.data[6], diffcap]]
            y_pred_test = clf.predict(scaler.transform(X_test))  # prediction (apres normalisation)
            y_pred_testcap = clfcap.predict(scaler1.transform(X_testcap))  # prediction (apres normalisation)

            if y_pred_test == -1 and y_pred_testcap == -1:
                brouildeteccap = True
                brouildetec = True  # le point est une anomalie de distance et cap
                print('Leurrage détecté distance et cap !')
            elif y_pred_testcap == -1 and y_pred_test == 1:
                brouildetec = False
                brouildeteccap = True  # le point est une anomalie de cap
                print('Leurrage détecté cap !')
            elif y_pred_testcap == 1 and y_pred_test == -1:
                brouildetec = True
                brouildeteccap = False  # le point est une anomalie de distance
                print('Leurrage détecté distance !')
            else:
                brouildetec = False  # le point est bon
                brouildeteccap = False
                print('Tout va bien pour la position')


            # mise en memoire des données des points pour calcul de la prochaine distance
            donneestest.pop(0)
            donneestest.pop(0)

        #En sortie, il suffit de recuperer les booléens brouildetec, brouildeteccap si l'un est vrai,
        #Un leurage est détecté par le programme


except KeyboardInterrupt:
    raise

