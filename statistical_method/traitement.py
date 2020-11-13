#------------------------------------------------------------------------
#
# @Author : EV2 CHEVALLIER
#
# @Date : 06.11.20
# @Location : École Navale / Chaire de Cyberdéfense des systèmes navals
# @Project : Projet de Fin d'Études
# @Subject : # Real time detection of cyber anomalies upon a NMEA network by using machine learning methods
#------------------------------------------------------------------------
# @Title : useful functions
#------------------------------------------------------------------------
# @Description : # This programm implement some useful functions : statistic calculations, opening of a json file, difference beetwen two lists...
#------------------------------------------------------------------------

import json
import math
import statistics as st

epsilon=0.0000000000001

def set_path():
    path="/home/guillaume/PFE/pythonProject/PFE_NMEA-main/" # put the correct path
    return path

def dissect(messages): # open a NMEA message formated with the python librairy pynmea2
    dico = []
    for i in range(len(messages.data) - 1):
        dico.append((messages.fields[i][1], messages.data[i]))

    dico = dict(dico)
    return json.dumps(dico) #


def load(file):  # open a json file containing NMEA sentences
    list_phi = []
    list_g = []
    list_t = []
    list_speed=[]
    list_heading=[]

    resultat=[[]]
    for line in file:
        sentence = json.loads(line)

        if str(sentence['status'])=="A":

            list_phi.append(float(sentence["lat"]))
            list_g.append(float(sentence["lon"]))
            list_t.append(float(sentence["timestamp"]))
            list_speed.append(float(sentence["spd_over_grnd"]))
            list_heading.append(float(sentence["true_course"]))

        else:
            list_phi.append(0)
            list_g.append(0)
            list_t.append(0)
            list_speed.append(0)
            list_heading.append(0)


    resultat.append(list_phi)
    resultat.append(list_g)
    resultat.append(list_t)
    resultat.append(list_speed)
    resultat.append(list_heading)

    resultat.pop(0)
    return resultat

def delta(liste,list_t):  # take a list of latitude or longitude and a list of time
    delta_liste = []
    for i in (range(len(liste) - 1)):
        if (list_t[i + 1] - list_t[i]) !=0:
            delta_liste.append( (liste[i + 1] - liste[i]) / (list_t[i + 1] - list_t[i]))
        else:
            delta_liste.append(0)
    return delta_liste

def delta_distance(l_phi,l_g): # return the list of the distances beetwen successives points
    delta_d = []
    for i in range(len(l_phi)-1):
        phi_m=(l_phi[i+1]+l_phi[i])*0.5
        d=math.sqrt((l_phi[i+1]-l_phi[i])**2 + ((l_g[i+1]-l_g[i])/math.cos(phi_m))**2)
        delta_d.append(d)
    return delta_d

def heading(l_phi,l_g):  # compute the list of the headings

    heading=[]

    for i in range(len(l_phi)-1):

        if abs(l_phi[i+1]-l_phi[i])<epsilon and l_g[i+1]<l_g[i]:
            cv=90
            heading.append(60.*cv)

        elif abs(l_phi[i+1]-l_phi[i])<epsilon and l_g[i+1]>l_g[i]:
            cv=270
            heading.append(60.*cv)

        elif l_phi[i+1]>l_phi[i] and abs(l_g[i+1]-l_g[i])<epsilon:
            cv=0
            heading.append(60.*cv)

        elif (l_phi[i+1]<l_phi[i] and abs(l_g[i+1]-l_g[i])<epsilon):
            cv=180
            heading.append(60.*cv)

        elif (abs(l_phi[i+1]<l_phi[i])<epsilon and abs(l_g[i+1]-l_g[i])<epsilon):
            cv=0
            heading.append(60.*cv)

        else:
            cos_phi_m = math.cos(0.5 * (l_phi[i + 1] + l_phi[i]))
            delta_phi = l_phi[i + 1] - l_phi[i]
            delta_g = l_g[i + 1] - l_g[i]
            #print(delta_g)

            a=(180./math.pi)*abs(math.atan(cos_phi_m*delta_phi/delta_g))

            if (l_phi[i+1]>l_phi[i] and l_g[i+1]<l_g[i]):
                cv=90-a
                heading.append(60.*cv) # heading en minutes

            elif (l_phi[i+1]>l_phi[i] and l_g[i+1]>l_g[i]):
                cv=270+a
                heading.append(60.*cv)

            elif (l_phi[i+1]<l_phi[i] and l_g[i+1]>l_g[i]):
                cv=270-a
                heading.append(60.*cv)

            else: #l_phi[i+1]>l_phi[i] and l_g[i+1]<l_g[i]:
                cv=90+a
                heading.append(60.*cv)

    return heading

def speed(l_phi,l_g,l_t):

    speed=[]

    for i in range(len(l_phi)-1):
        if abs(l_t[i+1]-l_t[i])>epsilon:

            delta_t=l_t[i+1]-l_t[i]
            cos_phi_m=math.cos(0.5*(l_phi[i+1]+l_phi[i]))
            delta_phi=l_phi[i+1]-l_phi[i]
            delta_g=l_g[i+1]-l_g[i]
            print("delta_t : ", delta_t)

            vf=60*60.*(math.sqrt(delta_phi**2 + (delta_g/cos_phi_m)**2) / delta_t )# duration in s
            speed.append(vf)
        else:
            speed.append(0)
    return speed

def parameters(array_data):

    res={}
    res["mean"]=st.mean(array_data)
    res["normal_deviation"]=math.sqrt(st.variance(array_data))
    return res

