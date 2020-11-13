# ------------------------------------------------------------------------
#
# @Author : EV2 CHEVALLIER 
#
# @Date : 06.11.20
# @Location : École Navale / Chaire de Cyberdéfense des systèmes navals
# @Project : Projet de Fin d'Études
# @Subject : Real time detection of cyber anomalies upon a NMEA network by using machine learning methods
# ------------------------------------------------------------------------
# @Title : Model
# ------------------------------------------------------------------------
# @Description : # This programm loads the file of the training dataset in a python dictionary
# ------------------------------------------------------------------------
def model():
    dict = {}

    path = tr.set_path() # put the path of the files

    dict["0kts"] = {}
    dict["10kts"] = {}
    dict["20kts"] = {}
    dict["30kts"] = {}

    dict["0kts"]["all"] = open(chemin + "/PFE_NMEA-main/dataset/Entrainement/rmc_0nds.json")
    dict["10kts"]["0"] = open(chemin + "/PFE_NMEA-main/dataset/Entrainement/rmc_10nds_0.json")
    dict["10kts"]["45"] = open(chemin + "/PFE_NMEA-main/dataset/Entrainement/rmc_10nds_45.json")
    dict["10kts"]["90"] = open(chemin + "/PFE_NMEA-main/dataset/Entrainement/rmc_10nds_90.json")
    dict["10kts"]["135"] = open(chemin + "/PFE_NMEA-main/dataset/Entrainement/rmc_10nds_135.json")
    dict["10kts"]["180"] = open(chemin + "/PFE_NMEA-main/dataset/Entrainement/rmc_10nds_180.json")
    dict["10kts"]["270"] = open(chemin + "/PFE_NMEA-main/dataset/Entrainement/rmc_10nds_270.json")
    dict["10kts"]["315"] = open(chemin + "/PFE_NMEA-main/dataset/Entrainement/rmc_10nds_315.json")
    dict["10kts"]["225"] = open(chemin + "/PFE_NMEA-main/dataset/Entrainement/rmc_10nds_225.json")

    dict["20kts"]["0"] = open(chemin + "/PFE_NMEA-main/dataset/Entrainement/rmc_20nds_0.json")
    dict["20kts"]["45"] = open(chemin + "/PFE_NMEA-main/dataset/Entrainement/rmc_20nds_45.json")
    dict["20kts"]["90"] = open(chemin + "/PFE_NMEA-main/dataset/Entrainement/rmc_20nds_90.json")
    dict["20kts"]["135"] = open(chemin + "/PFE_NMEA-main/dataset/Entrainement/rmc_20nds_135.json")
    dict["20kts"]["180"] = open(chemin + "/PFE_NMEA-main/dataset/Entrainement/rmc_20nds_180.json")
    dict["20kts"]["270"] = open(chemin + "/PFE_NMEA-main/dataset/Entrainement/rmc_20nds_270.json")
    dict["20kts"]["315"] = open(chemin + "/PFE_NMEA-main/dataset/Entrainement/rmc_20nds_315.json")
    dict["20kts"]["225"] = open(chemin + "/PFE_NMEA-main/dataset/Entrainement/rmc_20nds_225.json")

    dict["30kts"]["0"] = open(chemin + "/PFE_NMEA-main/dataset/Entrainement/rmc_30nds_0.json")
    dict["30kts"]["45"] = open(chemin + "/PFE_NMEA-main/dataset/Entrainement/rmc_30nds_45.json")
    dict["30kts"]["90"] = open(chemin + "/PFE_NMEA-main/dataset/Entrainement/rmc_30nds_90.json")
    dict["30kts"]["135"] = open(chemin + "/PFE_NMEA-main/dataset/Entrainement/rmc_30nds_135.json")
    dict["30kts"]["180"] = open(chemin + "/PFE_NMEA-main/dataset/Entrainement/rmc_30nds_180.json")
    dict["30kts"]["270"] = open(chemin + "/PFE_NMEA-main/dataset/Entrainement/rmc_30nds_270.json")
    dict["30kts"]["315"] = open(chemin + "/PFE_NMEA-main/dataset/Entrainement/rmc_30nds_315.json")
    dict["30kts"]["225"] = open(chemin + "/PFE_NMEA-main/dataset/Entrainement/rmc_30nds_225.json")

    return dict
