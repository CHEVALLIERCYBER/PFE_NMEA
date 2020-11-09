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

# @Description : # Ce programme construit un dictionnaire avec l'ensemble des fichiers d'entrainement.


#------------------------------------------------------------------------

def modele():

    dict2={}

    dict2["0nds"]={}
    dict2["10nds"]={}
    dict2["20nds"]={}
    dict2["30nds"]={}

    dict2["0nds"]["all"]=open("/home/guillaume/PFE/DATA/RMC/rmc_0nds.json")

    dict2["10nds"]["0"]=open("/home/guillaume/PFE/DATA/RMC/rmc_10nds_0.json")
    dict2["10nds"]["45"]=open("/home/guillaume/PFE/DATA/RMC/rmc_10nds_45.json")
    dict2["10nds"]["90"]=open("/home/guillaume/PFE/DATA/RMC/rmc_10nds_90.json")
    dict2["10nds"]["135"]=open("/home/guillaume/PFE/DATA/RMC/rmc_10nds_135.json")
    dict2["10nds"]["180"]=open("/home/guillaume/PFE/DATA/RMC/rmc_10nds_180.json")
    dict2["10nds"]["270"]=open("/home/guillaume/PFE/DATA/RMC/rmc_10nds_270.json")
    dict2["10nds"]["315"]=open("/home/guillaume/PFE/DATA/RMC/rmc_10nds_315.json")
    dict2["10nds"]["225"]=open("/home/guillaume/PFE/DATA/RMC/rmc_10nds_225.json")

    dict2["20nds"]["0"]=open("/home/guillaume/PFE/DATA/RMC/rmc_20nds_0.json")
    dict2["20nds"]["45"]=open("/home/guillaume/PFE/DATA/RMC/rmc_20nds_45.json")
    dict2["20nds"]["90"]=open("/home/guillaume/PFE/DATA/RMC/rmc_20nds_90.json")
    dict2["20nds"]["135"]=open("/home/guillaume/PFE/DATA/RMC/rmc_20nds_135.json")
    dict2["20nds"]["180"]=open("/home/guillaume/PFE/DATA/RMC/rmc_20nds_180.json")
    dict2["20nds"]["270"]=open("/home/guillaume/PFE/DATA/RMC/rmc_20nds_270.json")
    dict2["20nds"]["315"]=open("/home/guillaume/PFE/DATA/RMC/rmc_20nds_315.json")
    dict2["20nds"]["225"]=open("/home/guillaume/PFE/DATA/RMC/rmc_20nds_225.json")

    dict2["30nds"]["0"]=open("/home/guillaume/PFE/DATA/RMC/rmc_30nds_0.json")
    dict2["30nds"]["45"]=open("/home/guillaume/PFE/DATA/RMC/rmc_30nds_45.json")
    dict2["30nds"]["90"]=open("/home/guillaume/PFE/DATA/RMC/rmc_30nds_90.json")
    dict2["30nds"]["135"]=open("/home/guillaume/PFE/DATA/RMC/rmc_30nds_135.json")
    dict2["30nds"]["180"]=open("/home/guillaume/PFE/DATA/RMC/rmc_30nds_180.json")
    dict2["30nds"]["270"]=open("/home/guillaume/PFE/DATA/RMC/rmc_30nds_270.json")
    dict2["30nds"]["315"]=open("/home/guillaume/PFE/DATA/RMC/rmc_30nds_315.json")
    dict2["30nds"]["225"]=open("/home/guillaume/PFE/DATA/RMC/rmc_30nds_225.json")

    return dict2

modele()
