import traitement as tr
import sklearn as sk

def prediction(test,modele):  #recoit en parametre une liste de listes de valeurs de phi,g,t et le modele calculé par la fonction entrainement

    phi_test=test[0]
    g_test=test[1]
    t_test=test[2]
    vitesse_test=test[3]
    cap_test=test[4]


    delta_cap_test=tr.delta(cap_test,t_test) # delta en minutes de cap
    delta_distance_test=tr.delta_distance(phi_test,g_test)

    resultat=[] # estimation de Z=(X-µ)/sigma
    leurrage=[] # True si leurrage: w>3

    for i in range(len(cap_test)-1): # on parcourt la liste des points

        cap=cap_test[i]/60 # en degres
        vitesse=vitesse_test[i]


        if (vitesse < 15 and vitesse>=5):   # la vitesse autour de  10 nds

            # on différencie selon le cap

            if (cap >= 22.5) and (cap < 67.5): # 45

                w=(abs(delta_cap_test[i]-modele["µ"]["10nds"]["45"]["cap"])/modele["sigma"]["10nds"]["45"]["cap"])
                if (w>3):
                    leurrage=True
                else:
                    leurrage=False
                resultat.append(w)

            elif (cap >= 67.5 and cap < 112.5): # 90

                w= (abs(delta_cap_test[i]-modele["µ"]["10nds"]["90"]["cap"])/modele["sigma"]["10nds"]["90"]["cap"])

                if (w>3):
                    leurrage=True
                else:
                    leurrage=False
                resultat.append(w)

            elif (cap >= 112.5 and cap < 157.5): # 135

                w= (abs(delta_cap_test[i]-modele["µ"]["10nds"]["135"]["cap"])/modele["sigma"]["10nds"]["135"]["cap"])

                if (w>3):
                    leurrage=True
                else:
                    leurrage=False
                resultat.append(w)

            elif (cap >= 157.5 and cap < 202.5): # 180

                w= (abs(delta_cap_test[i]-modele["µ"]["10nds"]["180"]["cap"])/modele["sigma"]["10nds"]["180"]["cap"])

                if (w>3):
                    leurrage=True
                else:
                    leurrage=False
                resultat.append(w)

            elif (cap >= 202.5 and cap < 247.5): # 225

                w= (abs(delta_cap_test[i]-modele["µ"]["10nds"]["225"]["cap"])/modele["sigma"]["10nds"]["225"]["cap"])


                if (w>3):
                    leurrage=True
                else:
                    leurrage=False
                resultat.append(w)

            elif (cap >= 247.5 and cap < 292.5): # 270

                w= (abs(delta_cap_test[i]-modele["µ"]["10nds"]["270"]["cap"])/modele["sigma"]["10nds"]["270"]["cap"])

                if (w>3):
                    leurrage=True
                else:
                    leurrage=False
                resultat.append(w)

            elif (cap >= 292.5 and cap < 337.5): # 315

                w= (abs(delta_cap_test[i]-modele["µ"]["10nds"]["315"]["cap"])/modele["sigma"]["10nds"]["315"]["cap"])


                if (w>3):
                    leurrage=True
                else:
                    leurrage=False
                resultat.append(w)

            else:

                w= (abs(delta_cap_test[i]-modele["µ"]["10nds"]["0"]["cap"])/modele["sigma"]["10nds"]["0"]["cap"])


                if (w>3):
                    leurrage=True
                else:
                    leurrage=False
                resultat.append(w)

            z = (abs(delta_distance_test[i] - modele["µ"]["10nds"]["0"]["cap"]) / modele["sigma"]["10nds"]["0"]["cap"])


        elif (vitesse < 25 and vitesse>=15):    # vitesse autour de  20 nds

            # on différencie selon le cap

            if (cap >= 22.5) and (cap < 67.5): # 45

                w= (abs(delta_cap_test[i]-modele["µ"]["20nds"]["45"]["cap"])/modele["sigma"]["20nds"]["45"]["cap"])


                if (w>3):
                    leurrage=True
                else:
                    leurrage=False
                resultat.append(w)

            elif (cap >= 67.5 and cap < 112.5): # 90

                w= (abs(delta_cap_test[i]-modele["µ"]["20nds"]["90"]["cap"])/modele["sigma"]["20nds"]["90"]["cap"])

                if (w>3):
                    leurrage=True
                else:
                    leurrage=False
                resultat.append(w)

            elif (cap >= 112.5 and cap < 157.5): # 135

                w= (abs(delta_cap_test[i]-modele["µ"]["20nds"]["135"]["cap"])/modele["sigma"]["20nds"]["135"]["cap"])

                if (w>3):
                    leurrage=True
                else:
                    leurrage=False
                resultat.append(w)

            elif (cap >= 157.5 and cap < 202.5): # 180

                w= (abs(delta_cap_test[i]-modele["µ"]["20nds"]["180"]["cap"])/modele["sigma"]["20nds"]["180"]["cap"])

                if (w>3):
                    leurrage=True
                else:
                    leurrage=False
                resultat.append(w)

            elif (cap >= 202.5 and cap < 247.5): # 225

                w= (abs(delta_cap_test[i]-modele["µ"]["20nds"]["225"]["cap"])/modele["sigma"]["20nds"]["225"]["cap"])

                if (w>3 or w>3):
                    leurrage=True
                else:
                    leurrage=False
                resultat.append(w)

            elif (cap >= 247.5 and cap < 292.5): # 270

                w= (abs(delta_cap_test[i]-modele["µ"]["20nds"]["270"]["cap"])/modele["sigma"]["20nds"]["270"]["cap"])

                if (w>3):
                    leurrage=True
                else:
                    leurrage=False
                resultat.append(w)

            elif (cap >= 292.5 and cap < 337.5): # 315

                w= (abs(delta_cap_test[i]-modele["µ"]["20nds"]["315"]["cap"])/modele["sigma"]["20nds"]["315"]["cap"])

                if (w>3):
                    leurrage=True
                else:
                    leurrage=False
                resultat.append(w)

            else:# 0

                w= (abs(delta_cap_test[i]-modele["µ"]["20nds"]["0"]["cap"])/modele["sigma"]["20nds"]["0"]["cap"])

                if (w>3):
                    leurrage=True
                else:
                    leurrage=False
                resultat.append(w)


        elif (vitesse < 5): # vitesse presque nulle ????


            w = (abs(delta_cap_test[i] - modele["µ"]["0nds"]["all"]["cap"]) / modele["sigma"]["0nds"]["all"]["cap"])

            if (w>3):
                leurrage=True
            else:
                leurrage=False
            resultat.append(w)

        else: # vitesse > 25

            if (cap >= 22.5 and cap < 67.5):

                w = (abs(delta_cap_test[i] - modele["µ"]["30nds"]["45"]["cap"]) / modele["sigma"]["30nds"]["45"]["cap"])

                if (w>3):
                    leurrage=True
                else:
                    leurrage=False
                resultat.append(w)

            elif (cap >= 67.5 and cap < 112.5):

                w = (abs(delta_cap_test[i] - modele["µ"]["30nds"]["90"]["cap"]) / modele["sigma"]["30nds"]["90"]["cap"])

                if (w>3):
                    leurrage=True
                else:
                    leurrage=False
                resultat.append(w)

            elif (cap >= 112.5 and cap < 157.5):

                w = (abs(delta_cap_test[i] - modele["µ"]["30nds"]["135"]["cap"]) / modele["sigma"]["30nds"]["135"]["cap"])

                if (w>3):
                    leurrage=True
                else:
                    leurrage=False
                resultat.append(w)

            elif (cap >= 157.5 and cap < 202.5):

                w = (abs(delta_cap_test[i] - modele["µ"]["30nds"]["180"]["cap"]) / modele["sigma"]["30nds"]["180"]["cap"])

                if (w>3):
                    leurrage=True
                else:
                    leurrage=False
                resultat.append(w)

            elif (cap >= 202.5 and cap < 247.5):

                w = (abs(delta_cap_test[i] - modele["µ"]["30nds"]["225"]["cap"]) / modele["sigma"]["30nds"]["225"]["cap"])


                if (w>3):
                    leurrage=True
                else:
                    leurrage=False
                resultat.append(w)

            elif (cap >= 247.5 and cap < 292.5):

                w = (abs(delta_cap_test[i] - modele["µ"]["30nds"]["270"]["cap"]) / modele["sigma"]["30nds"]["270"]["cap"])

                if (w>3):
                    leurrage=True
                else:
                    leurrage=False
                resultat.append(w)

            elif (cap >= 292.5 and cap < 337.5):

                w = (abs(delta_cap_test[i] - modele["µ"]["30nds"]["315"]["cap"]) / modele["sigma"]["30nds"]["315"]["cap"])

                if (w>3):
                    leurrage=True
                else:
                    leurrage=False
                resultat.append(w)

            else:

                w = (abs(delta_cap_test[i] - modele["µ"]["30nds"]["0"]["cap"]) / modele["sigma"]["30nds"]["0"]["cap"])

                if (w>3): # proba à 99%
                    leurrage=True
                else:
                    leurrage=False
                resultat.append(w)
    #print ("resultat : ",resultat)



    return [leurrage,resultat[-1]]

