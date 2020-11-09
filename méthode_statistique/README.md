Les scripts présents dans ce dossiers permettent de déterminer via la méthode statistique si un recepteur est soumis à du leurrage GPS.

On distingue plusieurs scripts :

--------------------------------------------------------------------------------------------------------------------------------------------------------

  - traitement.py 
  
Ce scripts contient les fonctions statistiques ( moyenne et ecart-type) utilisées pour construire le modele

--------------------------------------------------------------------------------------------------------------------------------------------------------


  - man_in_the_middle.py
  
  
  
--------------------------------------------------------------------------------------------------------------------------------------------------------

  - prediction.py

  - prediction2.py
  
Ces deux programmes permettent de determiner si un jeu de donnees de test est soumis à du leurrage, en utilisant plusieurs features différents : 

Le programme prediction.py utilise les variations de phi et g, le programme prediction2.py utilise les variations de distance et de cap.


--------------------------------------------------------------------------------------------------------------------------------------------------------


 - entrainement.py modele.py

Le script entrainement.py et modele.py ne sont là qu'a titre d'indication pour montrer comment est calculé le modèle, qui est déjà enregistré sous la forme du fichier modele.sauv présent dans le dossier dataset.
Pour recalculer le modele, il est possible d'executer les scripts modele.py et entrainement.py en utilisant les données d'entrainement extraites du Entrainement.zip

--------------------------------------------------------------------------------------------------------------------------------------------------------

Executer le script main.py pour  : python3 main.py
