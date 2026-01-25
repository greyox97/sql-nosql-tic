from utils.parser_sql import traducir_sql_a_kv
from database.firebase_client import get_todos, set_usuario, get_usuario, delete_usuario, get_todos_ordenados, set_masivo, update_usuario
import re

def _like_to_regex(pattern):
    """
    Convierte un patrón SQL LIKE a regex de Python.
    % -> .* (cualquier cantidad de caracteres)
    _ -> . (un solo caracter)
    """
    # 1. Reemplazar % y _ con placeholders temporales
    pattern = pattern.replace('%', '\x00PERCENT\x00').replace('_', '\x00UNDERSCORE\x00')
    # 2. Escapar caracteres especiales de regex
    escaped = re.escape(pattern)
    # 3. Restaurar placeholders como regex
    escaped = escaped.replace('\x00PERCENT\x00', '.*').replace('\x00UNDERSCORE\x00', '.')
    return f'^{escaped}$'

def _evaluar_condicion(registro, campo, operador, valor):
    """
    Evalúa si un registro cumple una condición.
    Soporta: =, >, <, >=, <=, LIKE, ILIKE
    """
    v = registro.get(campo)
    if v is None:
        return False
    
    try:
        if operador == "=":
            return v == valor
        elif operador == ">":
            return v > valor
        elif operador == "<":
            return v < valor
        elif operador == ">=":
            return v >= valor
        elif operador == "<=":
            return v <= valor
        elif operador == "LIKE":
            # Case-sensitive pattern matching
            if not isinstance(v, str):
                v = str(v)
            regex = _like_to_regex(valor)
            return bool(re.match(regex, v))
        elif operador == "ILIKE":
            # Case-insensitive pattern matching
            if not isinstance(v, str):
                v = str(v)
            regex = _like_to_regex(valor)
            return bool(re.match(regex, v, re.IGNORECASE))
    except (TypeError, re.error):
        return False
    
    return False

def traducir_y_ejecutar(sql):
    result = traducir_sql_a_kv(sql)
    op = result[0]
    if op == "GET":
        data = get_usuario(result[1], result[2])
        if result[3]:  # columnas específicas
            data = {k: v for k, v in data.items() if k in result[3]}
        return data
    elif op == "GET_ALL":
        todos = get_todos(result[1])
        if result[2]:  # columnas específicas
            for k in todos:
                todos[k] = {campo: valor for campo, valor in todos[k].items() if campo in result[2]}
        return todos
    elif op == "GET_ALL_ORDERED":
        # result = ("GET_ALL_ORDERED", tabla, columnas, order_campo, order_dir)
        tabla = result[1]
        columnas = result[2]
        order_campo = result[3]
        order_dir = result[4]
        
        # Obtener datos ordenados
        todos = get_todos_ordenados(tabla, order_campo, order_dir)
        
        # Aplicar proyección de columnas si es necesario
        if columnas:
            for k in todos:
                todos[k] = {campo: valor for campo, valor in todos[k].items() if campo in columnas}
        
        return todos
    elif op == "GET_FILTER":
        registros = None
        filtro = result[2]
        columnas = result[3]

        campo = filtro["campo"]
        operador = filtro["operador"]
        valor = filtro["valor"]
        
        # LIKE/ILIKE no son soportados por Firebase nativo, ir directo a filtrado en memoria
        if operador not in ("LIKE", "ILIKE"):
            # Intentar query nativa de Firebase primero (más eficiente)
            from database.firebase_client import get_filtrados_nativos
            registros = get_filtrados_nativos(result[1], campo, operador, valor)
        
        # Si query nativa no funcionó o es LIKE/ILIKE, hacer fallback a filtrado en memoria
        if registros is None:
            registros = get_todos(result[1]) or {}
            registros = {k: v for k, v in registros.items() if _evaluar_condicion(v, campo, operador, valor)}

        # Proyección de columnas (aplicar siempre, independiente del método)
        if columnas:
            filtrados = {}
            for k, v in registros.items():
                filtrados[k] = {c: val for c, val in v.items() if c in columnas}
            return filtrados

        return registros

    elif op == "GET_FILTER_MULTIPLE":
        registros = get_todos(result[1]) or {}
        filtro = result[2]
        columnas = result[3]
        
        operador_logico = filtro["operador_logico"]
        condiciones = filtro["condiciones"]
        
        def cumple_condiciones_multiples(registro):
            """Evalúa múltiples condiciones con lógica AND/OR"""
            resultados = [_evaluar_condicion(registro, c["campo"], c["operador"], c["valor"]) for c in condiciones]
            
            if operador_logico == "AND":
                return all(resultados)
            else:  # OR
                return any(resultados)
        
        filtrados = {k: v for k, v in registros.items() if cumple_condiciones_multiples(v)}
        
        # Proyección de columnas
        if columnas:
            for k in filtrados:
                filtrados[k] = {c: v for c, v in filtrados[k].items() if c in columnas}
        
        return filtrados

    elif op == "SET":
        tabla = result[1]
        set_usuario(tabla, result[2], result[3])
        return f"1 registro insertado en '{tabla}'"
    elif op == "DEL":
        tabla = result[1]
        eliminado = delete_usuario(tabla, result[2])
        if eliminado:
            return f"1 registro eliminado de '{tabla}'"
        else:
            return f"0 registros afectados. ID '{result[2]}' no existe en '{tabla}'"
    elif op == "UPDATE":
        tabla = result[1]
        update_usuario(tabla, result[2], result[3])
        return f"1 registro actualizado en '{tabla}'"
    elif op == "SET_BATCH":
        tabla = result[1]
        registros = result[2]
        set_masivo(tabla, registros)
        return f"{len(registros)} registros insertados en '{tabla}'"
    
    elif op == "DEL_FILTER":
        # result = ("DEL_FILTER", tabla, {campo, operador, valor})
        tabla = result[1]
        filtro = result[2]
        campo = filtro["campo"]
        operador = filtro["operador"]
        valor = filtro["valor"]
        
        # Obtener todos y filtrar
        registros = get_todos(tabla) or {}
        ids_eliminar = [k for k, v in registros.items() if _evaluar_condicion(v, campo, operador, valor)]
        
        eliminados = 0
        for id_reg in ids_eliminar:
            if delete_usuario(tabla, id_reg):
                eliminados += 1
        
        return f"{eliminados} registros eliminados de '{tabla}'"
    
    elif op == "DEL_FILTER_MULTIPLE":
        # result = ("DEL_FILTER_MULTIPLE", tabla, {operador_logico, condiciones})
        tabla = result[1]
        filtro = result[2]
        operador_logico = filtro["operador_logico"]
        condiciones = filtro["condiciones"]
        
        registros = get_todos(tabla) or {}
        
        def cumple_multiple(registro):
            resultados = [_evaluar_condicion(registro, c["campo"], c["operador"], c["valor"]) for c in condiciones]
            if operador_logico == "AND":
                return all(resultados)
            else:  # OR
                return any(resultados)
        
        ids_eliminar = [k for k, v in registros.items() if cumple_multiple(v)]
        eliminados = 0
        for id_reg in ids_eliminar:
            if delete_usuario(tabla, id_reg):
                eliminados += 1
        
        return f"{eliminados} registros eliminados de '{tabla}'"
    
    elif op == "UPDATE_FILTER":
        # result = ("UPDATE_FILTER", tabla, payload, {campo, operador, valor})
        tabla = result[1]
        payload = result[2]
        filtro = result[3]
        campo = filtro["campo"]
        operador = filtro["operador"]
        valor = filtro["valor"]
        
        registros = get_todos(tabla) or {}
        ids_actualizar = [k for k, v in registros.items() if _evaluar_condicion(v, campo, operador, valor)]
        
        actualizados = 0
        for id_reg in ids_actualizar:
            update_usuario(tabla, id_reg, payload)
            actualizados += 1
        
        return f"{actualizados} registros actualizados en '{tabla}'"
    
    elif op == "UPDATE_FILTER_MULTIPLE":
        # result = ("UPDATE_FILTER_MULTIPLE", tabla, payload, {operador_logico, condiciones})
        tabla = result[1]
        payload = result[2]
        filtro = result[3]
        operador_logico = filtro["operador_logico"]
        condiciones = filtro["condiciones"]
        
        registros = get_todos(tabla) or {}
        
        def cumple_multiple(registro):
            resultados = [_evaluar_condicion(registro, c["campo"], c["operador"], c["valor"]) for c in condiciones]
            if operador_logico == "AND":
                return all(resultados)
            else:
                return any(resultados)
        
        ids_actualizar = [k for k, v in registros.items() if cumple_multiple(v)]
        actualizados = 0
        for id_reg in ids_actualizar:
            update_usuario(tabla, id_reg, payload)
            actualizados += 1
        
        return f"{actualizados} registros actualizados en '{tabla}'"



def convertir_a_nosql(interna):
    op = interna[0]

    if op == "GET":
        return {
            "operacion": "GET",
            "tabla": interna[1],
            "id": interna[2],
            "columnas": interna[3]
        }

    elif op == "GET_ALL":
        return {
            "operacion": "GET_ALL",
            "tabla": interna[1],
            "columnas": interna[2]
        }

    elif op == "GET_ALL_ORDERED":
        return {
            "operacion": "GET_ALL_ORDERED",
            "tabla": interna[1],
            "columnas": interna[2],
            "order_campo": interna[3],
            "order_direccion": interna[4]
        }

    elif op == "GET_FILTER":
        return {
            "operacion": "GET_FILTER",
            "tabla": interna[1],
            "filtro": interna[2],
            "columnas": interna[3]
        }

    elif op == "GET_FILTER_MULTIPLE":
        return {
            "operacion": "GET_FILTER_MULTIPLE",
            "tabla": interna[1],
            "filtro": interna[2],
            "columnas": interna[3]
        }

    elif op == "SET":
        return {
            "operacion": "SET",
            "tabla": interna[1],
            "id": interna[2],
            "datos": interna[3]
        }

    elif op == "UPDATE":
        return {
            "operacion": "UPDATE",
            "tabla": interna[1],
            "id": interna[2],
            "datos": interna[3]
        }

    elif op == "DEL":
        return {
            "operacion": "DEL",
            "tabla": interna[1],
            "id": interna[2]
        }

    elif op == "SET_BATCH":
        return {
            "operacion": "SET_BATCH",
            "tabla": interna[1],
            "registros": interna[2]
        }

    elif op == "DEL_FILTER":
        return {
            "operacion": "DEL_FILTER",
            "tabla": interna[1],
            "filtro": interna[2]
        }

    elif op == "DEL_FILTER_MULTIPLE":
        return {
            "operacion": "DEL_FILTER_MULTIPLE",
            "tabla": interna[1],
            "filtro": interna[2]
        }

    elif op == "UPDATE_FILTER":
        return {
            "operacion": "UPDATE_FILTER",
            "tabla": interna[1],
            "datos": interna[2],
            "filtro": interna[3]
        }

    elif op == "UPDATE_FILTER_MULTIPLE":
        return {
            "operacion": "UPDATE_FILTER_MULTIPLE",
            "tabla": interna[1],
            "datos": interna[2],
            "filtro": interna[3]
        }

    return {"operacion": "desconocida"}

def generar_firebase_queries(nosql):
    """
    Genera snippets de código para JS y Python basados en la operación NoSQL.
    Incluye código detallado paso a paso para operaciones híbridas.
    """
    op = nosql.get("operacion")
    tabla = nosql.get("tabla")
    
    js_code = ""
    py_code = ""

    if op == "GET":
        id_val = nosql.get("id")
        js_code = f"firebase.database().ref('{tabla}/{id_val}').once('value');"
        py_code = f"db.reference('{tabla}/{id_val}').get()"

    elif op == "GET_ALL":
        js_code = f"firebase.database().ref('{tabla}').once('value');"
        py_code = f"db.reference('{tabla}').get()"

    elif op == "GET_ALL_ORDERED":
        campo = nosql.get("order_campo")
        direccion = nosql.get("order_direccion", "ASC")
        js_code = f"""// Firebase siempre ordena ASC, invertir en cliente para DESC
const snap = await firebase.database().ref('{tabla}').orderByChild('{campo}').once('value');
let registros = Object.entries(snap.val() || {{}});
{"registros = registros.reverse();" if direccion == "DESC" else "// Ya está en ASC"}"""
        py_code = f"""# Firebase siempre ordena ASC
ref = db.reference('{tabla}').order_by_child('{campo}').get()
{"registros = dict(reversed(list(ref.items())))" if direccion == "DESC" else "registros = ref"}"""

    elif op == "GET_FILTER":
        filtro = nosql.get("filtro")
        campo = filtro["campo"]
        operador = filtro["operador"]
        valor = filtro["valor"]

        if operador == "=":
            js_code = f"firebase.database().ref('{tabla}').orderByChild('{campo}').equalTo('{valor}').once('value');"
            py_code = f"db.reference('{tabla}').order_by_child('{campo}').equal_to('{valor}').get()"
        elif operador in ("LIKE", "ILIKE"):
            regex_pattern = valor.replace('%', '.*')
            flag = "i" if operador == "ILIKE" else ""
            js_code = f"""// Firebase no soporta {operador}. Filtrar en cliente:
const snap = await firebase.database().ref('{tabla}').once('value');
const registros = snap.val() || {{}};
const filtrados = Object.fromEntries(
    Object.entries(registros).filter(([id, r]) => 
        /{regex_pattern}/{flag}.test(r.{campo} || '')
    )
);"""
            py_code = f"""# Firebase no soporta {operador}. Filtrar en cliente:
import re
registros = db.reference('{tabla}').get() or {{}}
patron = r'{regex_pattern}'
filtrados = {{k: v for k, v in registros.items() if re.match(patron, str(v.get('{campo}', '')){", re.IGNORECASE" if operador == "ILIKE" else ""})}}"""
        else:
            js_code = f"firebase.database().ref('{tabla}').orderByChild('{campo}').startAt('{valor}').once('value');"
            py_code = f"db.reference('{tabla}').order_by_child('{campo}').start_at('{valor}').get()"

    elif op == "GET_FILTER_MULTIPLE":
        filtro = nosql.get("filtro")
        operador_logico = filtro.get("operador_logico", "AND")
        condiciones = filtro.get("condiciones", [])
        conds_str = " && ".join([f"r.{c['campo']} {c['operador']} '{c['valor']}'" for c in condiciones])
        js_code = f"""// Múltiples condiciones ({operador_logico}). Filtrar en cliente:
const snap = await firebase.database().ref('{tabla}').once('value');
const registros = snap.val() || {{}};
const filtrados = Object.fromEntries(
    Object.entries(registros).filter(([id, r]) => {conds_str.replace(" && ", f" {'&&' if operador_logico == 'AND' else '||'} ")})
);"""
        py_code = f"""# Múltiples condiciones ({operador_logico}). Filtrar en cliente:
registros = db.reference('{tabla}').get() or {{}}
# Evaluar condiciones para cada registro
filtrados = {{k: v for k, v in registros.items() if cumple_condiciones(v)}}"""

    elif op == "SET":
        id_val = nosql.get("id")
        datos = nosql.get("datos")
        js_code = f"firebase.database().ref('{tabla}/{id_val}').set({datos});"
        py_code = f"db.reference('{tabla}/{id_val}').set({datos})"

    elif op == "SET_BATCH":
        js_code = f"""// Inserción masiva con update()
const registros = {{ id1: {{...}}, id2: {{...}} }};
firebase.database().ref('{tabla}').update(registros);"""
        py_code = f"""# Inserción masiva con update()
registros = {{'id1': {{...}}, 'id2': {{...}}}}
db.reference('{tabla}').update(registros)"""

    elif op == "DEL":
        id_val = nosql.get("id")
        js_code = f"firebase.database().ref('{tabla}/{id_val}').remove();"
        py_code = f"db.reference('{tabla}/{id_val}').delete()"

    elif op == "UPDATE":
        id_val = nosql.get("id")
        datos = nosql.get("datos")
        js_code = f"firebase.database().ref('{tabla}/{id_val}').update({datos});"
        py_code = f"db.reference('{tabla}/{id_val}').update({datos})"

    elif op == "DEL_FILTER":
        filtro = nosql.get("filtro")
        campo = filtro["campo"]
        operador = filtro["operador"]
        valor = filtro["valor"]
        js_code = f"""// Paso 1: Obtener todos los registros
const snap = await firebase.database().ref('{tabla}').once('value');
const registros = snap.val() || {{}};

// Paso 2: Filtrar por condición ({campo} {operador} '{valor}')
const idsEliminar = Object.keys(registros).filter(id => 
    registros[id].{campo} {operador} '{valor}'
);

// Paso 3: Eliminar cada registro
for (const id of idsEliminar) {{
    await firebase.database().ref('{tabla}/' + id).remove();
}}"""
        py_code = f"""# Paso 1: Obtener todos los registros
registros = db.reference('{tabla}').get() or {{}}

# Paso 2: Filtrar por condición ({campo} {operador} '{valor}')
ids_eliminar = [k for k, v in registros.items() if v.get('{campo}') {operador} '{valor}']

# Paso 3: Eliminar cada registro
for id_reg in ids_eliminar:
    db.reference(f'{tabla}/{{id_reg}}').delete()"""

    elif op == "DEL_FILTER_MULTIPLE":
        filtro = nosql.get("filtro")
        operador_logico = filtro.get("operador_logico", "AND")
        js_code = f"""// Paso 1: Obtener todos los registros
const snap = await firebase.database().ref('{tabla}').once('value');
const registros = snap.val() || {{}};

// Paso 2: Evaluar múltiples condiciones ({operador_logico})
const idsEliminar = Object.keys(registros).filter(id => {{
    const r = registros[id];
    // Evaluar condiciones con {operador_logico}
    return cumpleCondiciones(r);
}});

// Paso 3: Eliminar cada registro
for (const id of idsEliminar) {{
    await firebase.database().ref('{tabla}/' + id).remove();
}}"""
        py_code = f"""# Paso 1: Obtener todos los registros
registros = db.reference('{tabla}').get() or {{}}

# Paso 2: Evaluar múltiples condiciones ({operador_logico})
ids_eliminar = [k for k, v in registros.items() if cumple_condiciones(v)]

# Paso 3: Eliminar cada registro
for id_reg in ids_eliminar:
    db.reference(f'{tabla}/{{id_reg}}').delete()"""

    elif op == "UPDATE_FILTER":
        filtro = nosql.get("filtro")
        datos = nosql.get("datos")
        campo = filtro["campo"]
        operador = filtro["operador"]
        valor = filtro["valor"]
        js_code = f"""// Paso 1: Obtener todos los registros
const snap = await firebase.database().ref('{tabla}').once('value');
const registros = snap.val() || {{}};

// Paso 2: Filtrar por condición ({campo} {operador} '{valor}')
const idsActualizar = Object.keys(registros).filter(id => 
    registros[id].{campo} {operador} '{valor}'
);

// Paso 3: Actualizar cada registro
for (const id of idsActualizar) {{
    await firebase.database().ref('{tabla}/' + id).update({datos});
}}"""
        py_code = f"""# Paso 1: Obtener todos los registros
registros = db.reference('{tabla}').get() or {{}}

# Paso 2: Filtrar por condición ({campo} {operador} '{valor}')
ids_actualizar = [k for k, v in registros.items() if v.get('{campo}') {operador} '{valor}']

# Paso 3: Actualizar cada registro
for id_reg in ids_actualizar:
    db.reference(f'{tabla}/{{id_reg}}').update({datos})"""

    elif op == "UPDATE_FILTER_MULTIPLE":
        filtro = nosql.get("filtro")
        datos = nosql.get("datos")
        operador_logico = filtro.get("operador_logico", "AND")
        js_code = f"""// Paso 1: Obtener todos los registros
const snap = await firebase.database().ref('{tabla}').once('value');
const registros = snap.val() || {{}};

// Paso 2: Evaluar múltiples condiciones ({operador_logico})
const idsActualizar = Object.keys(registros).filter(id => {{
    const r = registros[id];
    return cumpleCondiciones(r);
}});

// Paso 3: Actualizar cada registro
for (const id of idsActualizar) {{
    await firebase.database().ref('{tabla}/' + id).update({datos});
}}"""
        py_code = f"""# Paso 1: Obtener todos los registros
registros = db.reference('{tabla}').get() or {{}}

# Paso 2: Evaluar múltiples condiciones ({operador_logico})
ids_actualizar = [k for k, v in registros.items() if cumple_condiciones(v)]

# Paso 3: Actualizar cada registro
for id_reg in ids_actualizar:
    db.reference(f'{tabla}/{{id_reg}}').update({datos})"""

    else:
        js_code = "// Operación no soportada"
        py_code = "# Operación no soportada"

    return {
        "javascript": js_code,
        "python": py_code
    }

