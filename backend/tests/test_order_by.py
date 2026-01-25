"""
Tests para ORDER BY
"""
import pytest
from utils.parser_sql import traducir_sql_a_kv


class TestOrderBy:
    """Tests para ORDER BY en SELECT"""
    
    def test_order_by_asc_default(self):
        """SELECT con ORDER BY sin especificar dirección (ASC por defecto)"""
        sql = "SELECT * FROM usuarios ORDER BY edad"
        result = traducir_sql_a_kv(sql)
        
        assert result[0] == "GET_ALL_ORDERED"
        assert result[1] == "usuarios"
        assert result[2] is None  # columnas (*)
        assert result[3] == "edad"  # campo de ordenamiento
        assert result[4] == "ASC"  # dirección por defecto
    
    def test_order_by_asc_explicito(self):
        """SELECT con ORDER BY ASC explícito"""
        sql = "SELECT * FROM usuarios ORDER BY nombre ASC"
        result = traducir_sql_a_kv(sql)
        
        assert result[0] == "GET_ALL_ORDERED"
        assert result[3] == "nombre"
        assert result[4] == "ASC"
    
    def test_order_by_desc(self):
        """SELECT con ORDER BY DESC"""
        sql = "SELECT * FROM productos ORDER BY precio DESC"
        result = traducir_sql_a_kv(sql)
        
        assert result[0] == "GET_ALL_ORDERED"
        assert result[1] == "productos"
        assert result[3] == "precio"
        assert result[4] == "DESC"
    
    def test_order_by_con_columnas(self):
        """SELECT con columnas específicas y ORDER BY"""
        sql = "SELECT nombre, edad FROM usuarios ORDER BY edad DESC"
        result = traducir_sql_a_kv(sql)
        
        assert result[0] == "GET_ALL_ORDERED"
        assert result[2] == ["nombre", "edad"]
        assert result[3] == "edad"
        assert result[4] == "DESC"
    
    def test_select_sin_order_by(self):
        """SELECT sin ORDER BY debe seguir funcionando como GET_ALL"""
        sql = "SELECT * FROM usuarios"
        result = traducir_sql_a_kv(sql)
        
        assert result[0] == "GET_ALL"
        assert len(result) == 3  # No incluye order_campo ni order_dir
