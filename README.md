# Seahawks Monitoring

Projet MSPR ASRBD 2024-2025 — Application de supervision réseau en Python et FastAPI.

## Description

Seahawks Monitoring est une solution de monitoring réseau composée de deux parties :

- *Seahawks Harvester* (client) : script Python déployé sur chaque franchise, permettant de scanner le réseau local (LAN) et d'envoyer les résultats à une API.
- *Seahawks Nester* (serveur) : application web FastAPI permettant de centraliser, visualiser et consulter les résultats envoyés par chaque Harvester.

## Fonctionnalités

### Seahawks Harvester
- Scan du réseau local (IP + état UP/DOWN)
- Détection automatique de l'IP locale
- Mesure de la latence WAN
- Génération d’un identifiant unique de la sonde
- Envoi automatique des résultats à l’API Seahawks Nester

### Seahawks Nester
- API REST avec FastAPI
- Tableau de bord des sondes : IP, état, nombre d’équipements, latence WAN, date du dernier scan
- Accès aux résultats de chaque scan
- Interface utilisateur responsive (HTML/CSS)
- Dockerisé avec Docker Compose

## Arborescence du projet


MSPR/
├── SeahawksHarvester/
│   ├── harvester.py
│   ├── dashboard.py
│   ├── Dockerfile
│   └── requirements.txt
├── SeahawksNester/
│   ├── app.py
│   ├── nesterAPI/
│   ├── templates/
│   ├── static/
│   ├── Dockerfile
│   └── docker-compose.yml
├── scan_results.json
└── README.md


## Lancer le projet

### 1. Lancer Nester (API + Web)
Depuis le dossier MSPR/SeahawksNester/ :
bash
docker-compose up --build

Accès :
- API : [http://localhost:8000/sondes](http://localhost:8000/sondes)
- Interface web : [http://localhost:5000](http://localhost:5000)

### 2. Lancer Harvester
Depuis le dossier MSPR/SeahawksHarvester/ :
bash
python harvester.py

> Nécessite Python 3.10+ et les dépendances de requirements.txt

## Captures d’écran

