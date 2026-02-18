FROM python:3.14-slim

LABEL org.opencontainers.image.authors="hansel_prins10@hotmail.com"

# Define the working directory
WORKDIR /authentication-server-flask

# Copy requirements first to take advantage of the cache
COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Copy the source code
COPY . .

# Expose only port 5000
EXPOSE 5000

# Run Gunicorn on port 5000
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "run:app"]