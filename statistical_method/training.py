#------------------------------------------------------------------------
#
# @Auteurs : EV2 CHAVELLIER 
#
# @Date : 06.11.20
# @Location : École Navale / Chaire de Cyberdéfense des systèmes navals
# @Cadre : Projet de Fin d'Études
# @Subject : # Real time detection of cyber anomalies upon a NMEA network by using machine learning methods
#
#------------------------------------------------------------------------
# @Title : Training
#------------------------------------------------------------------------
# @Description : # Ce programme récupère les données d'éntrainement sous forme d'un dictionnaire et calcule les parametres satistiques des features interessants : 
# variations de phi, variation de g, variation de cap et variation de distance.
# Le tout est sauvegardé dans un fichier binaire grace au module pickle de python.
#------------------------------------------------------------------------


import traitement as tr
import pickle as pk
import model as md

def training(dict2):


    model={}
    model["µ"]={}
    model["sigma"]={}

    for x in dict: # on parcourt le dictionnaire en fonction du champ de vitesse
        model["µ"][x]={}
        model["sigma"][x]={}

        for y in dict[x]: # on parcourt le dictionnaire en fonction du champ de cap

            model["µ"][x][y] = {}
            model["sigma"][x][y] = {}

            doc=tr.load(dict[x][y]) # on ouvre le fichier json correspondant

            phi_l=doc[0]
            g_l=doc[1]   # recupere une liste de phi,g,t
            t_l=doc[2]

            dphi_l=tr.delta(phi_l,t_l) # calcule les différentiels
            dg_l=tr.delta(g_l,t_l)
            dcap_l=tr.delta(tr.cap(phi_l,g_l),t_l)
            d_distance=tr.delta_distance(phi_l,g_l)

# on construit le modele avec les features que l'on veut : ici différence de cap et difference de distance mais aussi variation de phi et de g

            model["µ"][x][y]["phi"] = tr.parametres(dphi_l)["moyenne"]
            model["µ"][x][y]["g"] = tr.parametres(dg_l)["moyenne"]    # met à jour le modele

            model["sigma"][x][y]["phi"] = tr.parametres(dphi_l)["ecart-type"]
            model["sigma"][x][y]["g"] = tr.parametres(g_l)["ecart-type"]


            model["µ"][x][y]["cap"] = tr.parametres(dcap_l)["moyenne"]
            model["µ"][x][y]["distance"] = tr.parametres(d_distance)["moyenne"]

            model["sigma"][x][y]["cap"] = tr.parametres(dcap_l)["ecart-type"]
            model["sigma"][x][y]["distance"] = tr.parametres(d_distance)["ecart-type"]

    with open('model.sauv','wb' ) as model_sauv_file: # enregistre le modele dans un fichier
        pk.dump(model, model_sauv_file) # sauvegarde le modele

    return model

entrainement(md.model())
