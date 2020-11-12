#------------------------------------------------------------------------
#
# @Auteurs : EV2 CHAVELLIER
#
# @Date : 06.11.20
# @Lieu : École Navale / Chaire de Cyberdéfense des systèmes navals
# @Cadre : Projet de Fin d'Études
# @Sujet : # Détection temps-réel d’anomalies cyber # sur un réseau NMEA par l’utilisation de # techniques d’apprentissage automatique.
#
#------------------------------------------------------------------------
# @Titre : Prediction de leurrage
#------------------------------------------------------------------------
# @Description : # Ce programme définit les fonctions statistiques utiles pour les calculs suivants : moyenne, écart-type, différence entre deux valeurs successives dans une liste 
#------------------------------------------------------------------------

import json
import math
import statistics as st

epsilon=0.0000000000001

def dissect(messages):
    dico = []
    for i in range(len(messages.data) - 1):
        dico.append((messages.fields[i][1], messages.data[i]))

    dico = dict(dico)
    return json.dumps(dico) # retourne


def load(file):
    list_phi = []
    list_g = []
    list_t = []
    list_vitesse=[]
    list_cap=[]

    resultat=[[]]
    for line in file:
        trame = json.loads(line)
        #print(str(trame['status']))

        if str(trame['status'])=="A":

            list_phi.append(float(trame["lat"]))
            list_g.append(float(trame["lon"]))
            list_t.append(float(trame["timestamp"]))
            list_vitesse.append(float(trame["spd_over_grnd"]))
            list_cap.append(float(trame["true_course"]))

        else:
            list_phi.append(0)
            list_g.append(0)
            list_t.append(0)
            list_vitesse.append(0)
            list_cap.append(0)


    resultat.append(list_phi)
    resultat.append(list_g)
    resultat.append(list_t)
    resultat.append(list_vitesse)
    resultat.append(list_cap)

    resultat.pop(0)
    return resultat # retourne les listes de chaque parametres : phi g et t

def load_gpxxx(file):
    list_phi = []
    list_g = []
    list_t = []

    resultat=[[]]
    for line in file:
        trame = json.loads(line)
        if (trame["lat_dir"]=='N'):
            list_phi.append(float(trame["lat"]))
        else:
            list_phi.append(-float(trame["lat"]))

        if (trame["lon_dir"] == 'W'):
            list_g.append(float(trame["lon"]))
        else:
            list_g.append(-float(trame["lon"]))

        list_g.append(float(trame["lon"]))
        list_t.append(float(trame["timestamp"]))

    resultat.append(list_phi)
    resultat.append(list_g)
    resultat.append(list_t)

    resultat.pop(0)
    return resultat # retourne les listes de chaque parametres : phi g et t

def delta(liste,list_t):  # list_phi ou list_g en minutes
    delta_liste = []
    for i in (range(len(liste) - 1)):
        if (list_t[i + 1] - list_t[i]) !=0:
            delta_liste.append( (liste[i + 1] - liste[i]) / (list_t[i + 1] - list_t[i]))  # écart en minutes d'arc
        else:
            delta_liste.append(0)
    return delta_liste

def delta_distance(l_phi,l_g): # retourne la liste des distances entre les pts successsifs
    delta_d = []
    for i in range(len(l_phi)-1):
        phi_m=(l_phi[i+1]+l_phi[i])*0.5
        d=math.sqrt((l_phi[i+1]-l_phi[i])**2 + ((l_g[i+1]-l_g[i])/math.cos(phi_m))**2)
        delta_d.append(d)
    return delta_d

def cap(l_phi,l_g): # phi g en minutes

    cap=[]

    for i in range(len(l_phi)-1):

        if abs(l_phi[i+1]-l_phi[i])<epsilon and l_g[i+1]<l_g[i]:
            cv=90
            cap.append(60.*cv)

        elif abs(l_phi[i+1]-l_phi[i])<epsilon and l_g[i+1]>l_g[i]:
            cv=270
            cap.append(60.*cv)

        elif l_phi[i+1]>l_phi[i] and abs(l_g[i+1]-l_g[i])<epsilon:
            cv=0
            cap.append(60.*cv)

        elif (l_phi[i+1]<l_phi[i] and abs(l_g[i+1]-l_g[i])<epsilon):
            cv=180
            cap.append(60.*cv)

        elif (abs(l_phi[i+1]<l_phi[i])<epsilon and abs(l_g[i+1]-l_g[i])<epsilon):
            cv=0
            cap.append(60.*cv)

        else:
            cos_phi_m = math.cos(0.5 * (l_phi[i + 1] + l_phi[i]))
            delta_phi = l_phi[i + 1] - l_phi[i]
            delta_g = l_g[i + 1] - l_g[i]
            #print(delta_g)

            a=(180./math.pi)*abs(math.atan(cos_phi_m*delta_phi/delta_g))

            if (l_phi[i+1]>l_phi[i] and l_g[i+1]<l_g[i]):
                cv=90-a
                cap.append(60.*cv) # cap en minutes

            elif (l_phi[i+1]>l_phi[i] and l_g[i+1]>l_g[i]):
                cv=270+a
                cap.append(60.*cv)

            elif (l_phi[i+1]<l_phi[i] and l_g[i+1]>l_g[i]):
                cv=270-a
                cap.append(60.*cv)

            else: #l_phi[i+1]>l_phi[i] and l_g[i+1]<l_g[i]:
                cv=90+a
                cap.append(60.*cv)

    return cap

def vitesse(l_phi,l_g,l_t):

    vitesse=[]

    for i in range(len(l_phi)-1):
        if abs(l_t[i+1]-l_t[i])>epsilon:

            delta_t=l_t[i+1]-l_t[i]
            cos_phi_m=math.cos(0.5*(l_phi[i+1]+l_phi[i]))
            delta_phi=l_phi[i+1]-l_phi[i]
            delta_g=l_g[i+1]-l_g[i]
            print("delta_t : ", delta_t)

            vf=60*60.*(math.sqrt(delta_phi**2 + (delta_g/cos_phi_m)**2) / delta_t )# duree en s
            vitesse.append(vf)
        else:
            vitesse.append(0)
    return vitesse

def parametres(array_data):

    res={}
    res["moyenne"]=st.mean(array_data)
    res["ecart-type"]=math.sqrt(st.variance(array_data))
    return res

test_jamming=open("/home/guillaume/PFE/GNSS_LOG/GPS/01_09_2020_jamming_gps_rmc.log.json")
load(test_jamming)
