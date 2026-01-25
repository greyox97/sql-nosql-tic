"""
Tests para WHERE con condiciones múltiples (AND/OR)
"""
import pytest
from utils.parser_sql import traducir_sql_a_kv


class TestWhereMultiple:
    """Tests para WHERE con AND/OR"""
    
    def test_where_and_simple(self):
        """SELECT con WHERE campo1 AND campo2"""
        sql = "SELECT * FROM usuarios WHERE edad >= 18 AND ciudad = 'Quito'"
        result = traducir_sql_a_kv(sql)
        
        assert result[0] == "GET_FILTER_MULTIPLE"
        assert result[1] == "usuarios"
        assert result[2]["operador_logico"] == "AND"
        assert len(result[2]["condiciones"]) == 2
        
        # Primera condición
        assert result[2]["condiciones"][0]["campo"] == "edad"
        assert result[2]["condiciones"][0]["operador"] == ">="
        assert result[2]["condiciones"][0]["valor"] == 18
        
        # Segunda condición
        assert result[2]["condiciones"][1]["campo"] == "ciudad"
        assert result[2]["condiciones"][1]["operador"] == "="
        assert result[2]["condiciones"][1]["valor"] == "Quito"
        
        assert result[3] is None  # columnas (*)
    
    def test_where_or_simple(self):
        """SELECT con WHERE campo1 OR campo2"""
        sql = "SELECT nombre, edad FROM usuarios WHERE edad < 18 OR edad > 65"
        result = traducir_sql_a_kv(sql)
        
        assert result[0] == "GET_FILTER_MULTIPLE"
        assert result[2]["operador_logico"] == "OR"
        assert len(result[2]["condiciones"]) == 2
        assert result[3] == ["nombre", "edad"]
    
    def test_where_and_tres_condiciones(self):
        """SELECT con WHERE con 3 condiciones AND"""
        sql = "SELECT * FROM productos WHERE precio > 100 AND stock >= 5 AND categoria = 'Electronica'"
        result = traducir_sql_a_kv(sql)
        
        assert result[0] == "GET_FILTER_MULTIPLE"
        assert result[2]["operador_logico"] == "AND"
        assert len(result[2]["condiciones"]) == 3
        
        assert result[2]["condiciones"][0]["campo"] == "precio"
        assert result[2]["condiciones"][1]["campo"] == "stock"
        assert result[2]["condiciones"][2]["campo"] == "categoria"
    
    def test_where_and_con_columnas_especificas(self):
        """SELECT con columnas específicas y WHERE AND"""
        sql = "SELECT nombre, ciudad FROM usuarios WHERE edad >= 25 AND edad <= 40"
        result = traducir_sql_a_kv(sql)
        
        assert result[0] == "GET_FILTER_MULTIPLE"
        assert result[3] == ["nombre", "ciudad"]
        assert len(result[2]["condiciones"]) == 2
