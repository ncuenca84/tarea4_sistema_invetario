# Sistema de Inventario

Sistema básico de gestión de inventario. Incluye la **CR-004-SEM4-CUENCA-NIXON**:
campos obligatorios **Lote** y **Fecha de caducidad** para productos perecibles,
aplicados a validación, reportes y exportación.

## Estructura

```
src/
  inventario/
    modelos.py       # Modelo Producto (incluye lote y fecha_caducidad)
    inventario.py    # Reglas de negocio y validación
    reportes.py      # Reportes: inventario, perecibles, caducados
    exportacion.py   # Exportación CSV y JSON
  main.py            # Demostración de uso
tests/
  test_inventario.py # Pruebas unitarias (8 casos)
docs/
  CR-004-control-de-configuracion.md  # Entregables de control de configuración
CHANGELOG.md
```

## Cómo ejecutar

```bash
# Demostración
cd src && python3 main.py

# Pruebas
python3 -m pytest tests/ -q
```

## Regla de negocio (CR-004)

- Producto **no perecible**: `lote` y `fecha_caducidad` son opcionales.
- Producto **perecible**: `lote` y `fecha_caducidad` son **obligatorios**;
  su ausencia genera un `ErrorValidacion`.
- Los campos aparecen en todos los reportes y en las exportaciones CSV/JSON.

## Documentación de control de configuración

Ver [`docs/CR-004-control-de-configuracion.md`](docs/CR-004-control-de-configuracion.md):
solicitud de cambio, análisis de impacto, matriz de riesgo, decisión, plan de
implementación, workflow de seguimiento y trazabilidad.
