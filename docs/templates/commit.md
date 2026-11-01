# Plantilla de mensaje de commit

> La primera línea dice **qué** cambió. El cuerpo dice **por qué** y **qué se descartó**.
> Nunca escribas un commit en nombre de Yordy sin que él haya explicado el diff.

```
<type>(<scope>): <descripción en imperativo, minúscula, sin punto final>

Por qué:
- <causa o requisito que motiva el cambio>

Qué se descartó:
- <alternativa y razón>

Cómo se verificó:
- <test, comando o revisión manual>
```

## Tipos

`feat` · `fix` · `refactor` · `test` · `docs` · `chore` · `perf` · `build` · `ci`

## Scopes

`bookings` · `courts` · `users` · `auth` · `memberships` · `penalties` · `db` · `infra` · `docs`

## Ejemplo

```
fix(bookings): prevent double booking with a unique constraint

Por qué:
- El chequeo de disponibilidad y el INSERT no eran atómicos: dos usuarios
  podían reservar el mismo bloque en paralelo.

Qué se descartó:
- SELECT ... FOR UPDATE: bloquea más de lo necesario y no protege inserciones
  desde otros puntos del sistema.

Cómo se verificó:
- test_bookings.py::test_double_booking_is_rejected (falla en v1.0-academica)
```
