# Imagen base de Python
FROM python:3.9-slim-buster

# Variables de entorno
  # Evita que Python genere archivos pyc
ENV PYTHONDONTWRITEBYTECODE 1
  # Mostrar las salidas de la aplicación en tiempo real
ENV PYTHONUNBUFFERED 1

# Directorio de trabajo en el contenedor
WORKDIR /TestLSEG

# Copiar archivos necesarios
COPY . /TestLSEG/

# Instalar dependencias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Comando para iniciar la aplicación
CMD ["python", "Test3.py"]