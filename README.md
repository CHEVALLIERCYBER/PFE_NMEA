Ces programme determinent avec des méthodes d'intelligence artificielles si un récepteur GPS est soumis à du leurrage.
Il est necessaire de dipsoser du module pynmea2 présent a cette adresse : https://github.com/Knio/pynmea2

Il peut fonctionner pour déterminer un leurrage simulé sur une plateforme simulée, via le logiciel BridgeCommand.

Lancer le logiciel BridgeCommand

Dans ce dépot, on distingue 3 parties : 

  - un dossier méthode_statistique qui implémente et évalue les différentes fonctions relatives à la résolution statistique du problème ( voir le README.md du dossier pour plus d'informations)

  - un dossier méthode_svm_lof qui implémente et évalue plusieurs méthodes d'intelligence atrificielle ( via le module scikit-learn de python ) pour déterminer la présence ou non de leurrage.
  
  - un dossier script_final qui contient la version "prete à l'emploi" de ces deux types de scripts. 
