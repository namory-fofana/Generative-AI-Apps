# Étape 1 : Utiliser une image légère
FROM python:3.10-slim AS base

# Ne pas générer de fichiers .pyc et forcer un stdout/stderr immédiat
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Définir le dossier de travail
WORKDIR /app

# Installer seulement ce qui est nécessaire pour pip (moins de packages)
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc curl && \
    rm -rf /var/lib/apt/lists/*

# Copier les dépendances en premier pour tirer profit du cache Docker
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install -r requirements.txt

# Copier le code après (cela évite de recompiler les dépendances à chaque changement de code)
COPY . .

# Exposer le port de Streamlit
EXPOSE 8501

# Vérification de santé (moins coûteuse)
HEALTHCHECK CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Commande de démarrage
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
