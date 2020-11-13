# ------------------------------------------------------------------------
#
# @Author : EV2 CHEVALLIER 
#
# @Date : 06.11.20
# @Location : École Navale / Chaire de Cyberdéfense des systèmes navals
# @Project : Projet de Fin d'Études
# @Subject : Real time detection of cyber anomalies upon a NMEA network by using machine learning methods
# ------------------------------------------------------------------------
# @Title : Prediction
# ------------------------------------------------------------------------
# @Description : # This programm predict if a spoofing happens, using the following features : the difference of latitude and longitude 

# These test are real time
# ------------------------------------------------------------------------

import traitement as tr
import sklearn as sk


def prediction(test, model):  # test is a list of liste containing some values of latitude, longitude, and time 

    phi_test = test[0]
    g_test = test[1]
    t_test = test[2]
    speed_test = test[3]
    heading_test = test[4]
    delta_phi_test = tr.delta(phi_test, t_test)  # successive differences  in minutes of latitude 
    delta_g_test = tr.delta(g_test, t_test)  # ---------------------   in minutes of longitude

    resultat = []  # estimation of Z=(X-µ)/sigma
    resultat_spoofing = []  # True if spoofing : x>3 ou y>3

    for i in range(len(heading_test) - 1):  # for all the points

        heading = heading_test[i] / 60  # in degrees
        speed = speed_test[i]

        if (speed < 15 and speed >= 5):  # speed around 10 kts

            # difference of traitement according to the heading

            if (heading >= 22.5) and (heading < 67.5):  # 45

                x = (abs(delta_phi_test[i] - model["µ"]["10nds"]["45"]["phi"]) / model["sigma"]["10nds"]["45"]["phi"])
                y = (abs(delta_g_test[i] - model["µ"]["10nds"]["45"]["g"]) / model["sigma"]["10nds"]["45"]["g"])

            elif (heading >= 67.5 and heading < 112.5):  # 90

                x = (abs(delta_phi_test[i] - model["µ"]["10nds"]["90"]["phi"]) / model["sigma"]["10nds"]["90"]["phi"])
                y = (abs(delta_g_test[i] - model["µ"]["10nds"]["90"]["g"]) / model["sigma"]["10nds"]["90"]["g"])

            elif (heading >= 112.5 and heading < 157.5):  # 135

                x = (abs(delta_phi_test[i] - model["µ"]["10nds"]["135"]["phi"]) / model["sigma"]["10nds"]["135"][
                    "phi"])
                y = (abs(delta_g_test[i] - model["µ"]["10nds"]["135"]["g"]) / model["sigma"]["10nds"]["135"]["g"])

            elif (heading >= 157.5 and heading < 202.5):  # 180

                x = (abs(delta_phi_test[i] - model["µ"]["10nds"]["180"]["phi"]) / model["sigma"]["10nds"]["180"][
                    "phi"])
                y = (abs(delta_g_test[i] - model["µ"]["10nds"]["180"]["g"]) / model["sigma"]["10nds"]["180"]["g"])

            elif (heading >= 202.5 and heading < 247.5):  # 225

                x = (abs(delta_phi_test[i] - model["µ"]["10nds"]["225"]["phi"]) / model["sigma"]["10nds"]["225"][
                    "phi"])
                y = (abs(delta_g_test[i] - model["µ"]["10nds"]["225"]["g"]) / model["sigma"]["10nds"]["225"]["g"])

            elif (heading >= 247.5 and heading < 292.5):  # 270

                x = (abs(delta_phi_test[i] - model["µ"]["10nds"]["270"]["phi"]) / model["sigma"]["10nds"]["270"][
                    "phi"])
                y = (abs(delta_g_test[i] - model["µ"]["10nds"]["270"]["g"]) / model["sigma"]["10nds"]["270"]["g"])

            elif (heading >= 292.5 and heading < 337.5):  # 315

                x = (abs(delta_phi_test[i] - model["µ"]["10nds"]["315"]["phi"]) / model["sigma"]["10nds"]["315"][
                    "phi"])
                y = (abs(delta_g_test[i] - model["µ"]["10nds"]["315"]["g"]) / model["sigma"]["10nds"]["315"]["g"])

            else:

                x = (abs(delta_phi_test[i] - model["µ"]["10nds"]["0"]["phi"]) / model["sigma"]["10nds"]["0"]["phi"])
                y = (abs(delta_g_test[i] - model["µ"]["10nds"]["0"]["g"]) / model["sigma"]["10nds"]["0"]["g"])

        elif (speed < 25 and speed >= 15):  # speed around 10 kts

            if (heading >= 22.5) and (heading < 67.5):  # 45

                x = (abs(delta_phi_test[i] - model["µ"]["20nds"]["45"]["phi"]) / model["sigma"]["20nds"]["45"]["phi"])
                y = (abs(delta_g_test[i] - model["µ"]["20nds"]["45"]["g"]) / model["sigma"]["20nds"]["45"]["g"])

            elif (heading >= 67.5 and heading < 112.5):  # 90

                x = (abs(delta_phi_test[i] - model["µ"]["20nds"]["90"]["phi"]) / model["sigma"]["20nds"]["90"]["phi"])
                y = (abs(delta_g_test[i] - model["µ"]["20nds"]["90"]["g"]) / model["sigma"]["20nds"]["90"]["g"])

            elif (heading >= 112.5 and heading < 157.5):  # 135

                x = (abs(delta_phi_test[i] - model["µ"]["20nds"]["135"]["phi"]) / model["sigma"]["20nds"]["135"][
                    "phi"])
                y = (abs(delta_g_test[i] - model["µ"]["20nds"]["135"]["g"]) / model["sigma"]["20nds"]["135"]["g"])

            elif (heading >= 157.5 and heading < 202.5):  # 180

                x = (abs(delta_phi_test[i] - model["µ"]["20nds"]["180"]["phi"]) / model["sigma"]["20nds"]["180"][
                    "phi"])
                y = (abs(delta_g_test[i] - model["µ"]["20nds"]["180"]["g"]) / model["sigma"]["20nds"]["180"]["g"])

            elif (heading >= 202.5 and heading < 247.5):  # 225

                x = (abs(delta_phi_test[i] - model["µ"]["20nds"]["225"]["phi"]) / model["sigma"]["20nds"]["225"][
                    "phi"])
                y = (abs(delta_g_test[i] - model["µ"]["20nds"]["225"]["g"]) / model["sigma"]["20nds"]["225"]["g"])

            elif (heading >= 247.5 and heading < 292.5):  # 270

                x = (abs(delta_phi_test[i] - model["µ"]["20nds"]["270"]["phi"]) / model["sigma"]["20nds"]["270"][
                    "phi"])
                y = (abs(delta_g_test[i] - model["µ"]["20nds"]["270"]["g"]) / model["sigma"]["20nds"]["270"]["g"])

            elif (heading >= 292.5 and heading < 337.5):  # 315

                x = (abs(delta_phi_test[i] - model["µ"]["20nds"]["315"]["phi"]) / model["sigma"]["20nds"]["315"][
                    "phi"])
                y = (abs(delta_g_test[i] - model["µ"]["20nds"]["315"]["g"]) / model["sigma"]["20nds"]["315"]["g"])

            else:

                x = (abs(delta_phi_test[i] - model["µ"]["20nds"]["0"]["phi"]) / model["sigma"]["20nds"]["0"]["phi"])
                y = (abs(delta_g_test[i] - model["µ"]["20nds"]["0"]["g"]) / model["sigma"]["20nds"]["0"]["g"])

        elif (speed < 5):  # speed around 0 kts

            x = (abs(delta_phi_test[i] - model["µ"]["0nds"]["all"]["phi"]) / model["sigma"]["0nds"]["all"]["phi"])
            y = (abs(delta_g_test[i] - model["µ"]["0nds"]["all"]["g"]) / model["sigma"]["0nds"]["all"]["g"])

        else:  # speed > 25 #speed around 10 kts

            if (heading >= 22.5) and (heading < 67.5):  # 45

                x = (abs(delta_phi_test[i] - model["µ"]["30nds"]["45"]["phi"]) / model["sigma"]["30nds"]["45"]["phi"])
                y = (abs(delta_g_test[i] - model["µ"]["30nds"]["45"]["g"]) / model["sigma"]["30nds"]["45"]["g"])

            elif (heading >= 67.5 and heading < 112.5):  # 90

                x = (abs(delta_phi_test[i] - model["µ"]["30nds"]["90"]["phi"]) / model["sigma"]["30nds"]["90"]["phi"])
                y = (abs(delta_g_test[i] - model["µ"]["30nds"]["90"]["g"]) / model["sigma"]["30nds"]["90"]["g"])

            elif (heading >= 112.5 and heading < 157.5):  # 135

                x = (abs(delta_phi_test[i] - model["µ"]["30nds"]["135"]["phi"]) / model["sigma"]["30nds"]["135"][
                    "phi"])
                y = (abs(delta_g_test[i] - model["µ"]["30nds"]["135"]["g"]) / model["sigma"]["30nds"]["135"]["g"])

            elif (heading >= 157.5 and heading < 202.5):  # 180

                x = (abs(delta_phi_test[i] - model["µ"]["30nds"]["180"]["phi"]) / model["sigma"]["30nds"]["180"][
                    "phi"])
                y = (abs(delta_g_test[i] - model["µ"]["30nds"]["180"]["g"]) / model["sigma"]["30nds"]["180"]["g"])

            elif (heading >= 202.5 and heading < 247.5):  # 225

                x = (abs(delta_phi_test[i] - model["µ"]["30nds"]["225"]["phi"]) / model["sigma"]["30nds"]["225"][
                    "phi"])
                y = (abs(delta_g_test[i] - model["µ"]["30nds"]["225"]["g"]) / model["sigma"]["30nds"]["225"]["g"])

            elif (heading >= 247.5 and heading < 292.5):  # 270

                x = (abs(delta_phi_test[i] - model["µ"]["30nds"]["270"]["phi"]) / model["sigma"]["30nds"]["270"][
                    "phi"])
                y = (abs(delta_g_test[i] - model["µ"]["30nds"]["270"]["g"]) / model["sigma"]["30nds"]["270"]["g"])

            elif (heading >= 292.5 and heading < 337.5):  # 315

                x = (abs(delta_phi_test[i] - model["µ"]["30nds"]["315"]["phi"]) / model["sigma"]["30nds"]["315"][
                    "phi"])
                y = (abs(delta_g_test[i] - model["µ"]["30nds"]["315"]["g"]) / model["sigma"]["30nds"]["315"]["g"])

            else:

                x = (abs(delta_phi_test[i] - model["µ"]["30nds"]["0"]["phi"]) / model["sigma"]["30nds"]["0"]["phi"])
                y = (abs(delta_g_test[i] - model["µ"]["30nds"]["0"]["g"]) / model["sigma"]["30nds"]["0"]["g"])

        if (x > 3 or y > 3):
            spoofing = True
        else:
            spoofing = False

        resultat.append([x, y])
        resultat_spoofing.append(spoofing)

    return [resultat_spoofing, resultat]
