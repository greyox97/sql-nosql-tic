from flask import request, jsonify
from services.traductor_service import convertir_a_nosql, traducir_sql_a_kv, traducir_y_ejecutar, generar_firebase_queries

def procesar_consulta():
    try:
        data = request.get_json()
        
        # Validación 1: Payload vacío
        if not data:
            return jsonify({"error": "Payload JSON vacío"}), 400
        
        if "sql" not in data:
            return jsonify({"error": "Debes enviar 'sql' con la consulta SQL"}), 400
        
        original = data["sql"]
        
        # Validación 2: SQL vacío
        if not original or not original.strip():
            return jsonify({"error": "Consulta SQL vacía"}), 400
        
        interna = traducir_sql_a_kv(original)
        consulta_parseada = convertir_a_nosql(interna)
        resultado = traducir_y_ejecutar(original)
        firebase_queries = generar_firebase_queries(consulta_parseada)

        return jsonify({
            "original": original,
            "consulta_parseada": consulta_parseada,
            "firebase_queries": firebase_queries,
            "resultado": resultado
        })
    
    except ValueError as ve:
        return jsonify({
            "error": f"Error de validación: {str(ve)}"
        }), 400
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            "error": f"Error interno: {str(e)}"
        }), 500
