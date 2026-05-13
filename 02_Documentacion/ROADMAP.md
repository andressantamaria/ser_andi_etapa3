# Roadmap de Estabilización y Mejoras - Sistema EAFIT

Este documento detalla las próximas fases para llevar el sistema de automatización documental de un experimento funcional (MVP) a un sistema robusto preparado para producción.

## Fases de Mejora

### 1. Sistema de Auditoría y Logs (Trazabilidad)
* **Objetivo:** Registrar cada evento crítico para diagnóstico inmediato.
* **Acciones:**
    * Implementar la librería `logging` de Python.
    * Configurar un archivo `sistema.log` que capture errores de validación, fallos de Ollama y éxitos de generación.
    * Añadir niveles de severidad (INFO, WARNING, ERROR).

### 2. Feedback de UI en Tiempo Real
* **Objetivo:** Mejorar la experiencia del usuario (UX) durante el procesamiento.
* **Acciones:**
    * Modificar `formulario_eafit.html` (JavaScript) para mostrar un estado de "Procesando..." o un spinner mientras la API trabaja.
    * Deshabilitar el botón de envío durante la carga para evitar peticiones duplicadas.

### 3. Externalización de Prompts (Mantenibilidad)
* **Objetivo:** Separar las instrucciones de la IA del código fuente.
* **Acciones:**
    * Crear una carpeta `/prompts/`.
    * Mover los prompts de `agente_final.py` a archivos `.txt` individuales (ej. `prompt_convenio.txt`, `prompt_otrosi.txt`).
    * Actualizar el orquestador para que lea estos archivos antes de llamar a Ollama.

### 4. Validación de Integridad Post-Render
* **Objetivo:** Garantizar la calidad del documento final.
* **Acciones:**
    * Añadir una validación post-renderizado en `agente_final.py`: verificar si el archivo PDF existe y si su tamaño es mayor a 0 antes de retornar la confirmación al usuario.
    * Implementar una limpieza automática de PDFs temporales (ej. > 24 horas) para optimizar el almacenamiento.

---
*Este plan establece la ruta para garantizar la estabilidad, la mantenibilidad y la fiabilidad del sistema a largo plazo.*
