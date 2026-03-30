# Dockerfile pour NetWatch-L3RI
# Projet d'Examen DEVNET - L3 RI ISI Keur Massar

FROM python:3.9-slim

# Configuration des métadonnées
LABEL maintainer="L3 RI ISI Keur Massar"
LABEL description="Application Flask de monitoring de conteneurs Docker"
LABEL version="1.0"

# Définition du répertoire de travail
WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Copie du fichier des dépendances
COPY requirements.txt .

# Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie des fichiers de l'application
COPY app.py .
COPY templates/ ./templates/

# Création d'un utilisateur non-root pour la sécurité
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Exposition du port
EXPOSE 5000

# Variables d'environnement
ENV PYTHONPATH=/app
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Commande de démarrage
CMD ["python", "app.py"]
