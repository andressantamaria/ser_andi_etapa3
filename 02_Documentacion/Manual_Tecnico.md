# Manual Técnico - Sistema de Gestión Documental Inteligente

## 1. Introducción
Este documento detalla la arquitectura, configuración, despliegue y mantenimiento del sistema de generación documental automatizado basado en agentes inteligentes.

## 2. Requisitos Previos
*   **Lenguaje:** Python 3.12 o superior.
*   **IA:** Ollama (instalado y corriendo en el puerto predeterminado 11434).
*   **Entorno:** Entorno virtual de Python (`venv`).
*   **Librerías:** Consultar archivo `requirements.txt` (generar mediante `pip freeze > requirements.txt`).

## 3. Instalación y Configuración del Entorno
1.  **Clonar el repositorio:** `git clone [URL_REPO]`
2.  **Crear y activar el entorno virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```
3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configurar Ollama:** Asegúrese de tener el modelo base instalado:
    ```bash
    ollama pull granite4:micro-h
    ```

## 4. Variables de Entorno
El sistema requiere un archivo `.env` en la raíz con las siguientes variables:
*   `TELEGRAM_TOKEN`: (Si se usa el bot de Telegram).
*   `GOOGLE_API_KEY`: Para integraciones con Google.
*   `OPENROUTER_API_KEY`: Para servicios de IA externos (si aplica).

## 5. Arquitectura del Sistema
El sistema sigue un modelo híbrido:
- **Backend:** Flask (API REST para enrutamiento).
- **Cerebro (Agente):** `agente_final.py` (Lógica centralizada).
- **Inteligencia (LLM):** Ollama con modelo `granite4:micro-h` (Normalización y estructuración semántica).
- **Validación:** Pydantic (esquemas de datos).
- **Motor de Plantillas:** Jinja2 + Markdown.
- **Generador PDF:** WeasyPrint (HTML5/CSS a PDF).
- **Base de Datos:** SQLite (`gestion.db`).

## 6. Configuración de modelos IA
El modelo de lenguaje está configurado en `agente_final.py` mediante la librería `langchain_ollama`.
```python
# agente_final.py (Línea 47)
llm = ChatOllama(model="granite4:micro-h")
```

## 7. Consideraciones técnicas para mantenimiento
- **Logs:** El sistema registra eventos y errores en `sistema.log` (formato: `%(asctime)s - %(levelname)s - %(message)s`).
- **Base de Datos:** SQLite (`gestion.db`) es auto-contenida. Para respaldos, simplemente copie el archivo `.db`.
- **Plantillas:** Las plantillas se encuentran en `01_Repositorio/datos/`. Cualquier cambio en el formato de los documentos debe reflejarse en los archivos `.md` correspondientes utilizando la sintaxis Jinja2 (`{{ variable }}`).
- **Despliegue:** Para producción, se recomienda encapsular la aplicación Flask con un servidor WSGI (ej. Gunicorn) y asegurar que el servicio de Ollama esté siempre corriendo como un daemon del sistema.
