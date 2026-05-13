# Evidencias del Proceso de Trabajo

Este documento consolida las decisiones técnicas, los problemas encontrados y el cronograma de ejecución del proyecto.

## 1. Roadmap y Cronograma
| Fase | Actividad | Estado |
|------|-----------|--------|
| **Estabilización** | Implementación de logs y validación. | Completado |
| **Optimización** | Benchmarking de modelos LLM y prompt engineering. | Completado |
| **Producción Masiva** | Creación del módulo de lotes. | Completado |
| **Refinamiento** | Corrección de errores en PDFs (None, números). | Completado |
| **Documentación** | Elaboración de informes finales. | En curso |

## 2. Decisiones Técnicas Tomadas
- **Arquitectura:** Se mantuvo el modelo híbrido (IA para interpretación + Python para lógica determinista), ya que probó ser más fiable que confiar toda la lógica al LLM.
- **Modelo LLM:** Se seleccionó `granite4:micro-h` tras comparar latencia y precisión contra `350m-h`. El modelo más pequeño mostró inestabilidad en el seguimiento de esquemas JSON complejos.
- **Mapeo de datos:** Se movió la lógica de formateo monetario y normalización de campos desde el LLM hacia funciones deterministas en Python (`agente_final.py`).
- **Renderizado:** Se integró `markdown-it` para asegurar que las negritas en los documentos PDF se rendericen correctamente sin mostrar asteriscos literales.

## 3. Problemas Encontrados y Soluciones

| Problema | Descripción | Solución |
|----------|-------------|----------|
| **Latencia elevada** | El modelo robusto tardaba ~18s por documento. | Optimización de prompts y exploración de modelos pequeños. |
| **Inestabilidad del LLM pequeño** | El modelo 350M generaba JSONs inválidos o con `None` en datos complejos. | Vuelta al modelo robusto + optimización del prompt mediante esquemas visuales. |
| **Formato de auxilio erróneo** | El LLM no transformaba números a letras correctamente. | Implementación de función determinista `numero_a_letras` en Python. |
| **Asteriscos en PDF** | El motor de renderizado mostraba `**nombre**` en lugar de **nombre**. | Integración de `markdown-it` para procesar Markdown a HTML previo al renderizado. |
| **Datos faltantes en PDF** | Aparición de literales "None" en documentos. | Implementación de sanitización de salida para reemplazar `None` por `___________`. |
