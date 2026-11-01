# Caso de estudio — Arriendo de Canchas

> Escribe este documento tú. La IA puede corregir forma, nunca el contenido.
> Regla: cada afirmación tiene que poder respaldarse con un archivo, un test o una captura.
> Si no puedes respaldarla, se borra.

## 1. Problema

Qué problema resuelve, para quién, y por qué existía antes del sistema. 5 líneas máximo.
Sin adjetivos: nada de "innovador" ni "robusto".

## 2. Alcance

| Dentro | Fuera |
|---|---|
| | |

## 3. Modelo de datos

Qué entidades existen y por qué. Enlace a `docs/database/README.md` y a las ADR.
Responde una sola pregunta: **¿qué restricción de la base protege la regla de negocio más cara?**

## 4. Arquitectura

Cómo se organiza el código (7 apps, por qué esa división) y dónde vive la lógica.
Enlace a `docs/arquitectura.md`.

## 5. Decisiones

Tabla resumen. El detalle vive en las ADR.

| # | Decisión | Costo que acepté |
|---|---|---|
| 0001 | | |
| 0002 | | |
| 0003 | | |

## 6. El error que encontré

La sección que más pesa en una entrevista. Estructura fija:

- **Qué hacía mal el sistema:** el chequeo de disponibilidad y la inserción no eran atómicos.
- **Cómo lo descubrí:** qué te hizo sospechar.
- **Cómo lo probé:** el test que falla contra la versión anterior.
- **Cómo lo resolví:** el mecanismo, en 3 líneas.
- **Qué aprendí:** la frase que dirías en una entrevista.

## 7. Proceso

Cómo se construyó de verdad: qué se delegó, qué se reescribió y por qué. Enlace a `docs/ai-log.md`.
Sin dramatismo y sin confesionario: es un registro de criterio.

## 8. Resultado

Qué se puede ver hoy: URL de la demo, usuario demo, suite de tests, CI.
Solo datos verificables. Si no hay demo, se dice.

## 9. Qué haría distinto

Tres puntos concretos. Uno de diseño, uno de proceso y uno de alcance.

## 10. Anexos

- ADR: `docs/adr/`
- Reglas de negocio: `docs/database/reglas.md`
- Capturas: `docs/evidencia/`
