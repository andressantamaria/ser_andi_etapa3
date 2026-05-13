#Nombre proyecto: 
    Nodo (NOrmalización DOcumental)

#Integrantes:
    

# Proyecto de Automatización de Documentos con Agentes LLM

Este proyecto es un experimento para automatizar la generación de documentos (como cartas de práctica) utilizando un flujo de agentes que combinan LLMs locales (Ollama), bases de datos SQL y motores de renderizado de documentos.

## Arquitectura general:

    ### 1. Núcleo del Sistema (Orquestación)
    * **`agente_final.py`**: Es el **Orquestador Principal**. Contiene la lógica que conecta la base de datos, el   
    LLM   de Ollama y el motor de PDFs. Es el cerebro que ejecuta el pipeline completo.

    ### 2. Base de Datos y Datos
    * **`gestion.db`**: El archivo de base de datos **SQLite** que contiene las tablas `estudiantes` y `empresas`.
    * **`crear_db.py`**: Script de inicialización que creó la estructura y los datos de prueba en `gestion.db`.

    ### 3. Sistema de Documentos (Plantillas)
    * **`datos/`**: Carpeta contenedora del RAG (Repositorio de Documentos).
    * **`carta_practica.md`**: Plantilla **Markdown** que contiene la estructura del documento y las etiquetas de   
    Jinja2 (`{{ ... }}`) que serán rellenadas.

    ### 4. Herramientas de Prueba y Diagnóstico
    * **`test_pdf.py`**: Script de prueba para validar que el motor de renderizado (Jinja2 + WeasyPrint)        
    funcione           correctamente.
    * **`test_sql_agent.py`**: Script de prueba para validar la conexión y generación de consultas SQL mediante     el      modelo local.
* **`NoDo.py`**: Script de prueba inicial para validar la conexión con Ollama.

### 5. Configuración y Entorno
* **`.env`**: Archivo que almacena credenciales (tokens).
* **`bot.py`**: Bot de Telegram (proyecto original).
* **`venv/`**: Carpeta del entorno virtual con todas las librerías instaladas.

## Pipeline del Proyecto (Flujo de trabajo)

Cuando ejecutas `agente_final.py`:

1. **Entrada (Input):** Recibe la `cédula` del estudiante.
2. **Extracción (SQL):** Consulta `gestion.db` para obtener los datos crudos.
3. **Inteligencia (LLM/Granite):** Llama a `Ollama` (`granite4:micro`) para convertir los datos crudos en un JSON limpio (datos estructurados).
4. **Renderizado (Jinja2):** Toma la plantilla en `datos/carta_practica.md` e inyecta el JSON usando Jinja2.
5. **Exportación (WeasyPrint):** El motor convierte el resultado final en un archivo PDF (ej. `certificado_1.pdf`).
