"""
Tests de integración end-to-end
Valida el endpoint /consulta completo
"""
import pytest
from flask import Flask
from routes import consulta_routes


@pytest.fixture
def client():
    """Cliente de prueba Flask"""
    app = Flask(__name__)
    app.register_blueprint(consulta_routes)
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        yield client


class TestEndpointValidaciones:
    """Tests de validaciones del endpoint"""
    
    def test_payload_vacio(self, client):
        """POST sin payload debe retornar 400"""
        response = client.post('/consulta')
        
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert "vacío" in data["error"].lower()
    
    def test_sql_vacio(self, client):
        """POST con SQL vacío debe retornar 400"""
        response = client.post('/consulta', json={"sql": ""})
        
        assert response.status_code == 400
        data = response.get_json()
        assert "vacía" in data["error"].lower()
    
    def test_sql_solo_espacios(self, client):
        """SQL con solo espacios debe retornar 400"""
        response = client.post('/consulta', json={"sql": "   "})
        
        assert response.status_code == 400
        data = response.get_json()
        assert "vacía" in data["error"].lower()
    
    def test_sql_invalido(self, client):
        """SQL inválido debe retornar 400 con ValueError"""
        response = client.post('/consulta', json={
            "sql": "SELEKT * FROM usuarios"
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert "validación" in data["error"].lower()


class TestEndpointFuncional:
    """Tests de funcionalidad del endpoint"""
    
    def test_consulta_sql_estructura_respuesta(self, client):
        """Respuesta debe tener estructura correcta"""
        response = client.post('/consulta', json={
            "sql": "SELECT * FROM usuarios WHERE id = 101"
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert "original" in data
        assert "traducida" in data
        assert "resultado" in data
    
    def test_consulta_nosql_estructura_respuesta(self, client):
        """Respuesta NoSQL debe tener estructura correcta"""
        response = client.post('/consulta', json={
            "nosql": {
                "operacion": "GET",
                "tabla": "usuarios",
                "id": "101",
                "columnas": None
            }
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert "original" in data
        assert "traducida" in data
        assert "resultado" in data
