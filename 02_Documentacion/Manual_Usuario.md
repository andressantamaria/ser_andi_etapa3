# Manual de Usuario - Sistema de Gestión Documental

## 1. Introducción
Este sistema permite la generación automatizada de documentos legales (convenios de práctica, pasantías y otrosí) de la Universidad EAFIT. El sistema utiliza inteligencia artificial para normalizar los datos capturados y asegurar la precisión en la generación de PDFs.

## 2. Cómo ingresar al sistema
Para utilizar el sistema, es necesario tener el servidor de la aplicación en ejecución:

1.  **Iniciar el servidor:**
    - Abra una terminal en la carpeta raíz del proyecto.
    - Ejecute el comando: `python app.py`
    - El servidor se iniciará en `http://localhost:5000`.

2.  **Abrir la interfaz:**
    - Abra el archivo `01_Repositorio/formulario_eafit.html` en su navegador web preferido.

## 3. Cómo usar la solución
El flujo de trabajo para generar un documento es el siguiente:

1.  **Diligenciamiento:** Complete las 7 secciones del formulario web.
2.  **Búsqueda Rápida:**
    - Utilice el botón "Buscar Estudiante" ingresando la cédula para autocompletar sus datos.
    - Utilice el botón "Buscar Organización" ingresando el NIT para autocompletar los datos de la empresa.
3.  **Envío:** Haga clic en el botón "Enviar Solicitud" al finalizar.
4.  **Procesamiento:** El sistema procesará los datos mediante IA y generará un archivo PDF en la carpeta `pdfs/`.
5.  **Resultado:** Una notificación le confirmará el éxito de la operación y el nombre del archivo generado.

## 4. Funcionalidades principales
*   **Autocompletado inteligente:** Búsqueda en tiempo real de estudiantes y empresas registradas en la base de datos local.
*   **Normalización de datos mediante IA:** El sistema corrige automáticamente formatos inconsistentes (fechas, direcciones, valores monetarios).
*   **Generación de documentos PDF:** Creación automática basada en plantillas oficiales de la Universidad EAFIT.
*   **Trazabilidad:** Registro automático de todos los documentos generados en el historial del sistema.
*   **Modo Oscuro/Claro:** Interfaz adaptable a las preferencias visuales del usuario.

## 5. Casos de uso
| Caso de Uso | Descripción |
| :--- | :--- |
| **Práctica Profesional** | Generación de convenios para prácticas obligatorias (remuneradas o no). |
| **Pasantía** | Generación de acuerdos para experiencias laborales tempranas. |
| **Otrosí (Modificación)** | Generación de documentos para cambios en convenios existentes (prórrogas, cambios de valor). |
| **Generación Masiva** | Procesamiento automático de múltiples documentos a partir de la base de datos. |

## 6. Errores comunes y recomendaciones
| Error | Causa Probable | Recomendación |
| :--- | :--- | :--- |
| **"Estudiante no encontrado"** | La cédula no existe en la base de datos `gestion.db`. | Verifique que la cédula sea correcta o registre al estudiante primero. |
| **"Organización no encontrada"** | El NIT ingresado no está en la base de datos `gestion.db`. | Verifique el NIT o registre la organización primero. |
| **PDF con guiones bajos (___________)** | Faltaron datos obligatorios en el formulario. | Asegúrese de completar todos los campos marcados con asterisco (*). |
| **El servidor no responde** | `app.py` no está ejecutándose. | Ejecute `python app.py` en una terminal y manténgala abierta. |

---
*Para soporte técnico, contacte a: soporte@eafit.edu.co*
