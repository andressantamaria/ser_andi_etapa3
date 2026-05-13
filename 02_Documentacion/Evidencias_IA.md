# Evidencias del uso de Inteligencia Artificial (RETO2 - EAFIT)

Este documento detalla el uso de herramientas de Inteligencia Artificial durante el desarrollo del sistema de gestión documental.

## 1. Herramientas y Modelos Utilizados
- **Modelos IA:** Gemini (modelos de Google), Kimi (modelo K2.6).
- **Entorno de Desarrollo:** `open-code` (CLI Agent).
- **Procesamiento de Lenguaje:** LangChain, Ollama (Granite 3.1).

## 2. Para qué se utilizó la IA
La IA fue el pilar fundamental en todo el ciclo de vida del desarrollo:
- **Diseño Arquitectónico:** Definición de la estructura de agentes (híbrida IA+determinista).
- **Desarrollo de Código:** Generación de estructuras de backend (Flask), validadores (Pydantic), y lógica de renderizado.
- **Frontend:** Desarrollo de la interfaz (`formulario_eafit.html`) utilizando Kimi K2.6 para estructurar los estilos y la lógica de validación AJAX.
- **Prompt Engineering:** Optimización del prompt del LLM para normalización de datos.
- **Documentación:** Generación y refinamiento de la documentación técnica y de usuario.

## 3. Tareas Resueltas por la IA vs. Tareas Desarrolladas Manualmente
- **Desarrolladas por IA:** Generación de boilerplate, refactorización de código, diseño de esquemas JSON, normalización de datos, redacción de documentos técnicos.
- **Desarrolladas manualmente:** Integración final de componentes, configuración del entorno local (SSH, Ollama), revisión de seguridad, pruebas de usuario final y despliegue del repositorio en GitHub.

## 4. Proceso de adopción
La adopción de herramientas de IA fue iterativa. Se comenzó con un enfoque puramente "agéntico" que demostró ser ineficiente por la complejidad de la lógica de negocio. Se refinó hacia un enfoque híbrido, donde la IA se utiliza para tareas de normalización semántica, mientras que las reglas de negocio estrictas son gestionadas por código determinista.

## 5. Reflexiones sobre la utilidad
- **Dificultades:** Gestionar los límites de contexto de los modelos más pequeños y asegurar que las instrucciones (prompts) fueran totalmente inequívocas para evitar alucinaciones.
- **Utilidad:** Consideramos que la IA es extremadamente útil como **acelerador de ingeniería**, pero requiere una supervisión humana constante para garantizar la integridad técnica. El mayor aprendizaje es que el humano actúa como *orquestador* de las capacidades de la IA.
