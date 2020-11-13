# ------------------------------------------------------------------------
#
# @Author : EV2 CHEVALLIER
#
# @Date : 06.11.20
# @Location : École Navale / Chaire de Cyberdéfense des systèmes navals
# @Project : Projet de Fin d'Études
# @Subject : # Détection temps-réel d’anomalies cyber # sur un réseau NMEA par l’utilisation de # techniques d’apprentissage automatique.
#
# ------------------------------------------------------------------------
# @Title : Prediction of spoofing
# ------------------------------------------------------------------------
# @Description : # This programm get a list of points ( list of latitude, longitude, time ) to test and the model that is a dictionary with statistical parameters
# of the following features : variations of distance (dD) beetwen two points and  variations of  heading (dC) 
# It computes the features(dC,dD) upon the dataset to test and compte the reduced varibles w= (dC-µ)/sigma et z=(dD-µ)/sigma
# if w>3 or z>3 we consider there is a spoofing 
# ------------------------------------------------------------------------

import traitement as tr
import sklearn as sk


def prediction(test,model):  
    phi_test = test[0]
    g_test = test[1]
    t_test = test[2]
    speed_test = test[3]
    heading_test = test[4]

    delta_heading_test = tr.delta(heading_test, t_test)  # delta in minutes of heading
    delta_distance_test = tr.delta_distance(phi_test, g_test)  # delta of distances in yards

    resultat = []
    detection_spoofing = []  # True if spoofing: w>3 ou z>3

    for i in range(len(heading_test) - 1): 

        heading = heading_test[i] / 60  # in degrees
        speed = speed_test[i]

        if (speed < 15 and speed >= 5):  #  speed around  10 kts

            w = (abs(delta_heading_test[i] - model["µ"]["10kts"]["0"]["heading"]) / model["sigma"]["10kts"]["0"]["heading"])
            z = (abs(delta_distance_test[i] - model["µ"]["10kts"]["0"]["distance"]) / model["sigma"]["10kts"]["0"][
                "heading"])

        elif (speed < 25 and speed >= 15):  # speed around  20 kts

            w = (abs(delta_heading_test[i] - model["µ"]["20kts"]["0"]["heading"]) / model["sigma"]["20kts"]["0"]["heading"])
            z = (abs(delta_distance_test[i] - model["µ"]["20kts"]["0"]["distance"]) / model["sigma"]["20kts"]["0"][
                "distance"])

        elif (speed < 5):  # speed around 0 kts

            w = (abs(delta_heading_test[i] - model["µ"]["0kts"]["all"]["heading"]) / model["sigma"]["0kts"]["all"]["heading"])
            z = (abs(delta_distance_test[i] - model["µ"]["0kts"]["0"]["distance"]) / model["sigma"]["0kts"]["0"][
                "distance"])

        else:  # speed > 25

            w = (abs(delta_heading_test[i] - model["µ"]["0kts"]["all"]["heading"]) / model["sigma"]["0kts"]["all"]["heading"])
            z = (abs(delta_distance_test[i] - model["µ"]["30kts"]["0"]["distance"]) / model["sigma"]["30kts"]["0"][
                "distance"])

        if (w > 3 or z > 3):
            spoofing = True
        else:
            spoofing = False

        resultat.append(w)
        resultat.append(z)
        detection_spoofing.append(spoofing)

    return [spoofing, resultat]
