# Diccionario de Datos - Base de Datos (gestion.db)

El sistema utiliza una base de datos SQLite para gestionar la información de estudiantes, organizaciones y el historial de documentos generados.

## 1. Tabla: `estudiantes`
Almacena la información de los estudiantes de la universidad.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | INTEGER | Cédula del estudiante (PK) |
| `nombre` | TEXT | Nombre completo |
| `carrera` | TEXT | Programa académico |
| `email` | TEXT | Correo electrónico |
| `direccion` | TEXT | Domicilio |

## 2. Tabla: `empresas`
Almacena la información de las organizaciones aliadas.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | INTEGER | NIT de la empresa (PK) |
| `nombre` | TEXT | Razón social |
| `rubro` | TEXT | Sector económico |
| `contacto` | TEXT | Nombre de contacto |
| `representante_legal` | TEXT | Nombre completo del representante |
| `direccion` | TEXT | Ubicación de la práctica |
| `cedula_representante`| TEXT | Cédula del representante |
| `cargo_representante` | TEXT | Cargo del representante |

## 3. Tabla: `historial_documentos`
Almacena el rastro de todos los convenios/documentos generados.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | INTEGER | ID autoincremental (PK) |
| `cedula` | TEXT | Cédula del estudiante |
| `tipo` | TEXT | Tipo de proceso (práctica, pasantía, etc.) |
| `ruta` | TEXT | Ruta al archivo PDF generado |
| `fecha` | TIMESTAMP | Fecha/Hora de generación |

---
*Este diccionario sirve como referencia para el mantenimiento de la integridad de los datos en el sistema.*
