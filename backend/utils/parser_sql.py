import sqlparse
import re

def _parsear_condicion(cond_str):
    """
    Parsea una condición individual del WHERE.
    Retorna dict con campo, operador, valor o None si no es válida.
    Soporta: =, >, <, >=, <=, LIKE, ILIKE
    """
    cond_str = cond_str.strip()
    
    # 1. Intentar LIKE / ILIKE primero (son palabras, no símbolos)
    match_like = re.match(
        r"(\w+)\s+(ILIKE|LIKE)\s+['\"]([^'\"]+)['\"]",
        cond_str, re.IGNORECASE
    )
    if match_like:
        campo = match_like.group(1).strip()
        operador = match_like.group(2).upper()  # Normalizar a mayúsculas
        valor = match_like.group(3)  # No strip, preservar espacios en patrón
        
        return {
            "campo": campo,
            "operador": operador,
            "valor": valor
        }
    
    # 2. Operadores de comparación: >=, <=, =, >, <
    match_cond = re.match(
        r"(\w+)\s*(>=|<=|=|>|<)\s*['\"]?([^'\"]+)['\"]?",
        cond_str
    )
    if match_cond:
        campo = match_cond.group(1).strip()
        operador = match_cond.group(2)
        valor = match_cond.group(3).strip()
        
        # Convertir a int si es posible
        if valor.isdigit():
            valor = int(valor)
        
        return {
            "campo": campo,
            "operador": operador,
            "valor": valor
        }
    
    return None

def _parsear_where_multiple(where_clause):
    """
    Parsea una cláusula WHERE con múltiples condiciones (AND/OR).
    Retorna dict con operador_logico y lista de condiciones.
    """
    # Detectar operador lógico
    if " AND " in where_clause.upper():
        operador_logico = "AND"
        condiciones_str = re.split(r"\s+AND\s+", where_clause, flags=re.IGNORECASE)
    elif " OR " in where_clause.upper():
        operador_logico = "OR"
        condiciones_str = re.split(r"\s+OR\s+", where_clause, flags=re.IGNORECASE)
    else:
        return None
    
    condiciones = []
    for cond_str in condiciones_str:
        cond = _parsear_condicion(cond_str)
        if cond:
            condiciones.append(cond)
    
    return {
        "operador_logico": operador_logico,
        "condiciones": condiciones
    }

def _normalizar_sql(sql):
    """
    Normaliza una consulta SQL para procesamiento:
    1. Normaliza whitespace (reemplaza múltiples espacios/newlines por un espacio)
    2. Elimina aliases de tabla (FROM users u -> FROM users)
    3. Elimina prefijos de alias en columnas (u.id -> id)
    """
    # 1. Normalizar whitespace
    sql = re.sub(r'\s+', ' ', sql).strip()
    
    # 2. Eliminar alias de tabla: FROM tabla alias -> FROM tabla
    # IMPORTANTE: No capturar palabras clave SQL como WHERE, ORDER, GROUP, LIMIT, etc.
    sql = re.sub(
        r'\bFROM\s+(\w+)\s+(?:AS\s+)?(?!WHERE|ORDER|GROUP|LIMIT|HAVING|UNION|JOIN|LEFT|RIGHT|INNER|OUTER)(\w+)\b',
        r'FROM \1',
        sql, flags=re.IGNORECASE
    )
    
    # 3. Eliminar prefijos de alias en columnas: alias.columna -> columna
    sql = re.sub(r'\b\w+\.(\w+)\b', r'\1', sql)
    
    return sql

def traducir_sql_a_kv(sql):
    sql = _normalizar_sql(sql)
    parsed = sqlparse.parse(sql)[0]
    tipo = parsed.get_type()
    tokens = [t.value for t in parsed.tokens if not t.is_whitespace]

    if tipo == "SELECT":
        sql = sql.strip(";").strip()

        # 0. SELECT con múltiples condiciones (AND/OR)
        # Detectar si hay AND u OR en la cláusula WHERE
        if re.search(r"\s+WHERE\s+.+\s+(AND|OR)\s+", sql, re.IGNORECASE):
            match_multiple = re.match(
                r"SELECT\s+(.*?)\s+FROM\s+(\w+)\s+WHERE\s+(.+)",
                sql, re.IGNORECASE
            )
            
            if match_multiple:
                columnas = match_multiple.group(1).strip()
                tabla = match_multiple.group(2)
                where_clause = match_multiple.group(3).strip()
                
                # Usar función auxiliar para parsear múltiples condiciones
                filtro = _parsear_where_multiple(where_clause)
                
                if filtro:
                    # Procesar columnas
                    if columnas == "*":
                        columnas = None
                    else:
                        columnas = [c.strip() for c in columnas.split(",")]
                    
                    return ("GET_FILTER_MULTIPLE", tabla, filtro, columnas)

        # 1. SELECT con condición simple (usando función auxiliar para soportar LIKE/ILIKE)
        match_where = re.match(
            r"SELECT\s+(.*?)\s+FROM\s+(\w+)\s+WHERE\s+(.+)",
            sql, re.IGNORECASE
        )
        if match_where:
            columnas = match_where.group(1).strip()
            tabla = match_where.group(2)
            where_clause = match_where.group(3).strip()
            
            # Usar función auxiliar para parsear la condición
            cond = _parsear_condicion(where_clause)
            
            if cond:
                campo = cond["campo"]
                
                # Si es id, dejarlo para match_id (más específico)
                if campo.lower() == "id" and cond["operador"] == "=":
                    pass  # Dejar que lo maneje match_id abajo
                else:
                    if columnas == "*":
                        columnas = None
                    else:
                        columnas = [c.strip() for c in columnas.split(",")]
                    
                    return ("GET_FILTER", tabla, cond, columnas)

        # 2. SELECT con WHERE id = ...
        match_id = re.match(
            r"SELECT\s+(.*?)\s+FROM\s+(\w+)\s+WHERE\s+id\s*=\s*['\"]([^'\"]+)['\"]",
            sql, re.IGNORECASE
        )
        if match_id:
            columnas = match_id.group(1).strip()
            tabla = match_id.group(2)
            id_val = match_id.group(3)

            if columnas == "*":
                columnas = None
            else:
                columnas = [col.strip() for col in columnas.split(",")]

            return ("GET", tabla, id_val, columnas)

        # 3. SELECT sin WHERE
        match_all = re.match(
            r"SELECT\s+(.*?)\s+FROM\s+(\w+)(?:\s+ORDER\s+BY\s+(\w+)(?:\s+(ASC|DESC))?)?",
            sql, re.IGNORECASE
        )
        if match_all:
            columnas = match_all.group(1).strip()
            tabla = match_all.group(2)
            order_campo = match_all.group(3)  # Puede ser None si no hay ORDER BY
            order_dir = match_all.group(4) if match_all.group(4) else "ASC"  # Default ASC

            if columnas == "*":
                columnas = None
            else:
                columnas = [col.strip() for col in columnas.split(",")]
            
            # Agregar información de ORDER BY a la tupla
            if order_campo:
                return ("GET_ALL_ORDERED", tabla, columnas, order_campo, order_dir.upper())
            else:
                return ("GET_ALL", tabla, columnas)

        raise ValueError("No se pudo analizar la sentencia SELECT.")



    elif tipo == "INSERT":
        # Detectar INSERT INTO tabla (cols) VALUES (...), (...), ...
        match_batch = re.match(
            r"INSERT\s+INTO\s+(\w+)\s*\((.*?)\)\s+VALUES\s*(.*)",
            sql, re.IGNORECASE | re.DOTALL
        )
        
        if match_batch:
            tabla = match_batch.group(1)
            columnas_str = match_batch.group(2)
            valores_completo = match_batch.group(3).strip().rstrip(";")
            
            # Separar columnas
            columnas = [c.strip() for c in columnas_str.split(",")]
            
            # Extraer todas las tuplas de valores: (...), (...), ...
            tuplas = re.findall(r"\(([^)]+)\)", valores_completo)
            
            if len(tuplas) == 0:
                raise ValueError("No se encontraron valores en el INSERT")
            
            # Si es una sola tupla, usar SET normal
            if len(tuplas) == 1:
                valores = [v.strip().strip("'\"") for v in tuplas[0].split(",")]
                
                if len(columnas) != len(valores):
                    raise ValueError("La cantidad de columnas no coincide con la cantidad de valores")
                
                id_val = valores[0].strip().strip("'\"")
                payload = {}
                for i, col in enumerate(columnas[1:], start=1):
                    valor = valores[i]
                    payload[col] = int(valor) if valor.isdigit() else valor
                
                return ("SET", tabla, id_val, payload)
            
            # Si son múltiples tuplas, usar SET_BATCH
            batch_data = {}
            for tupla in tuplas:
                valores = [v.strip().strip("'\"") for v in tupla.split(",")]
                
                if len(columnas) != len(valores):
                    raise ValueError(f"La cantidad de columnas no coincide con los valores en: ({tupla})")
                
                id_val = valores[0].strip().strip("'\"")
                payload = {}
                for i, col in enumerate(columnas[1:], start=1):
                    valor = valores[i]
                    payload[col] = int(valor) if valor.isdigit() else valor
                
                batch_data[id_val] = payload
            
            return ("SET_BATCH", tabla, batch_data)
        
        # Opción 2: INSERT INTO tabla VALUES (val1, val2, ...) - Retrocompatibilidad
        match_without_columns = re.match(
            r"INSERT\s+INTO\s+(\w+)\s+VALUES\s*\((.*?)\)",
            sql, re.IGNORECASE
        )
        
        if match_without_columns:
            tabla = match_without_columns.group(1)
            valores_str = match_without_columns.group(2)
            valores = [v.strip().strip("'\"") for v in valores_str.split(",")]
            
            id_val = valores[0].strip().strip("'\"")
            
            # Mantener retrocompatibilidad con tabla "usuarios"
            if tabla.lower() == "usuarios" and len(valores) == 4:
                payload = {
                    "nombre": valores[1],
                    "edad": int(valores[2]) if valores[2].isdigit() else valores[2],
                    "ciudad": valores[3]
                }
            else:
                # Formato genérico: field_1, field_2, ...
                payload = {}
                for i, val in enumerate(valores[1:], start=1):
                    key = f"field_{i}"
                    payload[key] = int(val) if val.isdigit() else val
            
            return ("SET", tabla, id_val, payload)
        
        raise ValueError("INSERT no reconocido. Use: INSERT INTO tabla (cols) VALUES (vals) o INSERT INTO tabla VALUES (vals)")

    elif tipo == "DELETE":
        sql_clean = sql.strip(";").strip()
        
        # Extraer tabla y WHERE clause
        match_delete_base = re.match(
            r"DELETE\s+FROM\s+(\w+)\s+WHERE\s+(.+)",
            sql_clean, re.IGNORECASE
        )
        
        if not match_delete_base:
            raise ValueError("DELETE no reconocido. Use: DELETE FROM tabla WHERE condicion")
        
        tabla = match_delete_base.group(1)
        where_clause = match_delete_base.group(2).strip()
        
        # 1. Verificar si es DELETE con múltiples condiciones (AND/OR)
        if re.search(r"\s+(AND|OR)\s+", where_clause, re.IGNORECASE):
            filtro = _parsear_where_multiple(where_clause)
            if filtro:
                return ("DEL_FILTER_MULTIPLE", tabla, filtro)
        
        # 2. DELETE por ID (caso especial optimizado)
        match_id = re.match(r"id\s*=\s*['\"]?([^'\";\s]+)['\"]?", where_clause, re.IGNORECASE)
        if match_id:
            id_val = match_id.group(1)
            return ("DEL", tabla, id_val)
        
        # 3. DELETE por campo simple (ej: company = 'X')
        cond = _parsear_condicion(where_clause)
        if cond:
            return ("DEL_FILTER", tabla, cond)
        
        raise ValueError("DELETE no reconocido. Use: DELETE FROM tabla WHERE campo = 'valor'")

    elif tipo == "UPDATE":
        sql_clean = sql.strip(";").strip()
        
        # Extraer tabla, SET clause y WHERE clause
        match_update = re.match(
            r"UPDATE\s+(\w+)\s+SET\s+(.+?)\s+WHERE\s+(.+)",
            sql_clean, re.IGNORECASE
        )
        
        if not match_update:
            raise ValueError("UPDATE no reconocido. Use: UPDATE tabla SET campo = valor WHERE condicion")
        
        tabla = match_update.group(1)
        set_clause = match_update.group(2).strip()
        where_clause = match_update.group(3).strip()
        
        # Parsear SET clause
        campos = set_clause.split(",")
        payload = {}
        for campo in campos:
            if "=" not in campo:
                continue
            k, v = campo.strip().split("=", 1)  # split solo en el primer =
            k = k.strip()
            v = v.strip().strip("'").strip('"')
            payload[k] = int(v) if v.isdigit() else v
        
        if not payload:
            raise ValueError("No se encontraron campos válidos en la cláusula SET.")
        
        # 1. UPDATE con múltiples condiciones (AND/OR)
        if re.search(r"\s+(AND|OR)\s+", where_clause, re.IGNORECASE):
            filtro = _parsear_where_multiple(where_clause)
            if filtro:
                return ("UPDATE_FILTER_MULTIPLE", tabla, payload, filtro)
        
        # 2. UPDATE por ID (caso especial optimizado)
        match_id = re.match(r"id\s*=\s*['\"]?([^'\";\s]+)['\"]?", where_clause, re.IGNORECASE)
        if match_id:
            id_val = match_id.group(1)
            return ("UPDATE", tabla, id_val, payload)
        
        # 3. UPDATE por campo simple (ej: company ILIKE 'X%')
        cond = _parsear_condicion(where_clause)
        if cond:
            return ("UPDATE_FILTER", tabla, payload, cond)
        
        raise ValueError("UPDATE no reconocido. Use: UPDATE tabla SET ... WHERE condicion")

    raise ValueError("Consulta no reconocida")
