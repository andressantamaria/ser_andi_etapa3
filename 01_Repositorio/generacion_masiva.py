"""
Módulo de Generación Masiva de Documentos
Permite procesar múltiples documentos en lote automáticamente
"""

import sqlite3
import os
import logging
from datetime import datetime
from typing import List, Dict, Optional
from agente_final import generar_documento_desde_formulario, seleccionar_plantilla, buscar_estudiante
from jinja2 import Environment, FileSystemLoader
from langchain_ollama import ChatOllama
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

llm = ChatOllama(model="granite4:micro-h")


class GeneradorMasivo:
    """
    Generador de documentos en masa para prácticas profesionales.
    Procesa múltiples estudiantes/empresas en un solo lote.
    """
    
    def __init__(self):
        self.resultados = []
        self.errores = []
        self.procesados = 0
        self.fallos = 0
        
    def obtener_todos_estudiantes(self) -> List[Dict]:
        """Obtiene todos los estudiantes de la base de datos"""
        conn = sqlite3.connect('gestion.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nombre, carrera, email, direccion 
            FROM estudiantes 
            WHERE id NOT IN (
                SELECT DISTINCT cedula 
                FROM historial_documentos
            )
        """)
        estudiantes = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return estudiantes
    
    def obtener_todas_empresas(self) -> List[Dict]:
        """Obtiene todas las empresas de la base de datos"""
        conn = sqlite3.connect('gestion.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, rubro, contacto, representante_legal, direccion, cedula_representante, cargo_representante FROM empresas")
        empresas = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return empresas
    
    def crear_combinaciones(self, estudiantes: List[Dict], empresas: List[Dict]) -> List[Dict]:
        """
        Crea combinaciones estudiante-empresa para procesar.
        Estrategia: Producto cartesiano (todos con todos) o emparejamiento 1:1
        """
        combinaciones = []
        
        if len(empresas) == 0:
            logger.warning("No hay empresas registradas")
            return combinaciones
            
        # Si hay igual número, emparejar 1:1
        if len(estudiantes) == len(empresas):
            for i in range(len(estudiantes)):
                combinaciones.append({
                    'estudiante': estudiantes[i],
                    'empresa': empresas[i % len(empresas)]
                })
        else:
            # Producto cartesiano limitado
            for estudiante in estudiantes:
                for empresa in empresas:
                    combinaciones.append({
                        'estudiante': estudiante,
                        'empresa': empresa
                    })
        
        logger.info(f"Se crearon {len(combinaciones)} combinaciones estudiante-empresa")
        return combinaciones
    
    def generar_datos_ejemplo(self, estudiante: Dict, empresa: Dict, tipo_proceso: str = 'practica_profesional', 
                              es_remunerada: str = 'si') -> Dict:
        """
        Genera datos de ejemplo para un estudiante y empresa dados
        """
        fecha_inicio = datetime.now().strftime('%Y-06-01')
        fecha_fin = datetime.now().strftime('%Y-12-01')
        
        return {
            'tipoProceso': tipo_proceso,
            'esRemunerada': es_remunerada,
            'cedulaEstudiante': str(estudiante['id']),
            'nombreEstudiante': estudiante['nombre'],
            'programa_estudiante': estudiante.get('carrera', 'Ingeniería'),
            'nombreOrganizacion': empresa.get('nombre', 'Empresa S.A.'),
            'nit_organizacion': str(empresa.get('id', '900000000')),
            'nombre_representante_organizacion': empresa.get('representante_legal', 'Representante Legal'),
            'cedula_representante_organizacion': empresa.get('cedula_representante', '12345678'),
            'cargo_representante_organizacion': empresa.get('cargo_representante', 'Gerente'),
            'direccion_organizacion': empresa.get('direccion', 'Dirección principal'),
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'actividades_lista': '1. Desarrollo de actividades\n2. Seguimiento de proyectos',
            'auxilio_letras': 'UN MILLON',
            'auxilio_numeros': '1000000'
        }
    
    def procesar_lote(self, combinaciones: List[Dict], tipo_proceso: str = 'practica_profesional',
                      es_remunerada: str = 'si', limite: Optional[int] = None) -> Dict:
        """
        Procesa un lote de combinaciones estudiante-empresa
        
        Args:
            combinaciones: Lista de diccionarios con estudiante y empresa
            tipo_proceso: Tipo de documento a generar
            es_remunerada: Si es remunerada o no
            limite: Límite máximo de documentos a generar
            
        Returns:
            Diccionario con resultados del procesamiento
        """
        self.resultados = []
        self.errores = []
        self.procesados = 0
        self.fallos = 0
        
        total = limite if limite else len(combinaciones)
        logger.info(f"Iniciando procesamiento masivo de {total} documentos...")
        
        for i, combinacion in enumerate(combinaciones[:total]):
            estudiante = combinacion['estudiante']
            empresa = combinacion['empresa']
            
            logger.info(f"Procesando {i+1}/{total}: {estudiante['nombre']} - {empresa.get('nombre', 'N/A')}")
            
            try:
                # Generar datos de ejemplo
                datos = self.generar_datos_ejemplo(estudiante, empresa, tipo_proceso, es_remunerada)
                
                # Generar documento individual
                resultado = generar_documento_desde_formulario(datos)
                
                if resultado.get('success'):
                    self.resultados.append({
                        'estudiante': estudiante['nombre'],
                        'empresa': empresa.get('nombre', 'N/A'),
                        'ruta': resultado.get('ruta'),
                        'estado': 'exitoso'
                    })
                    self.procesados += 1
                    logger.info(f"✓ Documento {self.procesados} generado exitosamente")
                else:
                    self.errores.append({
                        'estudiante': estudiante['nombre'],
                        'empresa': empresa.get('nombre', 'N/A'),
                        'error': resultado.get('mensaje', 'Error desconocido')
                    })
                    self.fallos += 1
                    logger.error(f"✗ Error: {resultado.get('mensaje')}")
                    
            except Exception as e:
                self.errores.append({
                    'estudiante': estudiante['nombre'],
                    'empresa': empresa.get('nombre', 'N/A'),
                    'error': str(e)
                })
                self.fallos += 1
                logger.error(f"✗ Excepción: {str(e)}")
        
        # Generar reporte
        reporte = {
            'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_procesados': self.procesados,
            'total_fallos': self.fallos,
            'tasa_exito': round((self.procesados / (self.procesados + self.fallos) * 100), 2) if (self.procesados + self.fallos) > 0 else 0,
            'resultados': self.resultados,
            'errores': self.errores
        }
        
        # Guardar reporte
        self._guardar_reporte(reporte)
        
        return reporte
    
    def _guardar_reporte(self, reporte: Dict):
        """Guarda el reporte de procesamiento"""
        try:
            ruta_reporte = os.path.join('pdfs', f"reporte_lote_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            with open(ruta_reporte, 'w', encoding='utf-8') as f:
                json.dump(reporte, f, indent=2, ensure_ascii=False)
            logger.info(f"Reporte guardado en: {ruta_reporte}")
        except Exception as e:
            logger.error(f"Error guardando reporte: {e}")
    
    def procesar_todos_estudiantes(self, tipo_proceso: str = 'practica_profesional', 
                                   es_remunerada: str = 'si', limite: Optional[int] = None) -> Dict:
        """
        Procesa automáticamente todos los estudiantes con empresas disponibles
        
        Args:
            tipo_proceso: Tipo de documento
            es_remunerada: Si es remunerada
            limite: Límite de documentos
            
        Returns:
            Reporte del procesamiento
        """
        logger.info("Obteniendo estudiantes y empresas de la base de datos...")
        
        estudiantes = self.obtener_todos_estudiantes()
        empresas = self.obtener_todas_empresas()
        
        if not estudiantes:
            logger.error("No hay estudiantes para procesar")
            return {'error': 'No hay estudiantes registrados'}
        
        if not empresas:
            logger.error("No hay empresas registradas")
            return {'error': 'No hay empresas registradas'}
        
        logger.info(f"Encontrados {len(estudiantes)} estudiantes y {len(empresas)} empresas")
        
        combinaciones = self.crear_combinaciones(estudiantes, empresas)
        
        if not combinaciones:
            return {'error': 'No se pudieron crear combinaciones'}
        
        return self.procesar_lote(combinaciones, tipo_proceso, es_remunerada, limite)


def generar_25_documentos_ejemplo():
    """
    Función principal para generar 25 documentos de ejemplo.
    Crea automáticamente estudiantes y empresas si no existen.
    """
    logger.info("=" * 60)
    logger.info("INICIANDO GENERACIÓN MASIVA DE 25 DOCUMENTOS")
    logger.info("=" * 60)
    
    generador = GeneradorMasivo()
    
    # Verificar si hay suficientes estudiantes
    estudiantes = generador.obtener_todos_estudiantes()
    empresas = generador.obtener_todas_empresas()
    
    if len(estudiantes) < 25:
        logger.warning(f"Solo hay {len(estudiantes)} estudiantes. Se crearán 25 estudiantes de ejemplo...")
        _crear_estudiantes_ejemplo(25 - len(estudiantes))
        estudiantes = generador.obtener_todos_estudiantes()
    
    if len(empresas) < 5:
        logger.warning(f"Solo hay {len(empresas)} empresas. Se crearán 5 empresas de ejemplo...")
        _crear_empresas_ejemplo(5 - len(empresas))
        empresas = generador.obtener_todas_empresas()
    
    # Crear combinaciones para 25 documentos
    combinaciones = []
    for i in range(25):
        combinaciones.append({
            'estudiante': estudiantes[i % len(estudiantes)],
            'empresa': empresas[i % len(empresas)]
        })
    
    # Procesar lote
    reporte = generador.procesar_lote(combinaciones, limite=25)
    
    # Imprimir resumen
    print("\n" + "=" * 60)
    print("RESUMEN DE GENERACIÓN MASIVA")
    print("=" * 60)
    print(f"Fecha: {reporte['fecha']}")
    print(f"Total procesados: {reporte['total_procesados']}")
    print(f"Total fallidos: {reporte['total_fallos']}")
    print(f"Tasa de éxito: {reporte['tasa_exito']}%")
    print("=" * 60)
    
    if reporte['total_fallos'] > 0:
        print("\nERRORES:")
        for error in reporte['errores'][:5]:  # Mostrar primeros 5 errores
            print(f"  - {error['estudiante']} ({error['empresa']}): {error['error']}")
    
    print("\nDocumentos generados en: pdfs/")
    print("=" * 60)
    
    return reporte


def _crear_estudiantes_ejemplo(cantidad: int):
    """Crea estudiantes de ejemplo en la base de datos"""
    conn = sqlite3.connect('gestion.db')
    cursor = conn.cursor()
    
    carreras = ['Ingeniería de Sistemas', 'Ingeniería Industrial', 'Administración', 
                'Contaduría', 'Derecho', 'Economía', 'Medicina']
    
    for i in range(cantidad):
        id_est = 1000000 + i
        cursor.execute("""
            INSERT OR REPLACE INTO estudiantes (id, nombre, carrera, email, direccion)
            VALUES (?, ?, ?, ?, ?)
        """, (
            id_est,
            f'Estudiante Ejemplo {i+1}',
            carreras[i % len(carreras)],
            f'estudiante{i+1}@eafit.edu.co',
            f'Calle {i+1} #10-20, Medellín'
        ))
    
    conn.commit()
    conn.close()
    logger.info(f"{cantidad} estudiantes de ejemplo creados")


def _crear_empresas_ejemplo(cantidad: int):
    """Crea empresas de ejemplo en la base de datos"""
    conn = sqlite3.connect('gestion.db')
    cursor = conn.cursor()
    
    rubros = ['Tecnología', 'Servicios', 'Comercio', 'Industria', 'Finanzas']
    
    for i in range(cantidad):
        id_emp = 900000000 + i
        cursor.execute("""
            INSERT OR REPLACE INTO empresas (id, nombre, rubro, contacto, representante_legal, 
                                           direccion, cedula_representante, cargo_representante)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            id_emp,
            f'Empresa Ejemplo {i+1} S.A.S.',
            rubros[i % len(rubros)],
            f'contacto@empresa{i+1}.com',
            f'Representante Legal {i+1}',
            f'Carrera {i+1} #20-30, Bogotá',
            f'9876543{i}',
            'Gerente General'
        ))
    
    conn.commit()
    conn.close()
    logger.info(f"{cantidad} empresas de ejemplo creadas")


if __name__ == "__main__":
    generar_25_documentos_ejemplo()
