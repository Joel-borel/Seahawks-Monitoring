# Dockerfile - SeahawksNester
FROM python:3.12-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers du projet dans le conteneur
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Exposer le port (FastAPI + Flask utilisent 8000 et 5000)
EXPOSE 8000
EXPOSE 5000

# Lancer les deux serveurs (API + Interface web Flask) via un script
CMD ["sh", "-c", "uvicorn nesterAPI.api:app --host 0.0.0.0 --port 8000 & python app.py"]