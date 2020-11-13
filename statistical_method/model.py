#------------------------------------------------------------------------
#
# @Author : EV2 CHEVALLIER 
#
# @Date : 06.11.20
# @Location : École Navale / Chaire de Cyberdéfense des systèmes navals
# @Project : Projet de Fin d'Études
# @Subject : Real time detection of cyber anomalies upon a NMEA network by using machine learning methods
#------------------------------------------------------------------------
# @Title : Model
#------------------------------------------------------------------------
# @Description : # This programm loads the file of the training dataset in a python dictionary
#------------------------------------------------------------------------
def model():

    dict={}
    
    chemin="/home/guillaume/Téléchargements/temp" # put the path

    dict["0nds"]={}
    dict["10nds"]={}
    dict["20nds"]={}
    dict["30nds"]={}

    dict["0nds"]["all"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_0nds.json")
    dict["10nds"]["0"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_10nds_0.json")
    dict["10nds"]["45"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_10nds_45.json")
    dict["10nds"]["90"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_10nds_90.json")
    dict["10nds"]["135"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_10nds_135.json")
    dict["10nds"]["180"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_10nds_180.json")
    dict["10nds"]["270"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_10nds_270.json")
    dict["10nds"]["315"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_10nds_315.json")
    dict["10nds"]["225"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_10nds_225.json")

    dict["20nds"]["0"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_20nds_0.json")
    dict["20nds"]["45"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_20nds_45.json")
    dict["20nds"]["90"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_20nds_90.json")
    dict["20nds"]["135"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_20nds_135.json")
    dict["20nds"]["180"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_20nds_180.json")
    dict["20nds"]["270"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_20nds_270.json")
    dict["20nds"]["315"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_20nds_315.json")
    dict["20nds"]["225"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_20nds_225.json")

    dict["30nds"]["0"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_30nds_0.json")
    dict["30nds"]["45"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_30nds_45.json")
    dict["30nds"]["90"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_30nds_90.json")
    dict["30nds"]["135"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_30nds_135.json")
    dict["30nds"]["180"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_30nds_180.json")
    dict["30nds"]["270"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_30nds_270.json")
    dict["30nds"]["315"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_30nds_315.json")
    dict["30nds"]["225"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_30nds_225.json")

    return dict

