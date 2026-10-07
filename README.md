# Projet UE5.3 - Moteur de recherche

### Objectif

Concevoir un moteur de recherches à partir de sources externes, comme des APIs et des bases documentaires.

### Architecture

Pour faire cela, j'ai conçu une architecture contenant :

- Un client (fait en Angular)
- Un serveur (fait en Python)

Le serveur est le projet sur lequel vous êtes en train de consulter le README.md

### Lancement de l'API

Pour lancer l'API, lancer la commande suivante :

``fastapi dev main.py``

Vous devriez avoir le résultat suivant :

```
⚡️ Starting FastAPI in development mode
 
🐍 Using import string: main:api
 
🌐 Server started at http://127.0.0.1:8000
   Documentation at http://127.0.0.1:8000/docs
   ```

Si besoin de changer le port d'exposition utilisé par l'API, vous pouvez en le spécifiant dans la commande suivante :

``fastapi dev main.py --port 8080`` (si je veux exposer sur le port 8080)

Pour une exposition en mode développement (du moins pas en localhost), il suffit simplement de faire la commande :

``fastapi run main.py``

(Vous pouvez également changer le port si vous le souhaitez, avec la commande) :

``fastapi run main.py --port 8080`` (si on veut l'exposer, encore une fois, sur le port 8080)
