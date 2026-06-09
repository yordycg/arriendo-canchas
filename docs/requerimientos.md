# Especificación de Requerimientos Funcionales

Este documento detalla las capacidades del sistema de Arriendo de Canchas, sincronizado con la implementación final.

## 1. Gestión de Usuarios y Acceso

| ID | Requerimiento | Descripción | Acceso |
| :--- | :--- | :--- | :--- |
| **RF-01** | Identificación por RUT | El sistema usa el RUT como identificador primario y único. | Público |
| **RF-03** | Seguridad de Acceso | Bloqueo de cuenta tras 3 intentos fallidos de login (Auditoría incluida). | Público |
| **RF-04** | Roles de Sistema | Permisos diferenciados para Admin, Recepcionista y Cliente. | Sistema |
| **RF-16** | Sistema de Inactividad | Cierre de sesión automático tras 15 min de inactividad con alerta preventiva. | Sistema |

## 2. Membresías y Beneficios

| ID | Requerimiento | Descripción | Acceso |
| :--- | :--- | :--- | :--- |
| **RF-05** | Niveles de Socio | Gestión de planes: Normal, VIP y Socio con descuentos del 0%, 15% y 30%. | Admin |
| **RF-06** | Aplicación de Descuentos | Cálculo automático del precio final en el motor de reservas según membresía. | Sistema |

## 3. Infraestructura

| ID | Requerimiento | Descripción | Acceso |
| :--- | :--- | :--- | :--- |
| **RF-07** | Gestión Deportiva | Administración de Canchas (tipo, superficie, recinto) y Quinchos. | Admin |
| **RF-08** | Restricción VIP | Los Quinchos marcados como 'Solo VIP' solo pueden ser reservados por socios VIP. | Cliente |
| **RF-17** | Catálogo Informativo | Los clientes pueden explorar canchas y planes sin opciones de edición. | Cliente |

## 4. Reservas y Transacciones

| ID | Requerimiento | Descripción | Acceso |
| :--- | :--- | :--- | :--- |
| **RF-09** | Motor de Disponibilidad | Prevención de sobrecupo mediante validación de bloques horarios AJAX. | Cliente |
| **RF-10** | Cancelación Flexible | Cancelación sin multa hasta 60 min antes (30 min para VIP/Socio). | Cliente |
| **RF-18** | Formateo Monetario | Visualización estandarizada de montos en CLP ($XX.XXX) en todo el sitio. | Sistema |

## 5. Penalizaciones y Disciplina

| ID | Requerimiento | Descripción | Acceso |
| :--- | :--- | :--- | :--- |
| **RF-11** | Registro de Faltas | Registro de inasistencias y cancelaciones fuera de plazo. | Sistema |
| **RF-12** | Escala Progresiva | Aplicación de recargos (50% en 3ra falta, 100% en 5ta falta). | Sistema |
| **RF-13** | Bloqueo por Deuda | Impedir reservas a usuarios con 5 o más faltas vigentes. | Cliente |
| **RF-20** | Registro de No-show | Botón administrativo para marcar inasistencias y generar multas automáticas. | Admin |

## 6. Infraestructura de Software

| ID | Requerimiento | Descripción | Acceso |
| :--- | :--- | :--- | :--- |
| **RF-19** | Centralización de Activos | Uso de app 'core' para unificar UI, librerías y dashboards globales. | Sistema |
