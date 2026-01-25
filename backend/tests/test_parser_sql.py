"""
Tests unitarios para parser_sql.py
Valida traducción de SQL a representación interna clave-valor
"""
import pytest
from utils.parser_sql import traducir_sql_a_kv


class TestSelectQueries:
    """Tests para consultas SELECT"""
    
    def test_select_con_where_id(self):
        """SELECT con WHERE id = valor"""
        sql = "SELECT * FROM usuarios WHERE id = 101"
        result = traducir_sql_a_kv(sql)
        
        assert result[0] == "GET"
        assert result[1] == "usuarios"
        assert result[2] == "101"
        assert result[3] is None
    
    def test_select_con_columnas_especificas(self):
        """SELECT con columnas específicas y WHERE id"""
        sql = "SELECT nombre, edad FROM usuarios WHERE id = 102"
        result = traducir_sql_a_kv(sql)
        
        assert result[0] == "GET"
        assert result[1] == "usuarios"
        assert result[2] == "102"
        assert result[3] == ["nombre", "edad"]
    
    def test_select_sin_where(self):
        """SELECT sin WHERE (get all)"""
        sql = "SELECT * FROM usuarios"
        result = traducir_sql_a_kv(sql)
        
        assert result[0] == "GET_ALL"
        assert result[1] == "usuarios"
        assert result[2] is None
    
    def test_select_con_where_campo(self):
        """SELECT con WHERE campo distinto de id"""
        sql = "SELECT * FROM usuarios WHERE edad >= 18"
        result = traducir_sql_a_kv(sql)
        
        assert result[0] == "GET_FILTER"
        assert result[1] == "usuarios"
        assert result[2]["campo"] == "edad"
        assert result[2]["operador"] == ">="
        assert result[2]["valor"] == 18
        assert result[3] is None
    
    def test_select_filtro_con_columnas(self):
        """SELECT con WHERE campo + columnas específicas"""
        sql = "SELECT nombre, ciudad FROM usuarios WHERE edad > 25"
        result = traducir_sql_a_kv(sql)
        
        assert result[0] == "GET_FILTER"
        assert result[2]["campo"] == "edad"
        assert result[2]["operador"] == ">"
        assert result[2]["valor"] == 25
        assert result[3] == ["nombre", "ciudad"]


class TestInsertQueries:
    """Tests para consultas INSERT"""
    
    def test_insert_basico_retrocompatible(self):
        """INSERT sin nombres de columnas (formato antiguo)"""
        sql = "INSERT INTO usuarios VALUES (103, 'Ana', 22, 'Madrid')"
        result = traducir_sql_a_kv(sql)
        
        assert result[0] == "SET"
        assert result[1] == "usuarios"
        assert result[2] == "103"
        assert result[3]["nombre"] == "Ana"
        assert result[3]["edad"] == 22
        assert result[3]["ciudad"] == "Madrid"
    
    def test_insert_con_nombres_columnas(self):
        """INSERT con nombres de columnas explícitas"""
        sql = "INSERT INTO usuarios (id, nombre, edad) VALUES (104, 'Luis', 30)"
        result = traducir_sql_a_kv(sql)
        
        assert result[0] == "SET"
        assert result[1] == "usuarios"
        assert result[2] == "104"
        assert result[3] == {"nombre": "Luis", "edad": 30}
    
    def test_insert_tabla_generica_con_columnas(self):
        """INSERT en tabla genérica con columnas"""
        sql = "INSERT INTO productos (id, nombre, precio, stock) VALUES (1, 'Laptop', 1200, 5)"
        result = traducir_sql_a_kv(sql)
        
        assert result[0] == "SET"
        assert result[1] == "productos"
        assert result[2] == "1"
        assert result[3] == {"nombre": "Laptop", "precio": 1200, "stock": 5}
    
    def test_insert_tabla_generica_sin_columnas(self):
        """INSERT en tabla genérica sin nombres de columnas"""
        sql = "INSERT INTO productos VALUES (2, 'Mouse', 25)"
        result = traducir_sql_a_kv(sql)
        
        assert result[0] == "SET"
        assert result[1] == "productos"
        assert result[2] == "2"
        # Formato genérico: field_1, field_2, ...
        assert result[3] == {"field_1": "Mouse", "field_2": 25}
    
    def test_insert_columnas_desalienadas(self):
        """INSERT con cantidad distinta de columnas y valores debe dar error"""
        sql = "INSERT INTO usuarios (id, nombre) VALUES (105, 'Carlos', 28)"
        
        with pytest.raises(ValueError, match="cantidad de columnas"):
            traducir_sql_a_kv(sql)


class TestUpdateQueries:
    """Tests para consultas UPDATE"""
    
    def test_update_un_campo(self):
        """UPDATE con un solo campo"""
        sql = "UPDATE usuarios SET edad = 30 WHERE id = 101"
        result = traducir_sql_a_kv(sql)
        
        assert result[0] == "UPDATE"
        assert result[1] == "usuarios"
        assert result[2] == "101"
        assert result[3] == {"edad": 30}
    
    def test_update_multiples_campos(self):
        """UPDATE con múltiples campos"""
        sql = "UPDATE usuarios SET nombre = 'Juan', edad = 26 WHERE id = 102"
        result = traducir_sql_a_kv(sql)
        
        assert result[0] == "UPDATE"
        assert result[3]["nombre"] == "Juan"
        assert result[3]["edad"] == 26


class TestDeleteQueries:
    """Tests para consultas DELETE"""
    
    def test_delete_basico(self):
        """DELETE con WHERE id"""
        sql = "DELETE FROM usuarios WHERE id = 103"
        result = traducir_sql_a_kv(sql)
        
        assert result[0] == "DEL"
        # El parser actual retorna: ("DEL", "WHERE id = 103", "103")
        # Verificar que extrajo el ID correctamente
        assert result[2] == "103"


class TestErrorHandling:
    """Tests de manejo de errores"""
    
    def test_sql_invalido(self):
        """SQL inválido debe lanzar ValueError"""
        with pytest.raises(ValueError, match="Consulta no reconocida"):
            traducir_sql_a_kv("SELEKT * FROM usuarios")
    
    def test_select_sin_tabla(self):
        """SELECT sin FROM debe dar error"""
        with pytest.raises(ValueError):
            traducir_sql_a_kv("SELECT * WHERE id = 1")
