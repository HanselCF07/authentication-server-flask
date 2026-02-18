FROM python:3.14-slim

# Usa LABEL en lugar de Maintainer
LABEL org.opencontainers.image.authors="hansel_prins10@hotmail.com"

# Definir el directorio de trabajo
WORKDIR /authentication_server_example

# Copiar primero requirements para aprovechar el caché
COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . .

# Exponer solo el puerto 5000
EXPOSE 5000

# Ejecutar Gunicorn en el puerto 5000
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "run:app"]