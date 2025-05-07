# Imagen base liviana con Python
FROM python:3.12-slim

# Desactiva prompts interactivos al instalar
ENV DEBIAN_FRONTEND=noninteractive

# Instala ffmpeg y dependencias necesarias
RUN apt-get update && \
    apt-get install -y ffmpeg gcc libffi-dev libnacl-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Crea el directorio de la app
WORKDIR /app

# Copia el código
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Comando por defecto al ejecutar el contenedor
CMD ["python", "/bot.py"]
