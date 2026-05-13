# Manual de Usuario - Sistema de Gestión de Prácticas Profesionales

## Universidad EAFIT - Sistema de Generación Documental

---

## Tabla de Contenido

1. [Introducción](#1-introducción)
2. [Requisitos Previos](#2-requisitos-previos)
3. [Instalación y Configuración](#3-instalación-y-configuración)
4. [Inicio del Sistema](#4-inicio-del-sistema)
5. [Uso del Formulario](#5-uso-del-formulario)
6. [Tipos de Documentos](#6-tipos-de-documentos)
7. [Preguntas Frecuentes](#7-preguntas-frecuentes)
8. [Solución de Problemas](#8-solución-de-problemas)
9. [Soporte Técnico](#9-soporte-técnico)

---

## 1. Introducción

### 1.1 ¿Qué es este sistema?

El **Sistema de Gestión de Prácticas Profesionales** es una plataforma automatizada que genera documentos oficiales para prácticas profesionales y pasantías de la Universidad EAFIT. Utiliza inteligencia artificial para completar automáticamente la información en plantillas estandarizadas.

### 1.2 Características Principales

- ✅ Generación automática de PDFs oficiales
- ✅ Búsqueda automática de estudiantes y empresas
- ✅ Plantillas predefinidas según tipo de documento
- ✅ Validación de datos en tiempo real
- ✅ Historial de documentos generados
- ✅ Interfaz adaptable (modo claro/oscuro)

### 1.3 Tipos de Documentos Soportados

| Documento | Descripción |
|-----------|-------------|
| **Anexo 02** | Convenio de práctica profesional remunerada |
| **Anexo 04** | Convenio de práctica profesional no remunerada |
| **Acuerdo de Pasantía** | Convenio universidad-empresa para pasantías |
| **Otrosí** | Modificación a convenios existentes |
| **Carta de Práctica** | Constancia básica de práctica |

---

## 2. Requisitos Previos

### 2.1 Requisitos del Sistema

| Componente | Versión Mínima |
|------------|----------------|
| Python | 3.8+ |
| Navegador Web | Chrome 90+, Firefox 88+, Edge 90+ |
| Conexión a Internet | Requerida (para LLM local) |
| Espacio en Disco | 500 MB mínimo |

### 2.2 Dependencias Instaladas

El sistema incluye las siguientes librerías:
- Flask (servidor web)
- LangChain (orquestación de IA)
- Ollama (modelo LLM local)
- Jinja2 (plantillas)
- WeasyPrint (generación PDF)
- Pydantic (validación de datos)
- SQLite (base de datos)

---

## 3. Instalación y Configuración

### 3.1 Verificar Instalación

1. Abra una terminal en la carpeta del proyecto:
```bash
cd /home/sonoman/Documentos/Proyecto1
```

2. Verifique que el entorno virtual esté activo:
```bash
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows
```

3. Confirme que las dependencias estén instaladas:
```bash
pip list | grep -E "flask|langchain|ollama|jinja2|weasyprint"
```

### 3.2 Configurar Base de Datos

La base de datos `gestion.db` debe contener al menos:

**Tabla: estudiantes**
```sql
CREATE TABLE estudiantes (
    id INTEGER PRIMARY KEY,
    nombre TEXT,
    carrera TEXT,
    email TEXT,
    direccion TEXT
);
```

**Tabla: empresas**
```sql
CREATE TABLE empresas (
    id INTEGER PRIMARY KEY,
    nombre TEXT,
    rubro TEXT,
    contacto TEXT,
    representante_legal TEXT,
    direccion TEXT,
    cedula_representante TEXT,
    cargo_representante TEXT
);
```

### 3.3 Verificar Ollama

El sistema requiere Ollama instalado localmente:

```bash
# Verificar si Ollama está corriendo
ollama list

# El modelo debe estar disponible
ollama show granite4:micro-h
```

---

## 4. Inicio del Sistema

### 4.1 Iniciar el Servidor

1. Abra una terminal en la carpeta del proyecto
2. Active el entorno virtual (si aplica)
3. Ejecute:

```bash
python app.py
```

4. Verá el siguiente mensaje:
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

### 4.2 Acceder al Formulario

1. Abra su navegador web preferido
2. Navegue a: `http://localhost:5000/formulario_eafit.html`
3. El formulario cargará en la navegador

**Nota:** Si el puerto 5000 está ocupado, el sistema usará otro puerto automáticamente.

---

## 5. Uso del Formulario

### 5.1 Estructura del Formulario

El formulario está dividido en **7 secciones**:

```
┌─────────────────────────────────────────┐
│ 1. Datos de Clasificación               │
│ 2. Datos de la Organización             │
│ 3. Datos del Estudiante                 │
│ 4. Condiciones de la Práctica           │
│ 5. Responsables de Supervisión          │
│ 6. Contenido Formativo                  │
│ 7. Gestión Documental                   │
└─────────────────────────────────────────┘
```

### 5.2 Paso a Paso

#### **Paso 1: Datos de Clasificación**

| Campo | Opciones | Descripción |
|-------|----------|-------------|
| Tipo de Proceso | Práctica Profesional / Pasantía / Otrosí | Seleccione el tipo de documento |
| ¿Es Remunerada? | Sí / No | Define si hay auxilio económico |
| Responsable ARL | Organización / Universidad | Quien cubre ARL |
| Tipo de Pasantía | Interna / Externa con pago / Externa con facturación | Solo si aplica |

#### **Paso 2: Datos de la Organización**

| Campo | Descripción |
|-------|-------------|
| Nombre de la Organización | Razón social completa |
| NIT | Número de identificación tributaria |
| Representante Legal | Nombre completo |
| Cédula | Documento del representante |
| Cargo del Firmante | Ej: Gerente, Director |
| Dirección | Ubicación donde se desarrolla la práctica |

**💡 Función de Búsqueda:**
- Digite el NIT en el campo correspondiente
- Presione el botón **"Buscar Organización"**
- El sistema completará automáticamente los campos disponibles

#### **Paso 3: Datos del Estudiante**

| Campo | Descripción |
|-------|-------------|
| Nombre Completo | Identificación exacta para el diploma |
| Cédula de Ciudadanía | Número y lugar de expedición |
| Programa Académico | Carrera que cursa |
| Domicilio | Dirección de residencia |

**💡 Función de Búsqueda:**
- Digite la cédula en el campo correspondiente
- Presione el botón **"Buscar Estudiante"**
- El sistema completará nombre, programa y domicilio

#### **Paso 4: Condiciones de la Práctica**

| Campo | Descripción |
|-------|-------------|
| Fecha de Inicio | Día de inicio de actividades |
| Fecha de Fin | Día de finalización |
| Intensidad Horaria | Horas semanales (1-48) |
| Modalidad | Presencial / Híbrida / Virtual |
| Valor del Auxilio | Monto mensual en números |

#### **Paso 5: Responsables de Supervisión**

| Campo | Descripción |
|-------|-------------|
| Tutor (Empresa) | Nombre del jefe inmediato |
| Cédula del Tutor | Documento del tutor |
| Monitor (Universidad) | Nombre del asesor EAFIT |
| Cédula del Monitor | Documento del monitor |

#### **Paso 6: Contenido Formativo**

| Campo | Descripción |
|-------|-------------|
| Actividades | Liste entre 4 y 8 actividades que desarrollará el estudiante |

**Ejemplo:**
```
1. Desarrollo de aplicaciones web
2. Pruebas unitarias y de integración
3. Documentación técnica
4. Reuniones de seguimiento ágil
```

#### **Paso 7: Gestión Documental**

Cargue los siguientes documentos en PDF:

| Documento | Requisitos |
|-----------|------------|
| Certificado de Existencia | Máximo 90 días de antigüedad |
| RUT Actualizado | Año actual o anterior |
| Cédula del Representante | Documento escaneado |

### 5.3 Enviar Solicitud

1. Complete todos los campos obligatorios (marcados con `*`)
2. Revise que la información sea correcta
3. Presione **"Enviar Solicitud"**
4. Espere la confirmación del sistema

**Mensaje de Éxito:**
```
✓ PDF 'pdfs/certificado_XXXXXX.pdf' generado exitosamente.
```

**Mensaje de Error:**
```
✗ Error: [descripción del problema]
```

---

## 6. Tipos de Documentos

### 6.1 Anexo 02 - Práctica Remunerada

**Se usa cuando:**
- El estudiante recibe auxilio económico
- La práctica es profesional (no pasantía)

**Campos requeridos:**
- Todos los datos del estudiante
- Datos completos de la organización
- Fechas y valor del auxilio

### 6.2 Anexo 04 - Práctica No Remunerada

**Se usa cuando:**
- No hay auxilio económico
- La práctica es profesional

**Campos requeridos:**
- Todos los datos del estudiante
- Datos completos de la organización
- Fechas (valor en $0)

### 6.3 Acuerdo de Pasantía

**Se usa cuando:**
- El documento es una pasantía (no práctica profesional)
- Puede ser interna o externa

**Campos requeridos:**
- Tipo de pasantía seleccionado
- Datos de supervisión completos

### 6.4 Otrosí Genérico

**Se usa cuando:**
- Se modifica un convenio existente
- Cambios de fechas, valores o condiciones

**Campos adicionales:**
- Número de otrosí
- Fecha del convenio original
- Motivo del cambio

---

## 7. Preguntas Frecuentes

### 7.1 ¿El sistema funciona sin internet?

**Parcialmente.** El LLM (Ollama) funciona localmente, pero requiere que el modelo esté previamente descargado.

### 7.2 ¿Cuánto tarda en generarse un PDF?

**Tiempo promedio:** 10-30 segundos, dependiendo de:
- Velocidad del equipo
- Complejidad del documento
- Disponibilidad del LLM

### 7.3 ¿Dónde se guardan los PDF generados?

En la carpeta `pdfs/` dentro del proyecto:
```
/home/sonoman/Documentos/Proyecto1/pdfs/certificado_[CEDULA].pdf
```

### 7.4 ¿Puedo modificar las plantillas?

**Sí.** Las plantillas están en `/datos/`:
- `ANEXO_02.md`
- `ANEXO_04.md`
- `ACUERDO_PASANTIA_UNIVERSIDAD_EMPRESA.md`
- `OTROSÍ_GENERICO.md`
- `carta_practica.md`

**Formato:** Markdown con variables Jinja2 `{{ variable }}`

### 7.5 ¿Cómo agrego más estudiantes o empresas?

```bash
# Opción 1: Usando SQLite CLI
sqlite3 gestion.db "INSERT INTO estudiantes (id, nombre, carrera, email, direccion) VALUES (3, 'Nuevo Estudiante', 'Ingeniería', 'nuevo@email.com', 'Calle 123');"

# Opción 2: Usando Python
python -c "
import sqlite3
conn = sqlite3.connect('gestion.db')
cursor = conn.cursor()
cursor.execute('INSERT INTO estudiantes VALUES (?, ?, ?, ?, ?)', (3, 'Nuevo Estudiante', 'Ingeniería', 'nuevo@email.com', 'Calle 123'))
conn.commit()
conn.close()
"
```

### 7.6 ¿Puedo generar documentos en lote?

**Actualmente:** No. El sistema genera documentos de uno en uno.

**Próximamente:** Función de generación masiva (25 documentos).

---

## 8. Solución de Problemas

### 8.1 Error: "Estudiante no encontrado"

**Causa:** La NIT digitado no existe en la base de datos.

**Solución:**
1. Verifique que el NIT sea correcto
2. Confirme que la empresa esté registrada en `gestion.db`
3. Si no existe, agréguela (ver Pregunta 7.5)

### 8.2 Error: "Organización no encontrada"

**Causa:** La cédula digitada no existe en la base de datos.

**Solución:**
1. Verifique que la cédula sea correcta
2. Confirme que el estudiante esté registrado
3. Si no existe, agréguelo (ver Pregunta 7.5)

### 8.3 Error: "Error en la validación de datos"

**Causa:** El LLM no pudo generar un JSON válido.

**Solución:**
1. Revise que todos los campos estén completos
2. Verifique que Ollama esté corriendo
3. Reinicie el servidor Flask

### 8.4 Error: "No se puede conectar con Ollama"

**Causa:** El servicio Ollama no está disponible.

**Solución:**
```bash
# Verificar si Ollama está corriendo
ollama list

# Iniciar Ollama si no está activo
ollama serve

# Verificar que el modelo esté instalado
ollama show granite4:micro-h

# Si no existe, instálelo
ollama pull granite4:micro-h
```

### 8.5 Error: "El puerto 5000 ya está en uso"

**Causa:** Otra aplicación está usando el puerto 5000.

**Solución:**
```python
# En app.py, cambie la línea final:
app.run(debug=True, port=5001)  # Use otro puerto
```

### 8.6 Error: "No se genera el PDF"

**Causa:** Problema con WeasyPrint o las plantillas.

**Solución:**
1. Verifique que `plantilla_base.html` exista
2. Confirme que la carpeta `/datos/` tenga las plantillas
3. Revise el archivo `sistema.log` para más detalles

### 8.7 Error: "Error crítico en servidor"

**Causa:** Error no controlado en el backend.

**Solución:**
1. Revise `sistema.log` para el error específico
2. Verifique que la base de datos no esté corrupta
3. Reinicie el servidor Flask
4. Si persiste, contacte al soporte técnico

---

## 9. Soporte Técnico

### 9.1 Archivos de Log

El sistema genera dos archivos de registro:

| Archivo | Descripción |
|---------|-------------|
| `sistema.log` | Logs de la aplicación Flask |
| `pdfs/` | PDFs generados con historial |

### 9.2 Contactos de Soporte

| Concepto | Contacto |
|----------|---------|
| Soporte Técnico | soporte@eafit.edu.co |
| Mesa de Ayuda TI | mesadeayuda@eafit.edu.co |
| Coordinación Prácticas | practicas@eafit.edu.co |

### 9.3 Información Adicional

| Recurso | Ubicación |
|---------|-----------|
| README del Proyecto | `/README.md` |
| Respuestas RETO2 | `/respuestas.md` |
| Roadmap | `/ROADMAP.md` |
| Documentación | `/Documentos.md` |

---

## Anexo A: Comandos Útiles

### Verificar estado del sistema

```bash
# Verificar Python
python --version

# Verificar dependencias
pip list | grep -E "flask|langchain|ollama|jinja2|weasyprint"

# Verificar Ollama
ollama list

# Verificar base de datos
sqlite3 gestion.db "SELECT * FROM estudiantes LIMIT 5;"
sqlite3 gestion.db "SELECT * FROM empresas LIMIT 5;"

# Verificar logs
tail -f sistema.log
```

### Reiniciar servicios

```bash
# Detener Flask (Ctrl + C en la terminal)

# Reiniciar Ollama
ollama serve

# Iniciar Flask
python app.py
```

---

## Anexo B: Flujo del Sistema

``
┌─────────────────────────────────────────────────────────────┐
│ 1. Usuario diligencia formulario_eafit.html                 │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. app.py recibe datos y valida en SQLite                   │
│    - Busca estudiante por cédula                            │
│    - Busca empresa por NIT                                  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. agente_final.py selecciona plantilla según tipo          │
│    - ANEXO_02.md (remunerada)                               │
│    - ANEXO_04.md (no remunerada)                            │
│    - ACUERDO_PASANTIA.md                                    │
│    - OTROSÍ_GENERICO.md                                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. LLM (Ollama) genera JSON con datos estructurados         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. Pydantic valida datos contra modelo DatosConvenio        │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. Jinja2 renderiza plantilla Markdown con datos            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ 7. WeasyPrint convierte a PDF                               │
│    - Guarda en pdfs/certificado_[CEDULA].pdf                │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────┐
│ 8. Registro en historial_documentos (SQLite)                │
└─────────────────────────────────────────────────────────────┘
``

---

## Historial de Versiones

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | Mayo 2026 | Versión inicial del manual |

---

*Documento elaborado para el Sistema de Gestión de Prácticas Profesionales - Universidad EAFIT*

*Última actualización: Mayo 2026*
