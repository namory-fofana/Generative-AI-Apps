# Image Python avec beaucoup de paquets précompilés pour éviter build-essential
FROM python:3.11

# Répertoire de travail
WORKDIR /app

# Copier uniquement requirements.txt pour profiter du cache Docker
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source après l'installation des dépendances
COPY app.py .

# Exposer le port Streamlit
EXPOSE 8501

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Commande pour lancer l'application
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
