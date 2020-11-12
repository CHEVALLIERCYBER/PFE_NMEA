def modele():

    dict2={}
    
    chemin="/home/guillaume/Téléchargements/temp" # put the path

    dict2["0nds"]={}
    dict2["10nds"]={}
    dict2["20nds"]={}
    dict2["30nds"]={}

    dict2["0nds"]["all"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_0nds.json")
    dict2["10nds"]["0"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_10nds_0.json")
    dict2["10nds"]["45"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_10nds_45.json")
    dict2["10nds"]["90"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_10nds_90.json")
    dict2["10nds"]["135"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_10nds_135.json")
    dict2["10nds"]["180"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_10nds_180.json")
    dict2["10nds"]["270"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_10nds_270.json")
    dict2["10nds"]["315"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_10nds_315.json")
    dict2["10nds"]["225"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_10nds_225.json")

    dict2["20nds"]["0"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_20nds_0.json")
    dict2["20nds"]["45"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_20nds_45.json")
    dict2["20nds"]["90"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_20nds_90.json")
    dict2["20nds"]["135"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_20nds_135.json")
    dict2["20nds"]["180"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_20nds_180.json")
    dict2["20nds"]["270"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_20nds_270.json")
    dict2["20nds"]["315"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_20nds_315.json")
    dict2["20nds"]["225"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_20nds_225.json")

    dict2["30nds"]["0"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_30nds_0.json")
    dict2["30nds"]["45"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_30nds_45.json")
    dict2["30nds"]["90"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_30nds_90.json")
    dict2["30nds"]["135"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_30nds_135.json")
    dict2["30nds"]["180"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_30nds_180.json")
    dict2["30nds"]["270"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_30nds_270.json")
    dict2["30nds"]["315"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_30nds_315.json")
    dict2["30nds"]["225"]=open(chemin+"/PFE_NMEA-main/dataset/Entrainement/rmc_30nds_225.json")

    return dict2

modele()
