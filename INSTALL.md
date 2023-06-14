# Installation

Une fois récupéré le code source (```git clone https://github.com/jmtrivial/sis.git```), installer ```pyinstaller``` ave la commande ```pip install pyinstaller```, puis utiliser la commande suivante pour fabriquer un exécutable (éventuellement avec le chemin d'accès à pyinstaller s'il n'est pas dans le PATH, de la forme ```c:\users\<utilisateur>\appdata\local\packages\...\localcache\local-packages\python311\site-packages```):

* ```pyinstaller --onfile --windowed prototype.py```

Il est alors généré dans le dossier ```dist```. Le déplacer dans le dossier où il y a le code source (sinon les images ne sont pas chargées au démarrage de l'application).

Remarque: 
* on peut changer l'icône (à faire).