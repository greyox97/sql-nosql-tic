import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate('credenciales-firebase.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://middleware-kv-default-rtdb.europe-west1.firebasedatabase.app/'
})

def set_usuario(tabla, id, data):
    """INSERT: Crea un nuevo registro. Falla si ya existe."""
    if not data:
        raise ValueError("El diccionario de datos está vacío.")
    ref = db.reference(f'{tabla}/{id}')
    
    # Verificar si ya existe
    if ref.get() is not None:
        raise ValueError(f"El registro con id '{id}' ya existe en '{tabla}'")
    
    ref.set(data)

def update_usuario(tabla, id, data):
    """UPDATE: Actualiza un registro existente. Falla si no existe."""
    if not data:
        raise ValueError("El diccionario de actualización está vacío.")
    ref = db.reference(f'{tabla}/{id}')
    
    # Verificar si existe
    if ref.get() is None:
        raise ValueError(f"El registro con id '{id}' no existe en '{tabla}'")
    
    ref.update(data)

def get_usuario(tabla, id):
    ref = db.reference(f'{tabla}/{id}')
    return ref.get()

def get_todos(tabla):
    ref = db.reference(tabla)
    return ref.get() or {}

def delete_usuario(tabla, id):
    ref = db.reference(f'{tabla}/{id}')
    # Verificar si existe antes de borrar
    if ref.get() is None:
        return False  # No existía
    ref.delete()
    return True  # Sí existía y se eliminó

def set_masivo(tabla, data_dict):
    """
    Insertar múltiples registros en una sola operación.
    data_dict: {id1: {campo1: val1, ...}, id2: {...}, ...}
    Falla si alguno de los IDs ya existe.
    """
    if not data_dict:
        raise ValueError("El diccionario de datos está vacío.")
    
    # Verificar si alguno ya existe
    existentes = get_todos(tabla) or {}
    duplicados = [id for id in data_dict.keys() if id in existentes]
    
    if duplicados:
        raise ValueError(f"Los siguientes registros ya existen: {duplicados[:5]}{'...' if len(duplicados) > 5 else ''}")
    
    ref = db.reference(tabla)
    ref.update(data_dict)

def get_filtrados_nativos(tabla, campo, operador, valor):
    """
    Ejecutar query de Firebase nativa para filtrar eficientemente.
    Retorna None si el operador no es soportado nativamente.
    """
    ref = db.reference(tabla)
    
    try:
        # Firebase solo soporta ciertos operadores nativamente con order_by_child
        if operador == "=":
            resultado = ref.order_by_child(campo).equal_to(valor).get()
        elif operador == ">=":
            resultado = ref.order_by_child(campo).start_at(valor).get()
        elif operador == ">":
            # Firebase no tiene "mayor que estricto", usar start_at y filtrar después
            return None
        elif operador == "<=":
            resultado = ref.order_by_child(campo).end_at(valor).get()
        elif operador == "<":
            # Firebase no tiene "menor que estricto", usar end_at y filtrar después
            return None
        else:
            # Operador no soportado nativamente
            return None
        
        # Firebase retorna None si no hay resultados
        return resultado if resultado else {}
        
    except Exception as e:
        # Si falla la query nativa, retornar None para fallback
        print(f"Error en query nativa: {e}")
        return None

def get_todos_ordenados(tabla, campo, direccion="ASC"):
    """
    Obtener todos los registros ordenados por un campo.
    Firebase siempre retorna en orden ASC, se invierte en memoria para DESC.
    """
    ref = db.reference(tabla)
    
    try:
        # Firebase ordena por el campo especificado (siempre ASC)
        resultado = ref.order_by_child(campo).get()
        
        if not resultado:
            return {}
        
        # Si es DESC, invertir el orden
        if direccion == "DESC":
            # Convertir a lista de tuplas, invertir, y volver a dict
            items = list(resultado.items())
            items.reverse()
            return dict(items)
        
        return resultado
        
    except Exception as e:
        # Si falla, retornar datos sin ordenar
        print(f"Error al ordenar: {e}")
        return ref.get() or {}
