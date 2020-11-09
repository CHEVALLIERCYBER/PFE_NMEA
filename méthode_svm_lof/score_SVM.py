
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

# @Titre : Scoring SVM cap et distance

#------------------------------------------------------------------------

# @Description :
#ce code permet de tester en même temps le cap et la distance avec des algorithme de detection SVM
#Chaque évaluateur a ses paramètres optimaux, déterminés grâce aux programmes de matrice de confusion

#Des trames NMEA doivent être fournies en entrée en temps réél, sur le port 5005.
#Ce programme utilise les données de RMCbien.json comme données d'entrainement

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



# chargement des données du train set
#entrez le chemin d'accès au fichier RMCbien.json
train_dataRMC = open()


# normalisation
dataRMC = loadnprocessRMC(train_dataRMC)

X_train = dataRMC[0]
X_traincap = dataRMC[1]


scaler = preprocessing.StandardScaler().fit(X_train)  # definition du "normalisateur" pour la distance
scaler1 = preprocessing.StandardScaler().fit(X_traincap)  # definition du "normalisateur" pour les caps

X_train = preprocessing.scale(X_train)
X_traincap = preprocessing.scale(X_traincap)


# definition du modèle et entrainement
clf = svm.OneClassSVM(nu=0.007, kernel="rbf", gamma=0.7)
clf.fit(X_train)
clfcap = svm.OneClassSVM(nu=0.02, kernel="rbf", gamma=0.5)
clfcap.fit(X_traincap)


# definition des ports
UDP_IPrec = "127.0.0.1"
UDP_IPenv = "127.0.0.1"
UDP_PORTrec = 5005  # socket entrée (bridge command)
UDP_PORTenv = 10110  # socket de sortie (open CPN)

print("UDP receive IP: %s" % UDP_IPrec)
print("UDP target IP: %s" % UDP_IPenv)
print("UDP receive port: %s" % UDP_PORTrec)
print("UDP target port: %s" % UDP_PORTenv)




# création des socket d'entrée et sortie
sockrec = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockenv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockrec.bind((UDP_IPrec, UDP_PORTrec))

departdiff = 3  # compteur de trame avant debut du test
departdiffRPM = 2
ntrameRMC = 0  # compteur de trame
ntrameRPM = 0
donneestest = []  # liste contenant les données en cours, à tester


scoretrame = 0  # compte des trames bien classifiées
faussedetec = 0  # compteur de fausses detections

frequencebrouil = 0.10  # frenquence des trames changées
# offset de latitude et longitude ajoutés aux trames modifiées
# pas encore testé seuil de detection si score en fonction de l'offset
offsetlat = float(0.45 * np.random.random_sample(1) + 0.05)
offsetlong = float(0.45 * np.random.random_sample(1) + 0.05)


# booléen permetant d'identifier une trame suivant l'application d'un offset (comme la distance est calculée entre
# deux points, le brouillage entraine 2 sautes de distance, une avec le point précédent et une avec le point suivant)
modiftramesuivante = False
modiftramesuivantedeux = False

try:
    while ntrameRMC < 102:

        # reception des données, parsing
        data = sockrec.recvfrom(1024)
        data = data[0].decode("utf-8")
        message = pynmea2.parse(data)

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
            print(ntrameRMC)
            if np.random.random_sample(1) < frequencebrouil:
                modif = float(message.data[2]) + offsetlat
                message.data[2] = str(modif)
                modif = float(message.data[4]) + offsetlong
                message.data[4] = str(modif)
                brouilvrai = True  # la trame est modifiée
                brouilvraicap = True
                modiftramesuivante = True
                print('brouillage')
            elif modiftramesuivante:  # la trame suit directement une trame modifiée (voir commentaire sur
                # modiftramesuivante)
                print("le brouillage vient de s'arreter")
                brouilvrai = True
                brouilvraicap = True
                modiftramesuivante = False
                modiftramesuivantedeux = True
            elif modiftramesuivantedeux:  # la trame suit directement une trame modifiée (voir commentaire sur
                # modiftramesuivante)
                print("deuxieme trame apres brouillage")
                brouilvraicap = True
                brouilvrai = False
                modiftramesuivantedeux = False
            else:
                print('pas brouillage...')
                brouilvraicap = False
                brouilvrai = False  # la trame est bonne

            # analyse de la trame
            # mise en forme de la donnée et calcul de la distance, puis application du modèle

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
                print('Brouillage détecté distance et cap !')
            elif y_pred_testcap == -1 and y_pred_test == 1:
                brouildetec = False
                brouildeteccap = True  # le point est une anomalie de cap
                print('Brouillage détecté cap !')
            elif y_pred_testcap == 1 and y_pred_test == -1:
                brouildetec = True
                brouildeteccap = False  # le point est une anomalie de distance
                print('Brouillage détecté distance !')
            else:
                brouildetec = False  # le point est bon
                brouildeteccap = False
                print('Tout va bien')
            # Verification pour scoring de la validité du resulat
            if ((not brouildetec and not brouildeteccap) and (brouilvraicap or brouilvrai)) or ((not brouilvrai and not brouilvraicap) and (brouildetec or brouildeteccap)):
                scoretrame = scoretrame + 1
            elif (brouildetec and not brouilvrai) or (brouildeteccap and not brouilvraicap):
                print('fausse detection...')
                faussedetec = faussedetec + 1

            # mise en memoire des données des points pour calcul de la prochaine distance
            donneestest.pop(0)
            donneestest.pop(0)

        # conversion en hexadecimal et envoie au socket de sortie
        data = bytes(str(message), 'utf-8')
        sockenv.sendto(data, (UDP_IPenv, UDP_PORTenv))

except KeyboardInterrupt:
    score = (scoretrame / (ntrameRMC - 2)) * 100  # calcul du score : pourcentage de trame bien identifiées
    print(score)
    raise

print('Sur ' + str(ntrameRMC - 2) + ' trames RMC testées, ')
print('trames bien classifiées :' + str(scoretrame))
print('pour ' + str(faussedetec) + ' fausses detctions')
score = (scoretrame / (ntrameRMC - 2)) * 100  # calcul du score : pourcentage de trame bien identifiées
print('le score est de : ' + str(score))
