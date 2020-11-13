#------------------------------------------------------------------------
#
# @Author : EV2 CHEVALLIER 
#
# @Date : 16.09.20
# @Location : École Navale / Chaire de Cyberdéfense des systèmes navals
# @Project : Projet de Fin d'Études
# @Subject : # Real time detection of cyber anomalies upon a NMEA network by using machine learning methods
#
#------------------------------------------------------------------------
# @Title : Training
#------------------------------------------------------------------------
# @Description : # This programm get the training dataset, extract the interesting features ( mean and standard deviation of variations of latitude, 
# longitude, heading and distance )
# and put it in a python dictionnary and save it in a binary file with the pickle module.

#------------------------------------------------------------------------


import traitement as tr
import pickle as pk
import model as md

def training(dict):


    model={}
    model["µ"]={}
    model["sigma"]={}

    for x in dict: # loop with speed
        model["µ"][x]={}
        model["sigma"][x]={}

        for y in dict[x]: # loop with heading

            model["µ"][x][y] = {}
            model["sigma"][x][y] = {}

            doc=tr.load(dict[x][y]) # open the json file

            phi_l=doc[0]
            g_l=doc[1]   # get a list of phi,g,t
            t_l=doc[2]

            dphi_l=tr.delta(phi_l,t_l) # compute the differences
            dg_l=tr.delta(g_l,t_l)
            dheading_l=tr.delta(tr.heading(phi_l,g_l),t_l)
            d_distance=tr.delta_distance(phi_l,g_l)

# we build a model with the statistical values of the features : variation of latitude, longitude, heading and distance

            model["µ"][x][y]["phi"] = tr.parameters(dphi_l)["mean"]
            model["µ"][x][y]["g"] = tr.parameters(dg_l)["mean"]    # met à jour le modele

            model["sigma"][x][y]["phi"] = tr.parameters(dphi_l)["standard_deviation"]
            model["sigma"][x][y]["g"] = tr.parameters(g_l)["standard_deviation"]


            model["µ"][x][y]["heading"] = tr.parameters(dheading_l)["mean"]
            model["µ"][x][y]["distance"] = tr.parameters(d_distance)["mean"]

            model["sigma"][x][y]["heading"] = tr.parameters(dheading_l)["standard_deviation"]
            model["sigma"][x][y]["distance"] = tr.parameters(d_distance)["standard_deviation"]

    with open('model.sauv','wb' ) as model_sauv_file: 
        pk.dump(model, model_sauv_file) # save the model in a binary file

    return model

training(md.model())
