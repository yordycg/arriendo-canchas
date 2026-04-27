# Reglas de Negocio

## Canchas y Quinchos

1. Una "cancha" o "quincho" no puede ser "reservada" por mas de un "usuario" en el mismo bloque de fecha y hora. (Prevención de sobrecupo).
2. Los valores de arriendo por hora o reserva deben ser siempre mayores o iguales a cero.

## Reservas

1. Se puede "cancelar" una "reserva" con minimo 30 minutos de anticipacion.
   1.1 Por ejemplo: hacerlo con a los 20 minutos de la reserva, se le asigna una penalizacion al usuario.
2. El valor pagado registrado en la reserva debe ser mayor o igual a cero.

## Usuarios

1. Bloquear usuario despues de fallar 3 veces al ingresar al sistema.
2. Cada usuario debe tener un correo electrónico único.
3. El género de los usuarios se limita a Masculino, Femenino u Otro para fines de categorización.
4. Los usuarios invitados o externos pueden participar en equipos sin poseer una membresía activa inicialmente.

## Torneos y Partidos

1. La fecha de fin de un torneo no puede ser anterior a la fecha de inicio.
2. Un equipo no puede jugar un partido contra sí mismo.
3. Los resultados (goles/puntos) de un partido no pueden ser negativos y comienzan en cero por defecto.
4. **Regla de Walkover (Inasistencia):** Si un equipo no se presenta a un partido de torneo:
   - Se marca como Walkover (W.O.).
   - El resultado será estrictamente de 3-0 o 0-3 a favor del equipo que sí asistió.
   - El capitán del equipo que no asistió recibirá automáticamente una penalización de tipo "No show".

## Membresías y Penalizaciones

1. El porcentaje de descuento de una membresía debe estar estrictamente entre 0 y 100.
2. Las multas por penalización se registran como "pendientes de pago" por defecto.
3. Los días de bloqueo por penalización deben ser valores no negativos.
4. **Bloqueo por Reincidencia:** Un usuario con 5 o más faltas vigentes no podrá realizar nuevas reservas hasta regularizar su situación.
