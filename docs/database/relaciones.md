# Relaciones de la Base de Datos

Detalle de las relacciones entre las entidades del sistema de arriendo de canchas (y quinchos).

## 1. Relaciones Uno a Muchos (1:N)

_Es la relación más común, donde un registro de una tabla puede estar relacionado con muchos de otra._

| Tabla A (1)             | Tabla B (N)                | Descripción                                                              |
| :---------------------- | :------------------------- | :----------------------------------------------------------------------- |
| **tipo_canchas**        | **canchas**                | Un tipo de cancha (Futbol) puede tener muchas canchas físicas.           |
| **tipo_canchas**        | **torneos**                | Un torneo se juega específicamente en un tipo de cancha.                 |
| **estado_reservas**     | **reservas_canchas**       | Un estado (Pagada) puede aplicarse a múltiples reservas.                 |
| **estado_reservas**     | **reservas_quinchos**      | Similar a canchas, gestiona el flujo de pago/cancelación.                |
| **canchas**             | **reservas_canchas**       | Una cancha específica puede tener muchas reservas a lo largo del tiempo. |
| **quinchos**            | **reservas_quinchos**      | Un quincho puede ser arrendado muchas veces.                             |
| **estado_usuarios**     | **usuarios**               | Un estado (Activo/Bloqueado) aplica a muchos usuarios.                   |
| **roles**               | **usuarios**               | Un rol (Admin/Cliente) es compartido por varios usuarios.                |
| **membresias**          | **usuarios**               | Muchos usuarios pueden tener el mismo nivel de membresía (VIP).          |
| **usuarios**            | **reservas_canchas**       | Un usuario puede realizar múltiples reservas de canchas.                 |
| **usuarios**            | **reservas_quinchos**      | Un usuario puede realizar múltiples reservas de quinchos.                |
| **usuarios**            | **equipos**                | Un usuario puede ser capitán de varios equipos.                          |
| **usuarios**            | **usuario_penalizaciones** | Un usuario puede acumular varias penalizaciones en su historial.         |
| **tipo_penalizaciones** | **usuario_penalizaciones** | Un tipo de multa (No show) se aplica a muchos usuarios.                  |
| **torneos**             | **partidos**               | Un torneo se compone de muchos partidos programados.                     |
| **reservas_canchas**    | **partidos**               | Una reserva de cancha puede estar vinculada a un partido de torneo.      |
| **equipos**             | **partidos**               | Un equipo juega muchos partidos (como Equipo 1 o Equipo 2).              |

## 2. Relaciones Muchos a Muchos (N:M)

_Ocurre cuando muchos registros de una tabla se relacionan con muchos de otra. Requiere una tabla intermedia._

### usuarios <---> equipos

- **Tabla Intermedia:** `equipo_usuarios`
- **Lógica:** Un usuario puede pertenecer a varios equipos, y un equipo está compuesto por varios usuarios.

## 3. Relaciones Uno a Uno (1:1)

_En este diseño actual, no se han definido relaciones 1:1 obligatorias, ya que se prefiere la flexibilidad de 1:N._
_(Nota: El Capitán de un equipo se maneja como 1:N porque un usuario puede ser capitán de varios equipos distintos)._

## 4. Resumen de Integridad Referencial (FKs)

- **Recomendacion:** Se recomienda usar `PROTECT` en la mayoría de las FKs de configuración (como roles o tipos de cancha) para evitar borrar datos que dejen registros huérfanos.
- **Auditoría:** Todas las tablas de relación cuentan con `created_at` y `updated_at` para trazabilidad.
