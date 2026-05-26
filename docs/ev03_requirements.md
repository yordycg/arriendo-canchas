# 📝 Evaluación Sumativa - Desarrollo de Proyecto Web
## Framework Django + Base de Datos MySQL

### 📋 Descripción de la evaluación
La presente evaluación tiene como finalidad que los y las estudiantes desarrollen un proyecto web funcional utilizando el framework `Django` y base de datos `MySQL`, integrando los contenidos trabajados durante la asignatura.

El proyecto deberá evidenciar el desarrollo de una solución completa considerando:
- **Backend**.
- **Base de datos**.
- **Interfaz web**.
- **Consumo de API**.
- **Auditoría de accesos**.
- **Documentación técnica**.
- **Diseño responsivo**.

El sistema debe ser completamente funcional y orientado a resolver una problemática real o simulada.

### 🎯 Objetivo de la evaluación
Implementar un sistema web funcional utilizando `Django` y `MySQL`, aplicando autenticación, manejo de datos, consumo de API, interfaz responsiva y documentación técnica del desarrollo.

### 🛠️ Tecnologías obligatorias

| Tecnología | Uso requerido |
| :--- | :--- |
| **Python** | Lenguaje de programación |
| **Django** | Framework principal |
| **MySQL** | Base de datos |
| **Bootstrap** | Diseño responsivo |
| **SweetAlert** | Alertas visuales |
| **API REST** | Consumo de información externa o interna |

---

## 🚀 Requerimientos obligatorios del sistema

### 1. Sistema de Login con Auditoría
El sistema debe permitir autenticación de usuarios mediante login. Además, deberá registrar una auditoría de acceso almacenando:

| Campo | Descripción |
| :--- | :--- |
| `username` | Usuario ingresado |
| `fechaHora` | Fecha y hora del intento |
| `estadoLogin` | Correcto o Incorrecto |
| `passwordIngresada` | **Solo cuando el acceso sea incorrecto** |

**Consideraciones importantes:**
- [ ] La auditoría debe almacenarse en `MySQL`.
- [ ] El registro debe realizarse automáticamente.
- [ ] Debe existir evidencia funcional durante la presentación.

### 2. Desarrollo de 5 funcionalidades principales
El proyecto debe incluir al menos **5 funcionalidades** o módulos funcionales completos. Cada funcionalidad debe contemplar lógica de negocio, interfaz gráfica y persistencia de datos.

**Ejemplo: Módulo de Ventas**
- [ ] Registro de ventas.
- [ ] Selección de productos.
- [ ] Cálculo automático de totales.
- [ ] Validación de stock.
- [ ] Registro detalle de venta.
- [ ] Historial de ventas.
- [ ] Confirmaciones con `SweetAlert`.

### 3. Consumo de API
El proyecto debe consumir al menos una API. Ejemplos:
- [ ] **API de moneda**: Conversión de divisas.
- [ ] **API clima**: Temperatura por ciudad.
- [ ] **API regiones y comunas**: Carga dinámica.
- [ ] **API propia**: CRUD desde servicios `REST`.

### 4. Uso obligatorio de SweetAlert
- [ ] Confirmaciones.
- [ ] Mensajes de éxito.
- [ ] Eliminaciones.
- [ ] Errores.
- [ ] Validaciones.
- [ ] Login.

### 5. Uso obligatorio de Bootstrap
- [ ] Menú de navegación.
- [ ] Formularios responsivos.
- [ ] Tablas responsivas.
- [ ] Diseño visual coherente.
- [ ] Uso correcto de grillas y componentes.

---

## 📖 6. Manual de desarrollo (Documentación)
Se debe entregar un manual técnico en formato **PDF** o **Word** que contenga:

1. **Portada**: Nombre del proyecto, Integrantes, Asignatura, Fecha.
2. **Introducción**: Descripción general del sistema.
3. **Objetivo del sistema**: Finalidad del proyecto.
4. **Tecnologías utilizadas**: Explicación de herramientas.
5. **Arquitectura del sistema**: Funcionamiento general.
6. **Modelo de base de datos**: Diagrama Entidad-Relación, tablas y relaciones.
7. **Instalación del proyecto**: Configuración de entorno, dependencias, MySQL y migraciones.
8. **Explicación de funcionalidades**: Capturas de pantalla y descripción.
9. **Consumo de API**: Explicación de integración.
10. **Auditoría de login**: Explicación técnica y evidencia.
11. **Conclusión**: Reflexión final.

---

## 📦 Entregables

| Archivo | Formato |
| :--- | :--- |
| **Proyecto Django** | Carpeta comprimida `.zip` / `.rar` |
| **Base de datos** | Archivo `.sql` |
| **Manual de desarrollo** | `PDF` o `Word` |
| **Presentación** | `PPT` o `PDF` |

---

## 📅 Presentación del proyecto
Durante las **semanas 14 y 15** se realizará la presentación formal. Cada grupo deberá:
- Mostrar funcionamiento completo.
- Explicar arquitectura y base de datos.
- Evidenciar auditoría y consumo de API.
- Responder preguntas técnicas.

---

## 📊 Ponderación de evaluación

| Ítem | Porcentaje | Descripción |
| :--- | :--- | :--- |
| **Proyecto funcional** | **70%** | Desarrollo e implementación en `Django` + `MySQL`, API, Auditoría, UI y Manual. |
| **Presentación** | **30%** | Exposición, dominio técnico y demostración funcional. |

---

## 📝 Escala de evaluación - Proyecto (70%)

| Criterio | Logrado (100%) | Medianamente (70%) | En vías (50%) | No logrado (0%) |
| :--- | :--- | :--- | :--- | :--- |
| **Django** (10 pts) | Estructura y rutas correctas. | Detalles menores. | Errores de organización. | No implementa/Graves errores. |
| **MySQL** (10 pts) | Conexión y persistencia OK. | Detalles menores. | Errores en CRUD. | No funcional. |
| **Auditoría** (15 pts) | Login + Auditoría completa. | Incompleta/Errores. | Información parcial. | No implementa. |
| **Funciones** (25 pts) | 5 módulos completos. | Errores menores. | Incompletos. | Insuficientes. |
| **API** (10 pts) | Integración funcional. | Detalles menores. | Errores de integración. | No implementa. |
| **SweetAlert** (5 pts) | Uso correcto en todo. | Mayoría de acciones. | Uso limitado. | No implementa. |
| **Bootstrap** (5 pts) | Responsivo y ordenado. | Mayormente responsivo. | Problemas visuales. | Desorden significativo. |
| **Manual** (20 pts) | Completo y técnico. | Pequeños faltantes. | Falta claridad. | Insuficiente. |

---

## 🎤 Escala de evaluación - Presentación (30%)

| Criterio | Logrado | Medianamente | En vías | No logrado |
| :--- | :--- | :--- | :--- | :--- |
| **Claridad** (20 pts) | Fluida y técnica. | Mínimas dificultades. | Desordenado. | Confuso/Incompleto. |
| **Demostración** (25 pts) | Sin errores visibles. | Errores menores. | Fallas frecuentes. | No logra demostrar. |
| **Base de Datos** (15 pts) | Tablas/Relaciones OK. | Mayoría OK. | Vacíos técnicos. | No explica. |
| **API** (10 pts) | Integración técnica OK. | Pequeños errores. | Dificultades técnicas. | No explica. |
| **Auditoría** (15 pts) | Evidencia completa. | Información parcial. | Funcionamiento parcial. | Sin evidencia. |
| **Dominio** (15 pts) | Amplio y justifica. | Buen dominio. | Dificultades al responder. | Sin dominio. |