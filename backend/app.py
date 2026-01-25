from flask import Flask
from flask_cors import CORS
from routes import consulta_routes

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.register_blueprint(consulta_routes)

if __name__ == '__main__':
    app.run(debug=True)
