# Utilise une image Python officielle
FROM python:3.12-slim

# Définir le répertoire de travail à l'intérieur du conteneur
WORKDIR /app

# Copier le fichier requirements.txt et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code de l'application dans le conteneur
COPY . .

# Définir la commande pour exécuter ton application
CMD ["python", "SeahawksHarvester/dashboard.py"]