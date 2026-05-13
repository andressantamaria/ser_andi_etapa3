# Funcionamiento del Ecosistema - Motor Documental Inteligente

## Visión General del Sistema

Este documento explica explícitamente cómo funciona todo el ecosistema, el agente inteligente involucrado, sus módulos deterministas de soporte, y las ventajas de esta solución híbrida (IA + determinista) frente a un algoritmo tradicional de impresión de plantillas.

---

## 1. Arquitectura General del Sistema

El sistema sigue una arquitectura en capas con un agente inteligente central y módulos de soporte:

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CAPA DE PRESENTACIÓN                        │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  formulario_eafit.html (Frontend - HTML/CSS/JS)             │   │
│  │  - Captura y validación de datos                            │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                │ POST JSON
                                ↓
┌─────────────────────────────────────────────────────────────────────┐
│                         CAPA DE APLICACIÓN                          │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  app.py (API Flask - Backend)                               │   │
│  │  - Orquestación de peticiones y respuestas                  │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ↓
┌─────────────────────────────────────────────────────────────────────┐
│                  CAPA DE ORQUESTACIÓN Y PROCESAMIENTO               │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  agente_final.py (Orquestador: 1 Agente LLM + 8 módulos)    │   │
│  │  - 1. Agente LLM (IA: Normalización y Estructuración)       │   │
│  │  - 2. Módulos deterministas (Validación, Renderizado, etc.) │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ↓
┌─────────────────────────────────────────────────────────────────────┐
│                         CAPA DE DATOS                               │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │
│  │  SQLite DB       │  │  Plantillas MD   │  │  Template Base   │  │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. Componentes del Sistema: Agente Inteligente y Módulos de Soporte

El sistema está compuesto por una serie de módulos deterministas y un núcleo inteligente basado en un LLM.

### 2.1 Módulo de Interfaz (formulario_eafit.html)
**(Determinista)** Captura datos del usuario y los envía al backend.

### 2.2 Módulo de API (app.py)
**(Determinista)** Recibe solicitudes HTTP y coordina el flujo.

### 2.3 Módulo de Validación de Base de Datos
**(Determinista)** Verifica la existencia de estudiantes y empresas en SQLite.

### 2.4 Módulo de Selección de Plantilla
**(Determinista)** Define la plantilla MD a utilizar basada en el tipo de trámite.

### 2.5 Agente LLM de Extracción de Datos (IA)

**Ubicación:** `agente_final.py` (líneas 110-121)

**Función Principal:** Usar IA para estructurar datos dispersos en un JSON coherente.

**Modelo:** `granite4:micro-h` (via Ollama local)

**Responsabilidades:**
- ✅ Normalizar semánticamente los datos
- ✅ Adaptar el output al esquema solicitado

*(Resto de componentes en `agente_final.py` como Validación Pydantic, Renderizado Jinja2, Generación PDF WeasyPrint y Registro Histórico SQLite funcionan de manera determinista)*

---

## 3. Ventajas de la Solución Híbrida (IA + Determinista)

### 3.1 Comparación de Enfoques

| Característica | Solución Agéntica (IA) | Algoritmo Tradicional |
|----------------|----------------------|---------------------|
| **Flexibilidad** | ✅ Alta - se adapta a variaciones | ❌ Baja - requiere estructura fija |
| **Robustez** | ✅ Alta - la IA maneja el ruido | ❌ Baja - el código falla con cambios |
| **Mantenimiento** | ✅ Bajo - menos código, más contexto | ❌ Alto - alta fragilidad |

---

## 5. Resumen Ejecutivo

### 5.1 Componentes del Sistema

| Tipo | Módulo | Función |
|---|--------|---------|
| Determinista | Interfaz | Captura datos usuario |
| Determinista | API | Enruta solicitudes HTTP |
| Determinista | Validación BD | Verifica existencia en SQLite |
| Determinista | Selección Plantilla | Decide qué plantilla usar |
| **IA** | **Agente LLM** | **Normaliza y estructura datos con IA** |
| Determinista | Pydantic | Valida esquema JSON |
| Determinista | Renderizado | Inyecta datos en plantilla |
| Determinista | PDF | Genera archivo PDF |
| Determinista | Historial | Registra en bitácora |

---
*Documento elaborado para el Sistema de Gestión de Prácticas Profesionales - Universidad EAFIT*
*Última actualización: Mayo 2026*
