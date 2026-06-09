# Reglas de Negocio

## Canchas y Quinchos

1. Una "cancha" o "quincho" no puede ser "reservada" por mas de un "usuario" en el mismo bloque de fecha y hora. (Prevención de sobrecupo).
2. Los valores de arriendo por hora o reserva deben ser siempre mayores o iguales a cero.
3. **Consistencia Técnica:** El sistema no permite el registro de canchas con tipos de superficie o recinto fuera de los catálogos técnicos predefinidos (CHECK constraints).

## Reservas

1. Se puede "cancelar" una "reserva" sin penalización según el nivel de membresía:
   - **Cliente Normal:** Mínimo 60 minutos de anticipación.
   - **VIP / Socio:** Mínimo 30 minutos de anticipación.
   1.1 Si se cancela fuera de estos plazos, se asigna automáticamente una penalización al usuario.
2. El valor pagado registrado en la reserva debe ser mayor o igual a cero.
3. **Integridad Horaria:** La hora de término de una reserva debe ser estrictamente posterior a la hora de inicio (`hora_fin > hora`).

## Usuarios

1. Bloquear usuario despues de fallar 3 veces al ingresar al sistema.
2. Cada usuario debe tener un correo electrónico único.
3. El género de los usuarios se limita a Masculino, Femenino u Otro para fines de categorización.
4. Los usuarios invitados o externos pueden participar en equipos sin poseer una membresía activa inicialmente.
5. Los roles administrativos (Admin, Recepcionista) no requieren estar asociados a una membresía de cliente.

## Torneos y Partidos

1. La fecha de fin de un torneo no puede ser anterior a la fecha de inicio.
2. Un equipo no puede jugar un partido contra sí mismo.
3. Los resultados (goles/puntos) de un partido no pueden ser negativos y comienzan en cero por defecto.
4. **Regla de Walkover (Inasistencia):** Si un equipo no se presenta a un partido de torneo:
   - Se marca como Walkover (W.O.).
   - El resultado será estrictamente de 3-0 o 0-3 a favor del equipo que sí asistió (Regla técnica `ck_walkover_resultado`).
   - El capitán del equipo que no asistió recibirá automáticamente una penalización de tipo "No show".

## Membresías y Penalizaciones

1. El porcentaje de descuento de una membresía debe estar estrictamente entre 0 y 100.
2. Las multas por penalización se registran como "pendientes de pago" por defecto.
3. Los días de bloqueo por penalización deben ser valores no negativos.
4. **Fecha de Registro:** Las penalizaciones se fechan automáticamente al momento de la infracción (`CURRENT_DATE`).
5. **Bloqueo por Reincidencia:** Un usuario con 5 o más faltas vigentes no podrá realizar nuevas reservas hasta regularizar su situación.
