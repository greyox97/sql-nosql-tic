from flask import Blueprint, request, jsonify
from controllers.consulta_controller import procesar_consulta

consulta_routes = Blueprint('consulta_routes', __name__)

@consulta_routes.route('/consulta', methods=['POST'])
def consulta():
    return procesar_consulta()

@consulta_routes.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200
