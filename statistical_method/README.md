These scripts are using a statistical method in order to determine if a GNSS receiver is confronted with spoofing.

There are different scripts :

--------------------------------------------------------------------------------------------------------------------------------------------------------

  - traitement.py 
  
This script contains the statistical functions ( mean and standard deviation ), and other useful one like difference beetwen two lists.  

--------------------------------------------------------------------------------------------------------------------------------------------------------


  - man_in_the_middle.py
  
This script build a sockey to listen the output port of Bridge Command ( 127.0.0.1:5005), get the NMEA sentences, implement a real time alteration of a predifined number of sentences and put them to Open CPN.
  
In the same time, detection algorithms prediction_v1.py and prediction_v2.py are used to detect the anomalies.
  
--------------------------------------------------------------------------------------------------------------------------------------------------------

  - prediction.py

  - prediction2.py
  
These two scripts detect if a dataset is compromised by GNSS spoofing, with the use of differents features : latitude and longitude variations, heading and distance variations.

------------------------------------------------------------------------------------------------------------------------------------------------------

 - entrainement.py modele.py

The sript entrainement.py and modele.py are just used to explain how the model is computed, meanwhile the model is ever saved in the file /PFE_NMEA/datasets/model.sauv ( binary file containing a python object )

To comput the model again, run the script entrainement.py, with the dataset in the file Entrainement.zip.

--------------------------------------------------------------------------------------------------------------------------------------------------------

