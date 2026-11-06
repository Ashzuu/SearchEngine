# Projet UE5.3 - Moteur de recherche

## Objectif

Concevoir un moteur de recherches à partir de sources externes, comme des APIs et des bases documentaires.

## Architecture

Pour faire cela, j'ai conçu une architecture contenant :

- Un client (fait en Angular)
- Un serveur (fait en Python)

Le serveur est le projet sur lequel vous êtes en train de consulter le README.md

## Lancement de l'API

Pour lancer l'API, lancer les commandes suivantes :

``cd back/`` (si vous n'êtes pas déjà dans le back)

``pip install -r requirements.txt`` (Installation des dépendances)

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

## Lancement du front (Angular)

Pour lancer l'application web :

Dans un nouveau terminal :

``cd front`` (si vous n'êtes pas déjà dans le dossier)

``npm install`` (installation des dépendances)

``ng serve``

ou

``npm run start``

Vous devriez avoir le résultat suivant :

```
Initial chunk files | Names         | Raw size
main.js             | main          | 47.83 kB | 
styles.css          | styles        | 96 bytes | 

                    | Initial total | 47.93 kB

Application bundle generation complete. [1.960 seconds] - 2026-11-02T13:59:16.390Z

Watch mode enabled. Watching for file changes...
NOTE: Raw file sizes do not reflect development server per-request transformations.
  ➜  Local:   http://localhost:4200/
  ➜  press h + enter to show help
```