# Informe Técnico Final: Motor Documental Inteligente - EAFIT

## 1. Contexto del Reto
El proyecto nace en el marco del RETO2 de la Universidad EAFIT, cuyo objetivo es la automatización de la generación de documentos legales y de vinculación para prácticas profesionales y pasantías. El objetivo fue transformar un proceso manual de alta carga administrativa en un sistema ágil, escalable e inteligente.

## 2. Definición del Problema
Anteriormente, el personal administrativo debía diligenciar manualmente múltiples campos en un formulario y generar documentos uno a uno.
- **Tiempo:** 25-40 minutos por lote de 25 documentos.
- **Error humano:** Tasa de error estimada del 15% debido a la naturaleza repetitiva y manual de la tarea.
- **Escalabilidad:** Limitada, al depender totalmente de la capacidad humana.

## 3. Justificación de la Solución
Se implementó una solución híbrida que combina **IA (LLM)** para la normalización de lenguaje natural con **componentes deterministas** (Python, Jinja2, Pydantic, WeasyPrint) para asegurar la integridad legal y el formato de los documentos. La IA aporta la flexibilidad necesaria para interpretar datos no estructurados, mientras que el código determinista garantiza resultados legales exactos.

## 4. Metodología de Desarrollo
Se siguió un enfoque ágil iterativo:
1. **Análisis:** Modelado de los 11 anexos y acuerdos de pasantía.
2. **Prototipado:** Desarrollo del motor básico de renderizado (Jinja2 + WeasyPrint).
3. **Agente de IA:** Integración de LangChain + Ollama (Granite 3.1) para normalización de datos.
4. **Validación:** Implementación de esquemas Pydantic para garantizar la calidad del JSON generado por la IA.
5. **Optimización:** Refinamiento mediante *prompt engineering* y pruebas de latencia.

## 5. Arquitectura Técnica
El sistema opera en 4 capas:
1. **Presentación:** Formulario web (HTML5, JS, CSS).
2. **Backend API:** Servidor Flask.
3. **Orquestación:** Agente inteligente (`agente_final.py`) que coordina: LLM (normalización), Pydantic (validación), Jinja2 (renderizado), WeasyPrint (PDF).
4. **Datos:** SQLite (historial, empresas, estudiantes).

## 6. Flujo de Datos
`Usuario` -> `Frontend` -> `API Flask` -> `Orquestador (Agente Final)` -> `Base de Datos/LLM` -> `PDF` -> `Registro Histórico`.

## 7. Componentes Técnicos
- **Base de Datos:** SQLite (`gestion.db`).
- **APIs/Modelos:**
    - API: Flask.
    - LLM: `granite4:micro-h` (vía Ollama).
    - PDF: WeasyPrint (HTML5 a PDF).
- **IA:** LangChain como interfaz de orquestación, Pydantic para validación de estructura de datos no estructurados.

## 8. Resultados Obtenidos
- **Eficiencia:** Reducción del tiempo de generación para 25 documentos de ~30 min a ~5-10 min.
- **Fiabilidad:** Tasa de error < 2% (gracias a validación Pydantic + mapeo determinista).
- **Escalabilidad:** Implementación de generación masiva (`generacion_masiva.py`).

## 9. Dificultades Encontradas
- **Latencia:** El uso de un LLM local generaba tiempos de espera altos (~18s por documento).
- **Optimización de Modelo:** Se intentó implementar el modelo más pequeño (`ibm/granite4:350m-h`) para mejorar la velocidad. Si bien la latencia bajó a ~3s, el modelo **perdía contexto** en datos complejos, fallando en un 20% de las validaciones de esquema (generando valores `None` o JSON malformado).
- **Solución Final:** Se mantuvo el modelo robusto (`granite4:micro-h`) y se optimizó el *prompt* mediante técnicas de "Few-Shot" y mapeo explícito en Python para eliminar la carga inferencial del LLM.

## 10. Conclusiones
La combinación de IA para la interpretación semántica y código determinista para la ejecución es la arquitectura óptima para procesos documentales legales. La IA resuelve la rigidez del algoritmo tradicional sin comprometer la seguridad jurídica que brinda la ejecución determinista.

## 11. Recomendaciones
- **Infraestructura:** Migrar la inferencia del modelo a una GPU dedicada para eliminar los tiempos de latencia del LLM en entornos de producción.
- **Escalabilidad:** Implementar colas de trabajo (Celery/Redis) para el procesamiento masivo de documentos.
- **Monitorización:** Implementar un sistema de logging más robusto centralizado para la trazabilidad de documentos masivos.
