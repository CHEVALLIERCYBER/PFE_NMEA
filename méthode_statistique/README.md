Ce programme determine avec des méthodes d'intelligence si un recepteur GPS est soumis à du brouillage.

Il peut fonctionner pour déterminer un leurrage simulé sur une plateforme simulée, via le logiciel BridgeCommand.

Lancer le logiciel BridgeCommand

Il est necessaire de dipsoser du module pynmea2 présent a cette adresse : https://github.com/Knio/pynmea2

Executer le script main.py pour acceder à la méthode statistique : python3 main.py

Le script entrainement.py et modele.py ne sont là qu'a titre d'indication pour montrer comment est calculé le modèle, qui est déjà enregistré sous la forme du fichier modele.sauv .

Pour recalculer le modele, il est possible d'executer les scripts modele.py et entrainement.py en utilisant les données d'entrainement extraites du Entrainement.zip

Le script mim.py utilise ce fichier.

Executer le script svm_lof.py pour utiliser les autres méthodes de Machine Learning, ce programme évalue quelle est la méthode la plus efficace.
