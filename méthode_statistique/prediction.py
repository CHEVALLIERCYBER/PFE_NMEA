import traitement as tr
import sklearn as sk

def prediction(test,modele):  #recoit en parametre une liste de listes de valeurs de phi,g,t et le modele calculé par la fonction entrainement

	phi_test=test[0]
	g_test=test[1]
	t_test=test[2]
	vitesse_test=test[3]
	cap_test=test[4]
	delta_phi_test=tr.delta(phi_test,t_test) # ecarts successifs en minutes de phi 
	delta_g_test=tr.delta(g_test,t_test)     # ----------------- en minutes de g

	resultat=[] # estimation de Z=(X-µ)/sigma
	resultat_leurrage=[] # True si leurrage: x>3 ou y>3

	for i in range(len(cap_test)-1): # on parcourt la liste des points

		cap=cap_test[i]/60 # en degres
		vitesse=vitesse_test[i]


		if (vitesse < 15 and vitesse>=5):   # la vitesse autour de  10 nds

            # on différencie selon le cap

			if (cap >= 22.5) and (cap < 67.5): # 45

				x=(abs(delta_phi_test[i]-modele["µ"]["10nds"]["45"]["phi"])/modele["sigma"]["10nds"]["45"]["phi"])
				y=(abs(delta_g_test[i]-modele["µ"]["10nds"]["45"]["g"])/modele["sigma"]["10nds"]["45"]["g"])
                
			elif (cap >= 67.5 and cap < 112.5): # 90

				x=(abs(delta_phi_test[i]-modele["µ"]["10nds"]["90"]["phi"])/modele["sigma"]["10nds"]["90"]["phi"])
				y=(abs(delta_g_test[i]-modele["µ"]["10nds"]["90"]["g"])/modele["sigma"]["10nds"]["90"]["g"])
              
			elif (cap >= 112.5 and cap < 157.5): # 135

				x=(abs(delta_phi_test[i]-modele["µ"]["10nds"]["135"]["phi"])/modele["sigma"]["10nds"]["135"]["phi"])
				y=(abs(delta_g_test[i]-modele["µ"]["10nds"]["135"]["g"])/modele["sigma"]["10nds"]["135"]["g"])

			elif (cap >= 157.5 and cap < 202.5): # 180

				x=(abs(delta_phi_test[i]-modele["µ"]["10nds"]["180"]["phi"])/modele["sigma"]["10nds"]["180"]["phi"])
				y=(abs(delta_g_test[i]-modele["µ"]["10nds"]["180"]["g"])/modele["sigma"]["10nds"]["180"]["g"])

			elif (cap >= 202.5 and cap < 247.5): # 225

				x=(abs(delta_phi_test[i]-modele["µ"]["10nds"]["225"]["phi"])/modele["sigma"]["10nds"]["225"]["phi"])
				y=(abs(delta_g_test[i]-modele["µ"]["10nds"]["225"]["g"])/modele["sigma"]["10nds"]["225"]["g"])       

			elif (cap >= 247.5 and cap < 292.5): # 270

				x=(abs(delta_phi_test[i]-modele["µ"]["10nds"]["270"]["phi"])/modele["sigma"]["10nds"]["270"]["phi"])
				y=(abs(delta_g_test[i]-modele["µ"]["10nds"]["270"]["g"])/modele["sigma"]["10nds"]["270"]["g"])
               
			elif (cap >= 292.5 and cap < 337.5): # 315

				x=(abs(delta_phi_test[i]-modele["µ"]["10nds"]["315"]["phi"])/modele["sigma"]["10nds"]["315"]["phi"])
				y=(abs(delta_g_test[i]-modele["µ"]["10nds"]["315"]["g"])/modele["sigma"]["10nds"]["315"]["g"])

			else:

				x=(abs(delta_phi_test[i]-modele["µ"]["10nds"]["0"]["phi"])/modele["sigma"]["10nds"]["0"]["phi"])
				y=(abs(delta_g_test[i]-modele["µ"]["10nds"]["0"]["g"])/modele["sigma"]["10nds"]["0"]["g"])

		elif (vitesse < 25 and vitesse>=15):    # vitesse autour de  20 nds

            # on différencie selon le cap
            
			if (cap >= 22.5) and (cap < 67.5): # 45

				x=(abs(delta_phi_test[i]-modele["µ"]["20nds"]["45"]["phi"])/modele["sigma"]["20nds"]["45"]["phi"])
				y=(abs(delta_g_test[i]-modele["µ"]["20nds"]["45"]["g"])/modele["sigma"]["20nds"]["45"]["g"])
                
			elif (cap >= 67.5 and cap < 112.5): # 90

				x=(abs(delta_phi_test[i]-modele["µ"]["20nds"]["90"]["phi"])/modele["sigma"]["20nds"]["90"]["phi"])
				y=(abs(delta_g_test[i]-modele["µ"]["20nds"]["90"]["g"])/modele["sigma"]["20nds"]["90"]["g"])
              
			elif (cap >= 112.5 and cap < 157.5): # 135

				x=(abs(delta_phi_test[i]-modele["µ"]["20nds"]["135"]["phi"])/modele["sigma"]["20nds"]["135"]["phi"])
				y=(abs(delta_g_test[i]-modele["µ"]["20nds"]["135"]["g"])/modele["sigma"]["20nds"]["135"]["g"])

			elif (cap >= 157.5 and cap < 202.5): # 180

				x=(abs(delta_phi_test[i]-modele["µ"]["20nds"]["180"]["phi"])/modele["sigma"]["20nds"]["180"]["phi"])
				y=(abs(delta_g_test[i]-modele["µ"]["20nds"]["180"]["g"])/modele["sigma"]["20nds"]["180"]["g"])

			elif (cap >= 202.5 and cap < 247.5): # 225

				x=(abs(delta_phi_test[i]-modele["µ"]["20nds"]["225"]["phi"])/modele["sigma"]["20nds"]["225"]["phi"])
				y=(abs(delta_g_test[i]-modele["µ"]["20nds"]["225"]["g"])/modele["sigma"]["20nds"]["225"]["g"])       

			elif (cap >= 247.5 and cap < 292.5): # 270

				x=(abs(delta_phi_test[i]-modele["µ"]["20nds"]["270"]["phi"])/modele["sigma"]["20nds"]["270"]["phi"])
				y=(abs(delta_g_test[i]-modele["µ"]["20nds"]["270"]["g"])/modele["sigma"]["20nds"]["270"]["g"])
               
			elif (cap >= 292.5 and cap < 337.5): # 315

				x=(abs(delta_phi_test[i]-modele["µ"]["20nds"]["315"]["phi"])/modele["sigma"]["20nds"]["315"]["phi"])
				y=(abs(delta_g_test[i]-modele["µ"]["20nds"]["315"]["g"])/modele["sigma"]["20nds"]["315"]["g"])

			else:

				x=(abs(delta_phi_test[i]-modele["µ"]["20nds"]["0"]["phi"])/modele["sigma"]["20nds"]["0"]["phi"])
				y=(abs(delta_g_test[i]-modele["µ"]["20nds"]["0"]["g"])/modele["sigma"]["20nds"]["0"]["g"])

		elif (vitesse < 5): # vitesse presque nulle ????

			x=(abs(delta_phi_test[i]-modele["µ"]["0nds"]["all"]["phi"])/modele["sigma"]["0nds"]["all"]["phi"])
			y=(abs(delta_g_test[i]-modele["µ"]["0nds"]["all"]["g"])/modele["sigma"]["0nds"]["all"]["g"])
           
		else: # vitesse > 25

			if (cap >= 22.5) and (cap < 67.5): # 45

				x=(abs(delta_phi_test[i]-modele["µ"]["30nds"]["45"]["phi"])/modele["sigma"]["30nds"]["45"]["phi"])
				y=(abs(delta_g_test[i]-modele["µ"]["30nds"]["45"]["g"])/modele["sigma"]["30nds"]["45"]["g"])
                
			elif (cap >= 67.5 and cap < 112.5): # 90

				x=(abs(delta_phi_test[i]-modele["µ"]["30nds"]["90"]["phi"])/modele["sigma"]["30nds"]["90"]["phi"])
				y=(abs(delta_g_test[i]-modele["µ"]["30nds"]["90"]["g"])/modele["sigma"]["30nds"]["90"]["g"])
              
			elif (cap >= 112.5 and cap < 157.5): # 135

				x=(abs(delta_phi_test[i]-modele["µ"]["30nds"]["135"]["phi"])/modele["sigma"]["30nds"]["135"]["phi"])
				y=(abs(delta_g_test[i]-modele["µ"]["30nds"]["135"]["g"])/modele["sigma"]["30nds"]["135"]["g"])

			elif (cap >= 157.5 and cap < 202.5): # 180

				x=(abs(delta_phi_test[i]-modele["µ"]["30nds"]["180"]["phi"])/modele["sigma"]["30nds"]["180"]["phi"])
				y=(abs(delta_g_test[i]-modele["µ"]["30nds"]["180"]["g"])/modele["sigma"]["30nds"]["180"]["g"])

			elif (cap >= 202.5 and cap < 247.5): # 225

				x=(abs(delta_phi_test[i]-modele["µ"]["30nds"]["225"]["phi"])/modele["sigma"]["30nds"]["225"]["phi"])
				y=(abs(delta_g_test[i]-modele["µ"]["30nds"]["225"]["g"])/modele["sigma"]["30nds"]["225"]["g"])       

			elif (cap >= 247.5 and cap < 292.5): # 270

				x=(abs(delta_phi_test[i]-modele["µ"]["30nds"]["270"]["phi"])/modele["sigma"]["30nds"]["270"]["phi"])
				y=(abs(delta_g_test[i]-modele["µ"]["30nds"]["270"]["g"])/modele["sigma"]["30nds"]["270"]["g"])
               
			elif (cap >= 292.5 and cap < 337.5): # 315

				x=(abs(delta_phi_test[i]-modele["µ"]["30nds"]["315"]["phi"])/modele["sigma"]["30nds"]["315"]["phi"])
				y=(abs(delta_g_test[i]-modele["µ"]["30nds"]["315"]["g"])/modele["sigma"]["30nds"]["315"]["g"])

			else:

				x=(abs(delta_phi_test[i]-modele["µ"]["30nds"]["0"]["phi"])/modele["sigma"]["30nds"]["0"]["phi"])
				y=(abs(delta_g_test[i]-modele["µ"]["30nds"]["0"]["g"])/modele["sigma"]["30nds"]["0"]["g"])
    
		if (x>3 or y>3):
			leurrage=True
		else:
			leurrage=False
				
		resultat.append([x,y])
		resultat_leurrage.append(leurrage)	


	return [resultat_leurrage,resultat]

