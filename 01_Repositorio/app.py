import logging
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
from agente_final import generar_documento_desde_formulario
from generacion_masiva import GeneradorMasivo

# Configuración de Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='sistema.log')

app = Flask(__name__)
CORS(app)

@app.route('/api/procesar-practica', methods=['POST'])
def procesar():
    datos = request.json
    logging.info(f"Datos crudos recibidos: {datos}")
    logging.info(f"Recibida solicitud para estudiante: {datos.get('cedulaEstudiante')}")
    try:
        resultado = generar_documento_desde_formulario(datos)
        status_code = 200 if resultado.get("success") else 400
        logging.info(f"Proceso finalizado con éxito: {resultado.get('success')}")
        return jsonify(resultado), status_code
    except Exception as e:
        logging.error(f"Error crítico en servidor: {str(e)}")
        return jsonify({"success": False, "mensaje": f"Error crítico: {str(e)}"}), 500

@app.route('/api/buscar-estudiante', methods=['POST'])
def buscar_estudiante_endpoint():
    datos = request.json
    cedula = datos.get('cedula')
    conn = sqlite3.connect('gestion.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, carrera, direccion FROM estudiantes WHERE id = ?", (cedula,))
    data = cursor.fetchone()
    conn.close()
    if data:
        return jsonify({"success": True, "datos": {"nombre": data[0], "carrera": data[1], "direccion": data[2]}})
    return jsonify({"success": False, "mensaje": "Estudiante no encontrado"})

@app.route('/api/buscar-organizacion', methods=['POST'])
def buscar_organizacion_endpoint():
    datos = request.json
    nit = datos.get('nit')
    conn = sqlite3.connect('gestion.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, representante_legal, cedula_representante, cargo_representante, direccion FROM empresas WHERE id = ?", (nit,))
    data = cursor.fetchone()
    conn.close()
    if data:
        return jsonify({"success": True, "datos": {
            "nombre": data[0],
            "representante_legal": data[1],
            "cedula_representante": data[2],
            "cargo_representante": data[3],
            "direccion": data[4]
        }})
    return jsonify({"success": False, "mensaje": "Organización no encontrada"})

@app.route('/api/generacion-masiva', methods=['POST'])
def generacion_masiva():
    """
    Endpoint para generación masiva de documentos
    Recibe: {"tipo_proceso": "practica_profesional", "es_remunerada": "si", "limite": 25}
    Retorna: Reporte de procesamiento masivo
    """
    datos = request.json
    tipo_proceso = datos.get('tipo_proceso', 'practica_profesional')
    es_remunerada = datos.get('es_remunerada', 'si')
    limite = datos.get('limite', 25)
    
    logging.info(f"Solicitud de generación masiva: {limite} documentos, tipo={tipo_proceso}")
    
    try:
        generador = GeneradorMasivo()
        reporte = generador.procesar_todos_estudiantes(tipo_proceso, es_remunerada, limite)
        return jsonify(reporte), 200
    except Exception as e:
        logging.error(f"Error en generación masiva: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/estado-sistema', methods=['GET'])
def estado_sistema():
    """Verifica el estado del sistema y base de datos"""
    conn = sqlite3.connect('gestion.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM estudiantes")
    total_estudiantes = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM empresas")
    total_empresas = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM historial_documentos")
    total_documentos = cursor.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        "estudiantes": total_estudiantes,
        "empresas": total_empresas,
        "documentos_generados": total_documentos,
        "listo_para_produccion": total_estudiantes > 0 and total_empresas > 0
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
