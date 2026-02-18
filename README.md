# Run With: Python 3.14.3 Version

# authentication_server_example
    Python Flask - authentication server example



# Build the image (Docker slim images by default expose port 8000; use the `--no-cache` command to avoid affecting the image's base configuration)
    docker build --no-cache -t authentication-server-example:v1 .

# Inspect Docker Img
    docker inspect authentication-server-example:v1 | grep ExposedPorts -A 5

# Run Docker img
    docker run -d -p 5000:5000 authentication-server-example:v1

# Run the container in localhost:8000 and inject environment variables
# Remember to create a file with the environment variables used in the App Configuration
    docker run -d -p 5000:5000 --env-file .env authentication-server-example:v1



# Start Minikube (if it is not running)
    minikube start --driver=docker

# Running the following command will send the images directly to the cluster from your current terminal:
    eval $(minikube docker-env)

# View images uploaded to minikube
    minikube image ls

# Upload the image directly to the cluster (without registry)
    minikube image load authentication-server-example:v1  # Si usas Minikube
    
    kind load docker-image authentication-server-example:v1 # Si usas Kind




# Create Deployment and Service
    kubectl apply -f k8s-deployment.yaml
    kubectl apply -f k8s-service.yaml

# Configure Ingress
    kubectl apply -f k8s-ingress.yaml

# Activar el Ingress Controller (minikube)
    minikube addons enable ingress

# View pods
    kubectl get pods
# View servicios
    kubectl get svc




# Remember to modify the nginx configuration to send requests to the cluster's Ingress server.
    server {
        listen 80;
        server_name 192.168.1.47; # server ip or server domain

        location / {
            proxy_pass http://192.168.49.2:80; # cluster ip or cluster domain
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }

# Test API
    curl -X POST http://<ip-or-domain>/api/v1/authentication/user/login \
    -H "Content-Type: application/json" \


# Port forwarding (Fastest for testing)
    kubectl port-forward --address 0.0.0.0 service/SERVICE_NAME 5000:5000 (PORT_EXPOSED):(PORT_SERVICE)


# Script for MAP DB MODEL
    flask-sqlacodegen --flask --outfile user.py --schema "vg_store" --tables "user" postgresql+psycopg2://dev_user:dev_123@192.168.1.47:5432/db_store
