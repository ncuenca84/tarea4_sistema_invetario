# Changelog

Todas las versiones relevantes del Sistema de Inventario.

## [1.1.0] - 2026-08-12

### Añadido (CR-004-SEM4-CUENCA-NIXON)
- Campos `lote` y `fecha_caducidad` en el modelo `Producto`.
- Validación condicional: obligatorios para productos perecibles.
- Columnas `Lote` y `Fecha caducidad` en los reportes de inventario y perecibles.
- Reporte de productos caducados.
- Campos `lote` y `fecha_caducidad` en la exportación CSV y JSON.
- Pruebas unitarias de validación y regresión (8 casos).

### Trazabilidad
- CR: CR-004-SEM4-CUENCA-NIXON
- Requisito → Código → Pruebas → Release v1.1.0

## [1.0.0] - 2026-08-01

### Añadido
- Versión inicial del Sistema de Inventario: alta, edición, eliminación y
  listado de productos; reportes básicos y exportación CSV/JSON.
