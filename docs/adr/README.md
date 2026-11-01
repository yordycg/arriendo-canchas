# Decisiones de arquitectura (ADR)

Cada archivo registra una decisión que condiciona el resto del sistema. Se escriben **a mano**,
usando el esqueleto de `docs/templates/adr.md`. La IA puede corregir forma, nunca contenido.

## Índice

| # | Decisión | Estado | Fase |
|---|---|---|---|
| 0001 | Estrategia de acceso a datos (SQL manual / ORM / híbrido) | pendiente | F1.1 |
| 0002 | Estrategia de tests y creación de la base de test | pendiente | F1.3 |
| 0003 | Modelo de datos y restricciones | pendiente | F1.4 |
| 0004 | Condición de carrera en la reserva | pendiente | F2.1 |

Estados posibles: `pendiente` · `propuesta` · `aceptada` · `reemplazada por NNNN`.

## Reglas

1. Una decisión por archivo. Si necesita dos títulos "Decisión", son dos ADR.
2. Se escribe antes de implementar, no después.
3. Si una ADR se reemplaza, la antigua **no se borra**: se marca como reemplazada.
4. Toda ADR declara cómo se verifica (test, comando o revisión manual).
