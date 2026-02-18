from src import app

if __name__ == '__main__':
    # host='0.0.0.0' es clave para que funcione con Docker
    app.run(host='0.0.0.0', port=5000)
