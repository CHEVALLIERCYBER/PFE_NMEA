Ces progragrammes permmettent d'obtenir le score de programmes de classification, fonctionnant grâce à l'apprentissage automatique, dont le but est la détection en temps réel d'anomalie sur des trames NMEA GPS RMC.

Ils prennent tous en entrée des trames NMEA d'un batiment en temps réél (Par exemple produit par le simulateur Bridge Command), sur le port 5005
Ils utilisent tous le fichier de données d'entrainement RMCbien.json (fichier disponible dans le dossier dataset)

--------------------------------------------------------------------------------------------------------------------------------------------

confusion_matrix_distance.py et confusion_matrix_cap.py permettent de determiner les meilleurs évaluteurs avec les meilleurs paramètres pour la detection d'anomalies de cap et de distance sur les trames NMEA GPS RMC, respectivement. Le score est déterminé à partir du résultat de la classification simultanée de 100 trames RMC par tout les évaluateurs. Beaucoup d'évaluateurs sont testés en même temps, le programme peut mettre du temps à s'executer.

--------------------------------------------------------------------------------------------------------------------------------------------

score_SVM.py permet d'obtenir le score d'un programme conbinant un évaluateur SVM de cap et un évaluateur de distance sur 100 trames RMC, en temps réél. Leurs paramètres ont été choisis grâce aux programmes confusion_matrix_distance.py et confusion_matrix_cap.py



