# Control de Configuración — CR-004-SEM4-CUENCA-NIXON

**Proyecto:** Sistema de Inventario
**Caso práctico:** Opción A — Cambio funcional (alcance)
**Solicitud:** Agregar un campo obligatorio *Lote* y *Fecha de caducidad* en productos perecibles, aplicándolo también a **reportes** y **exportación**.

---

## TABLA 1 — Solicitud de Cambio (CR)

| Campo | Detalle |
|---|---|
| **ID CR** | CR-004-SEM4-CUENCA-NIXON |
| **Proyecto** | Sistema de Inventario |
| **Tipo de cambio** | Funcional (alcance) |
| **Descripción** | Incorporar dos campos nuevos al producto: `lote` (identificador de lote) y `fecha_caducidad`. Ambos son **obligatorios cuando el producto está marcado como perecible**. El cambio debe reflejarse en la validación de alta/edición de productos, en los **reportes** (inventario, perecibles, caducados) y en la **exportación** (CSV y JSON). |
| **Motivo** | Requisito de negocio + cumplimiento. Permite rastrear lotes para retiros de mercado (*recalls*), control de caducidad y reducción de pérdidas por producto vencido. |
| **Prioridad** | Alta |
| **Solicitante** | Product Owner (PO) — respaldado por área de Calidad/QC |
| **Fecha** | 12/08/2026 |
| **Elementos de configuración afectados** | Requisito (historia de usuario), Diseño (modelo de datos `Producto`), Código (`modelos.py`, `inventario.py`, `reportes.py`, `exportacion.py`), Pruebas (`tests/test_inventario.py`), Documentación (README, este documento). |

---

## TABLA 2 — Análisis de Impacto

| Área | Impacto | Evidencia / Nota |
|---|---|---|
| **Alcance** | Cambia | Se modifican: modelo `Producto`, validación, 3 reportes y 2 formatos de exportación. Nueva regla: perecible ⇒ lote + fecha_caducidad obligatorios. |
| **Tiempo** | +12 h aprox. (≈ 2 días) | Diseño 2 h, desarrollo 5 h, pruebas 3 h, documentación 2 h. |
| **Costo** | Bajo / sin costo adicional | No requiere licencias ni infraestructura nueva; se usa la stack existente (Python). |
| **Calidad** | Riesgo medio para QA | Requiere pruebas de validación (perecible con/sin campos), pruebas de regresión en reportes y exportación, y verificación de datos históricos sin lote. |
| **Arquitectura** | Componentes afectados | Módulo de dominio (`modelos`, `inventario`), módulo de reportes (`reportes`) y módulo de exportación (`exportacion`). Sin cambios en la arquitectura general. |
| **Seguridad** | No afecta | No cambia autenticación, autorización ni exposición de datos sensibles. `lote` y `fecha_caducidad` no son datos personales. |
| **Operación** | Despliegue simple + rollback disponible | Despliegue por *merge* de PR + tag de release. Rollback = revertir al tag anterior. Datos existentes no perecibles no se ven afectados. |

---

## TABLA 3 — Matriz de Riesgo

| # | Riesgo | Prob. | Impacto | Mitigación |
|---|---|---|---|---|
| R1 | Regresión: rompe reportes o exportación existentes al añadir columnas | Media | Alto | Pruebas de regresión automatizadas sobre reportes y export; revisión de PR; validar cabeceras CSV/JSON. |
| R2 | Datos históricos de perecibles sin `lote`/`fecha_caducidad` que fallan la nueva validación | Alta | Medio | Regla aplicada solo a altas/ediciones nuevas; plan de migración/carga de datos para registros antiguos; la validación no se ejecuta en solo-lectura. |
| R3 | Fecha de caducidad con formato inválido o inconsistente | Media | Medio | Tipar el campo como fecha (`date`), validar tipo en `Inventario.validar()`, prueba unitaria de formato. |
| R4 | Confusión entre productos perecibles y no perecibles (campos obligatorios donde no aplican) | Baja | Medio | Regla condicional (obligatorio **solo si** `perecible=True`); casos de prueba para ambos escenarios. |

**Nivel de riesgo global:** Medio — controlable con pruebas automatizadas y revisión de código.

---

## Decisión: **APROBADO**

**Justificación técnica:** El cambio es de bajo costo, sin impacto en seguridad ni en la arquitectura, y aporta valor directo de negocio (trazabilidad de lotes y control de caducidad). Los riesgos identificados (R1–R4) son de severidad media y quedan cubiertos por pruebas automatizadas, regla de validación condicional y un plan para datos históricos. Se aprueba para implementación inmediata bajo control de versiones (branch + PR + release).

**Órgano que aprueba:** CCB (Change Control Board) / PO.
**Condiciones de aprobación:** (1) cobertura de pruebas para perecible con y sin campos; (2) regresión verde en reportes y exportación; (3) documentar rollback.

---

## Plan de Implementación

| # | Paso | Responsable | Evidencia |
|---|---|---|---|
| 1 | Crear historia/requisito y CR en el gestor (Issue) | PO / PM | Issue de GitHub con la CR |
| 2 | Crear rama de trabajo desde `main` | Dev | Branch `claude/config-control-change-management-hsmc1i` |
| 3 | Añadir campos `lote` y `fecha_caducidad` al modelo `Producto` | Dev | `src/inventario/modelos.py` |
| 4 | Regla de validación condicional (perecible ⇒ campos obligatorios) | Dev | `src/inventario/inventario.py` |
| 5 | Reflejar campos en reportes | Dev | `src/inventario/reportes.py` |
| 6 | Reflejar campos en exportación CSV/JSON | Dev | `src/inventario/exportacion.py` |
| 7 | Pruebas unitarias y de regresión | QA / Dev | `tests/test_inventario.py` (8 pruebas, verdes) |
| 8 | Abrir Pull Request vinculado al Issue | Dev | PR con commits vinculados |
| 9 | Revisión y aprobación del PR | Líder técnico | Review aprobado |
| 10 | Merge + crear tag/release `v1.1.0` | PM / Dev | Tag `v1.1.0` + notas de versión |
| 11 | Cierre de CR e Issue | PM / QA | Issue cerrado + release publicado |

### Plan de rollback (mínimo)
1. Identificar el último tag estable previo (`v1.0.0`).
2. `git revert` del *merge* del PR **o** desplegar el tag `v1.0.0`.
3. Verificar reportes/exportación con el reporte de regresión.
4. Comunicar a los interesados y registrar en la CR.

---

## TABLA 4 — Seguimiento del Cambio (workflow)

| Estado | Quién | Condición de salida (evidencia) |
|---|---|---|
| **Registrado** | Solicitante / PM | CR creado con descripción completa (Issue abierto) |
| **En análisis** | Líder técnico / QA | Impacto (Tabla 2) + riesgos (Tabla 3) documentados |
| **Aprobado / Rechazado** | CCB / PM | Decisión con justificación técnica (este documento) |
| **En implementación** | Dev | Branch + PR con commits vinculados a la CR |
| **Verificado** | QA | Resultados de pruebas (8/8 verdes) + checklist |
| **Cerrado** | PM / QA | Tag `v1.1.0` + notas + Issue cerrado |

### Flujo de estados

```
Registrado --> En análisis --> Aprobado --> En implementación --> Verificado --> Cerrado
                                   |
                                   +--> Rechazado / Diferido (con justificación)
```

**Control del flujo:** cada transición requiere su evidencia de salida antes de avanzar. El PR no se fusiona sin pruebas verdes y revisión aprobada; la CR no se cierra sin release/tag.

---

## TABLA 5 — Trazabilidad mínima (CR → Artefactos)

| CR | Artefacto | Evidencia |
|---|---|---|
| CR-004-SEM4-CUENCA-NIXON | Requisito / Historia | Issue **#1** — https://github.com/ncuenca84/tarea4_sistema_invetario/issues/1 |
| CR-004-SEM4-CUENCA-NIXON | Diseño | Modelo `Producto` en `src/inventario/modelos.py` |
| CR-004-SEM4-CUENCA-NIXON | Código | Commit `d9a9a77`: `modelos.py`, `inventario.py`, `reportes.py`, `exportacion.py` |
| CR-004-SEM4-CUENCA-NIXON | Pruebas | `tests/test_inventario.py` — 8 casos, resultado **8 passed** |
| CR-004-SEM4-CUENCA-NIXON | Release | Tag `v1.1.0` + notas de versión (`CHANGELOG.md`) |

---

## Criterios de evaluación (autoevaluación)

| Criterio | Ponderación | Evidencia en esta entrega |
|---|---|---|
| Solicitud de cambio completa | 25% | Tabla 1 (ID, descripción, prioridad, EC afectados, motivo) |
| Análisis de impacto + riesgos | 30% | Tabla 2 + Tabla 3 con mitigaciones |
| Flujo de seguimiento | 20% | Tabla 4 + diagrama de estados y responsables |
| Trazabilidad y evidencia | 25% | Tabla 5 (CR→artefactos) + código, pruebas y release reales |
