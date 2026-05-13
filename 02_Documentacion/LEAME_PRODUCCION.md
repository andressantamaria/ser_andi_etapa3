# Guía Rápida - Producción Masiva de Documentos

## Problema Resuelto

**ANTES:** Generar 25 documentos requería diligenciar el formulario 25 veces manualmente (25-40 minutos).

**AHORA:** Un solo comando genera los 25 documentos automáticamente (5-10 minutos).

---

## Uso Básico

### Opción 1: Script Directo (Recomendado)

```bash
# 1. Activar entorno virtual
source venv/bin/activate

# 2. Ejecutar generación de 25 documentos
python generacion_masiva.py
```

**Resultado:**
- 25 PDFs generados en `pdfs/`
- Reporte JSON en `pdfs/reporte_lote_[fecha].json`
- Logs en `sistema.log`

---

### Opción 2: API REST

```bash
# 1. Iniciar servidor
python app.py

# 2. Verificar estado
curl http://localhost:5000/api/estado-sistema

# 3. Generar 25 documentos
curl -X POST http://localhost:5000/api/generacion-masiva \
  -H "Content-Type: application/json" \
  -d '{"tipo_proceso": "practica_profesional", "es_remunerada": "si", "limite": 25}'
```

---

## Estructura de Archivos

```
Proyecto1/
├── generacion_masiva.py       # Módulo de producción masiva
├── app.py                     # API con endpoint /generacion-masiva
├── agente_final.py            # Generación individual
├── pdfs/                      # PDFs generados
│   ├── certificado_*.pdf
│   └── reporte_lote_*.json    # Reportes de lote
└── sistema.log                # Logs del sistema
```

---

## Comandos Útiles

### Verificar estado del sistema
```bash
python -c "from generacion_masiva import GeneradorMasivo; g = GeneradorMasivo(); print(f'Estudiantes: {len(g.obtener_todos_estudiantes())}'); print(f'Empresas: {len(g.obtener_todas_empresas())}')"
```

### Generar 25 documentos
```bash
python generacion_masiva.py
```

### Generar lote personalizado
```bash
python -c "
from generacion_masiva import GeneradorMasivo
g = GeneradorMasivo()
g.procesar_todos_estudiantes(limite=10)
"
```

---

## Solución de Problemas

### Error: "No hay estudiantes registrados"
**Solución:** El script crea automáticamente 25 estudiantes de ejemplo si no hay suficientes.

### Error: "No hay empresas registradas"
**Solución:** El script crea automáticamente 5 empresas de ejemplo si no hay suficientes.

### Error: "Ollama no está disponible"
**Solución:**
```bash
# Verificar si Ollama está corriendo
ollama list

# Iniciar Ollama si es necesario
ollama serve
```

---

## Métricas

| Concepto | Valor |
|----------|-------|
| Tiempo por documento | ~15-30 seg |
| Tiempo para 25 docs | 5-10 min |
| Tasa de éxito típica | 90-100% |
| Espacio requerido | ~50MB para 25 PDFs |

---

## Archivos Generados

| Archivo | Descripción |
|---------|-------------|
| `pdfs/certificado_[CEDULA].pdf` | Documento PDF individual |
| `pdfs/reporte_lote_[TIMESTAMP].json` | Reporte consolidado del lote |
| `sistema.log` | Logs detallados del proceso |

---

## Siguientes Pasos

1. **Ejecutar prueba:** `python generacion_masiva.py`
2. **Verificar PDFs:** Revisar carpeta `pdfs/`
3. **Revisar reporte:** Abrir `pdfs/reporte_lote_*.json`
4. **Validar documentos:** Abrir PDFs generados

---

*Documento de referencia rápida para producción masiva*

*Última actualización: Mayo 2026*
