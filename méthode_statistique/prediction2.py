

import traitement as tr
import sklearn as sk

def prediction(test,modele):  #recoit en parametre une liste de listes de valeurs de phi,g,t et le modele calculé par la fonction entrainement

    phi_test=test[0]
    g_test=test[1]
    t_test=test[2]
    vitesse_test=test[3]
    cap_test=test[4]

    delta_cap_test=tr.delta(cap_test,t_test) # delta en minutes de cap
    delta_distance_test=tr.delta_distance(phi_test,g_test) # delta de distances en yards

    resultat=[] # estimation de Z=(X-µ)/sigma
    leurrage=[] # True si leurrage: w>3

    for i in range(len(cap_test)-1): # on parcourt la liste des points

        cap=cap_test[i]/60 # en degres
        vitesse=vitesse_test[i]


        if (vitesse < 15 and vitesse>=5):   # la vitesse autour de  10 nds

			w=(abs(delta_cap_test[i]-modele["µ"]["10nds"]["0"]["cap"])/modele["sigma"]["10nds"]["0"]["cap"])
			z = (abs(delta_distance_test[i] - modele["µ"]["10nds"]["0"]["cap"]) / modele["sigma"]["10nds"]["0"]["cap"])
			
            if (w>3):
                leurrage=True
            else:
                leurrage=False
                
            resultat.append(w)
            resultat.append(z)


        elif (vitesse < 25 and vitesse>=15):    # vitesse autour de  20 nds
 
			w=(abs(delta_cap_test[i]-modele["µ"]["20nds"]["0"]["cap"])/modele["sigma"]["20nds"]["0"]["cap"])
			z = (abs(delta_distance_test[i] - modele["µ"]["20nds"]["0"]["vitesse"]) / modele["sigma"]["20nds"]["0"]["vitesse"])
			
            if (w>3 or z> 3):
                leurrage=True
            else:
                leurrage=False
            resultat.append(w)
            resultat.append(z)

        elif (vitesse < 5): # vitesse presque nulle ????


            w = (abs(delta_cap_test[i] - modele["µ"]["0nds"]["all"]["cap"]) / modele["sigma"]["0nds"]["all"]["cap"])
			z = (abs(delta_distance_test[i] - modele["µ"]["0nds"]["0"]["vitesse"]) / modele["sigma"]["0nds"]["0"]["vitesse"])

			if (w>3 or z> 3):
                leurrage=True
            else:
                leurrage=False
                
            resultat.append(w)
            resultat.append(z)
            
            z = (abs(delta_distance_test[i] - modele["µ"]["10nds"]["0"]["cap"]) / modele["sigma"]["10nds"]["0"]["cap"])
           

        else: # vitesse > 25

			w = (abs(delta_cap_test[i] - modele["µ"]["0nds"]["all"]["cap"]) / modele["sigma"]["0nds"]["all"]["cap"])
			z = (abs(delta_distance_test[i] - modele["µ"]["30nds"]["0"]["cap"]) / modele["sigma"]["30nds"]["0"]["cap"])

            if (w>3 or z>3):
                leurrage=True
            else:
                leurrage=False
            resultat.append(w)
            resultat.append(z)

            
    #print ("resultat : ",resultat)



    return [leurrage,resultat[-1]]
