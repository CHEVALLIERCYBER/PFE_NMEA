#------------------------------------------------------------------------
#
# @Author : EV2 CHEVALLIER 
#
# @Date : 06.11.20
# @Location : École Navale / Chaire de Cyberdéfense des systèmes navals
# @Project : Projet de Fin d'Études
# @Subject : Real time detection of cyber anomalies upon a NMEA network by using machine learning methods
#------------------------------------------------------------------------
# @Title : Main
#------------------------------------------------------------------------
# @Description : # This programm execute the scripts to implement the statistical method, and compute a score calculation

# These test are real time
#------------------------------------------------------------------------

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pickle as pk

import training as ent
import model as md
import prediction_v1 as pr1
import prediction_v2 as pr2
import traitement as tr
import man_in_the_middle as mim

path=tr.set_path()


############### DYNAMICAL TEST #####################


mim.mim()
