"""
Tests para traductor_service.py
Valida conversión entre representaciones y lógica de traducción
"""
import pytest
from services.traductor_service import (
    convertir_a_nosql,
    convertir_a_sql
)


class TestConversionNoSQL:
    """Tests de conversión a formato NoSQL"""
    
    def test_convertir_get_a_nosql(self):
        """Convertir tupla GET a JSON NoSQL"""
        interna = ("GET", "usuarios", "101", None)
        nosql = convertir_a_nosql(interna)
        
        assert nosql["operacion"] == "GET"
        assert nosql["tabla"] == "usuarios"
        assert nosql["id"] == "101"
        assert nosql["columnas"] is None
    
    def test_convertir_get_all_a_nosql(self):
        """Convertir tupla GET_ALL a JSON NoSQL"""
        interna = ("GET_ALL", "usuarios", ["nombre", "edad"])
        nosql = convertir_a_nosql(interna)
        
        assert nosql["operacion"] == "GET_ALL"
        assert nosql["tabla"] == "usuarios"
        assert nosql["columnas"] == ["nombre", "edad"]
    
    def test_convertir_get_filter_a_nosql(self):
        """Convertir tupla GET_FILTER a JSON NoSQL"""
        interna = ("GET_FILTER", "usuarios", 
                   {"campo": "edad", "operador": ">=", "valor": 18},
                   ["nombre", "edad"])
        nosql = convertir_a_nosql(interna)
        
        assert nosql["operacion"] == "GET_FILTER"
        assert nosql["filtro"]["campo"] == "edad"
        assert nosql["columnas"] == ["nombre", "edad"]


class TestConversionSQL:
    """Tests de conversión a formato SQL"""
    
    def test_convertir_nosql_get_a_sql(self):
        """Convertir NoSQL GET a SQL"""
        nosql = {
            "operacion": "GET",
            "tabla": "usuarios",
            "id": "101",
            "columnas": None
        }
        sql = convertir_a_sql(nosql)
        
        assert sql == "SELECT * FROM usuarios WHERE id = '101';"
    
    def test_convertir_nosql_get_all_a_sql(self):
        """Convertir NoSQL GET_ALL a SQL"""
        nosql = {
            "operacion": "GET_ALL",
            "tabla": "usuarios",
            "columnas": None
        }
        sql = convertir_a_sql(nosql)
        
        assert sql == "SELECT * FROM usuarios;"
    
    def test_convertir_nosql_filter_a_sql(self):
        """Convertir NoSQL GET_FILTER a SQL"""
        nosql = {
            "operacion": "GET_FILTER",
            "tabla": "usuarios",
            "filtro": {"campo": "edad", "operador": ">=", "valor": 18},
            "columnas": ["nombre", "edad"]
        }
        sql = convertir_a_sql(nosql)
        
        assert "SELECT nombre, edad FROM usuarios" in sql
        assert "WHERE edad >= 18" in sql
