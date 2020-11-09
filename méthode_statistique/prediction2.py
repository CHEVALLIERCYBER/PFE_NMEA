#------------------------------------------------------------------------

#

# @Auteurs : EV2 CHEVALLIER

#

# @Date : 06.11.20

# @Lieu : École Navale / Chaire de Cyberdéfense des systèmes navals

# @Cadre : Projet de Fin d'Études

# @Sujet : # Détection temps-réel d’anomalies cyber # sur un réseau NMEA par l’utilisation de # techniques d’apprentissage automatique.

#

#------------------------------------------------------------------------

# @Titre : Prediction de leurrage

#------------------------------------------------------------------------

# @Description : # Ce programme recoit une liste de données à tester ( sous la forme de listes de latitudes, longitudes et temps ) et le modele qui est un dictionnaire contenant
# les paramètres statistiques des features suivants : variations de distance (dD) entre deux points et variations de cap (dC) entre deux points, et ce, en focntions de la vitesse du
# porteur.
# Il calcule ensuite les features(dC,dD) sur les données du jeu de test et calcule les variables réduite w= (dC-µ)/sigma et z=(dD-µ)/sigma
# Si w>3 ou z>3 on considere qu'il y a leurrage.


#------------------------------------------------------------------------

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

	resultat=[] 
	leurrage=[] # True si leurrage: w>3 ou z>3

	for i in range(len(cap_test)-1): # on parcourt la liste des points

		cap=cap_test[i]/60 # en degres
		vitesse=vitesse_test[i]

		if (vitesse < 15 and vitesse>=5): # la vitesse autour de  10 nds
		
			w=(abs(delta_cap_test[i]-modele["µ"]["10nds"]["0"]["cap"])/modele["sigma"]["10nds"]["0"]["cap"])
			z = (abs(delta_distance_test[i] - modele["µ"]["10nds"]["0"]["cap"]) / modele["sigma"]["10nds"]["0"]["cap"])
            
		elif (vitesse < 25 and vitesse>=15):    # vitesse autour de  20 nds

			w=(abs(delta_cap_test[i]-modele["µ"]["20nds"]["0"]["cap"])/modele["sigma"]["20nds"]["0"]["cap"])
			z = (abs(delta_distance_test[i] - modele["µ"]["20nds"]["0"]["vitesse"]) / modele["sigma"]["20nds"]["0"]["vitesse"])

		elif (vitesse < 5): # vitesse presque nulle 

			w = (abs(delta_cap_test[i] - modele["µ"]["0nds"]["all"]["cap"]) / modele["sigma"]["0nds"]["all"]["cap"])
			z = (abs(delta_distance_test[i] - modele["µ"]["0nds"]["0"]["vitesse"]) / modele["sigma"]["0nds"]["0"]["vitesse"])

		else: # vitesse > 25

			w = (abs(delta_cap_test[i] - modele["µ"]["0nds"]["all"]["cap"]) / modele["sigma"]["0nds"]["all"]["cap"])
			z = (abs(delta_distance_test[i] - modele["µ"]["30nds"]["0"]["cap"]) / modele["sigma"]["30nds"]["0"]["cap"])

		if (w>3 or z> 3):
			leurrage=True
		else:
			leurrage=False
                
		resultat.append(w)
		resultat.append(z)
		leurrage.append(leurrage)

            
    #print ("resultat : ",resultat)

	return [leurrage,resultat]
