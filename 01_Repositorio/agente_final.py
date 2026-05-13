import sqlite3
import json
import os
import logging
from langchain_ollama import ChatOllama
from jinja2 import Environment, FileSystemLoader
from markdown_it import MarkdownIt
from weasyprint import HTML
from pydantic import BaseModel, ValidationError
from typing import Union, List, Optional

# Configuración de Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='sistema.log')

# Definición de modelos de validación
class DatosConvenio(BaseModel):
    nombre_representante_organizacion: Optional[str] = None
    cedula_representante_organizacion: Optional[str] = None
    cargo_representante_organizacion: Optional[str] = None
    nombre_organizacion: Optional[str] = None
    nit_organizacion: Optional[str] = None
    nombre_estudiante: Optional[str] = None
    cedula_estudiante: Optional[str] = None
    programa_estudiante: Optional[str] = None
    direccion_organizacion: Optional[str] = None
    actividades_lista: Optional[Union[str, List[Union[str, dict]]]] = None
    fecha_inicio: Optional[str] = None
    fecha_fin: Optional[str] = None

    def get_actividades_string(self):
        if not self.actividades_lista: return ""
        if isinstance(self.actividades_lista, list):
            items = [str(next(iter(i.values())) if isinstance(i, dict) else i) for i in self.actividades_lista]
            return "\n".join([f"{i+1}. {a}" for i, a in enumerate(items)])
        return str(self.actividades_lista)

# Configuración del LLM
llm = ChatOllama(model="granite4:micro-h")
md = MarkdownIt()

def seleccionar_plantilla(form_data):
    tipo = form_data.get('tipoProceso')
    if tipo == 'practica_profesional':
        return 'datos/ANEXO_02.md' if form_data.get('esRemunerada') == 'si' else 'datos/ANEXO_04.md'
    elif tipo == 'pasantia': return 'datos/ACUERDO_PASANTIA_UNIVERSIDAD_EMPRESA.md'
    elif tipo == 'otrosi': return 'datos/OTROSÍ_GENERICO.md'
    return 'datos/carta_practica.md'

def buscar_estudiante(cedula):
    conn = sqlite3.connect('../05_Datasets/gestion.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, carrera FROM estudiantes WHERE id = ?", (cedula,))
    data = cursor.fetchone()
    conn.close()
    return {"nombre": data[0], "carrera": data[1]} if data else None

# Registro de documentos
def registrar_documento(cedula, tipo, ruta):
    conn = sqlite3.connect('../05_Datasets/gestion.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO historial_documentos (cedula, tipo, ruta) VALUES (?, ?, ?)", (cedula, tipo, ruta))
    conn.commit()
    conn.close()

def numero_a_letras(numero_str):
    try:
        n = int(numero_str.replace(",", "").replace(".", ""))
        if n == 0: return "cero"
        unidades = ["", "un", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez", "once", "doce", "trece", "catorce", "quince", "dieciséis", "diecisiete", "dieciocho", "diecinueve"]
        decenas = ["", "", "veinte", "treinta", "cuarenta", "cincuenta", "sesenta", "setenta", "ochenta", "noventa"]
        centenas = ["", "ciento", "doscientos", "trescientos", "cuatrocientos", "quinientos", "seiscientos", "setecientos", "ochocientos", "novecientos"]
        def convertir_tres_digitos(num):
            if num == 0: return ""
            if num < 20: return unidades[num]
            if num < 100:
                d, u = divmod(num, 10)
                return decenas[d] + (" y " + unidades[u] if u else "")
            c, r = divmod(num, 100)
            return (centenas[c] if c != 1 else "cien") + (" " + convertir_tres_digitos(r) if r else "")
        res = ""
        if n >= 1000000:
            millones = n // 1000000
            res += (convertir_tres_digitos(millones) if millones != 1 else "un") + " millón "
            n %= 1000000
        if n >= 1000:
            miles = n // 1000
            res += (convertir_tres_digitos(miles) if miles != 1 else "") + " mil "
            n %= 1000
        res += convertir_tres_digitos(n)
        return res.strip()
    except: return "valor no definido"

def generar_documento_desde_formulario(form_data):
    cedula = form_data.get('cedulaEstudiante')
    estudiante_db = buscar_estudiante(cedula)
    if not estudiante_db:
        return {"success": False, "mensaje": "Estudiante no encontrado."}

    ruta_plantilla = seleccionar_plantilla(form_data)
    datos_completos = {**form_data, **estudiante_db}
    
    prompt = f"""
    Extrae la información de los siguientes datos para llenar el esquema solicitado.
    Datos: {datos_completos}
    Esquema JSON:
    {{
        "nombre_representante_organizacion": "string|null",
        "cedula_representante_organizacion": "string|null",
        "cargo_representante_organizacion": "string|null",
        "nombre_organizacion": "string|null",
        "nit_organizacion": "string|null",
        "nombre_estudiante": "string|null",
        "cedula_estudiante": "string|null",
        "programa_estudiante": "string|null",
        "direccion_organizacion": "string|null",
        "actividades_lista": "string|null",
        "fecha_inicio": "string|null",
        "fecha_fin": "string|null"
    }}
    Responde SOLO con el JSON válido. Si falta un dato, pon 'null'.
    """
    
    try:
        response = llm.invoke(prompt)
        json_str = response.content.replace("```json", "").replace("```", "").strip()
        datos_json = json.loads(json_str)
        datos_validados = DatosConvenio.model_validate(datos_json)
        datos_finales = datos_validados.model_dump()
        datos_finales['actividades_lista'] = datos_validados.get_actividades_string()
        
        # Mapeo determinístico
        datos_finales['nombre_representante_organizacion'] = form_data.get('representanteLegal') or datos_finales.get('nombre_representante_organizacion')
        datos_finales['nombre_organizacion'] = form_data.get('nombreOrganizacion') or datos_finales.get('nombre_organizacion')
        datos_finales['nit_organizacion'] = form_data.get('nit') or datos_finales.get('nit_organizacion')
        datos_finales['nombre_estudiante'] = form_data.get('nombreEstudiante') or datos_finales.get('nombre_estudiante')
        datos_finales['direccion_organizacion'] = form_data.get('direccionOrganizacion') or datos_finales.get('direccion_organizacion')
        
        auxilio = form_data.get('valorAuxilio', '0')
        datos_finales['auxilio_numeros'] = f"{int(auxilio):,}"
        datos_finales['auxilio_letras'] = numero_a_letras(auxilio)
        
        for k, v in datos_finales.items():
            if v is None or v == "" or v == "None": datos_finales[k] = "___________"
    except Exception as e:
        return {"success": False, "mensaje": str(e)}

    # Renderizado
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(BASE_DIR))
    
    # Convertir Markdown a HTML
    contenido_markdown = env.get_template(ruta_plantilla).render(datos_finales)
    contenido_html = md.render(contenido_markdown)
    
    # Inyectar en base HTML
    html_content = env.get_template('plantilla_base.html').render(content=contenido_html)
    
    archivo_salida = os.path.join('pdfs', f"certificado_{cedula}.pdf")
    HTML(string=html_content, base_url='.').write_pdf(archivo_salida)
    
    registrar_documento(cedula, form_data.get('tipoProceso'), archivo_salida)
    return {"success": True, "ruta": archivo_salida}
