# sis
salle d'immersion sonore

(Ce code fonctionne de paire avec son application android)
Pour faire fonctionner les programmes : 

	Dans server.py : 
		- Choisir un HOST et un PORT (lignes 16 et 17)

	Dans soundGestion.py :
		- Modifier le self.folder_path (ligne 31) : donner le chemin complet jusqu'au dossier contenant le code

	Dans config.json : 
		- renseigner les informations suivantes : "webdav_hostname", "webdav_login", "webdav_password", "audio_library"
