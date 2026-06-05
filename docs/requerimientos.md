# Especificación de Requerimientos Funcionales

Este documento detalla las capacidades que debe poseer el sistema de Arriendo de Canchas.

## 1. Gestión de Usuarios y Acceso (App: `users`)

| ID | Requerimiento | Descripción | Acceso |
| :--- | :--- | :--- | :--- |
| **RF-01** | Identificación por RUT | El sistema debe usar el RUT como identificador primario y validar su formato. | Público |
| **RF-02** | Registro de Invitados | Permitir registrar usuarios (RUT/Nombre) sin correo ni clave para participar en equipos. | Admin |
| **RF-03** | Seguridad de Acceso | Bloquear cuenta tras 3 intentos fallidos de inicio de sesión. | Público |
| **RF-04** | Roles de Sistema | Definir permisos según rol: Admin, Recepcionista, Cliente e Invitado. | Sistema |

## 2. Membresías y Beneficios (App: `memberships`)

| ID | Requerimiento | Descripción | Acceso |
| :--- | :--- | :--- | :--- |
| **RF-05** | Niveles de Socio | Gestionar categorías: Normal (0%), VIP (15%) y Socio (30% de descuento). | Admin |
| **RF-06** | Aplicación de Descuentos | Calcular automáticamente el precio final basado en la membresía del usuario. | Sistema |

## 3. Infraestructura (Apps: `courts` / `pavilions`)

| ID | Requerimiento | Descripción | Acceso |
| :--- | :--- | :--- | :--- |
| **RF-07** | Atributos de Canchas | Definir superficie (Pasto, Arcilla, etc.) y tipo de recinto (Abierto, Cerrado). | Admin |
| **RF-08** | Restricción VIP Quinchos | Limitar la reserva de ciertos quinchos solo a usuarios con membresía VIP o Socio. | Cliente |

## 4. Reservas (App: `bookings`)

| ID | Requerimiento | Descripción | Acceso |
| :--- | :--- | :--- | :--- |
| **RF-09** | Prevención de Sobrecupo | Impedir más de una reserva para el mismo recurso, fecha y hora. | Cliente |
| **RF-10** | Cancelación Flexible | Permitir cancelar sin multa hasta 60 min antes (30 min para nivel VIP/Socio). | Cliente |

## 5. Penalizaciones (App: `penalties`)

| ID | Requerimiento | Descripción | Acceso |
| :--- | :--- | :--- | :--- |
| **RF-11** | Registro de Faltas | Registrar inasistencias y cancelaciones fuera de plazo. | Sistema |
| **RF-12** | Escala Progresiva | Aplicar recargos (50%/100%) según el número de faltas acumuladas. | Sistema |
| **RF-13** | Bloqueo por Reincidencia | Impedir nuevas reservas a usuarios con 5 o más faltas activas. | Cliente |

## 6. Torneos (App: `tournaments`)

| ID | Requerimiento | Descripción | Acceso |
| :--- | :--- | :--- | :--- |
| **RF-14** | Gestión de Equipos | Permitir la creación de equipos vinculados a un Capitán responsable. | Cliente |
| **RF-15** | Regla de Walkover | En caso de inasistencia, registrar resultado 3-0 y penalizar al capitán. | Admin |
