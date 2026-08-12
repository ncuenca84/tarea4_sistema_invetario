"""Generación de reportes del Sistema de Inventario.

La CR-004 (SEM4) exige que los campos 'Lote' y 'Fecha de caducidad' se
reflejen en los reportes de productos perecibles.
"""

from __future__ import annotations

from datetime import date
from typing import List, Optional

from .inventario import Inventario
from .modelos import Producto


def reporte_inventario(inventario: Inventario) -> str:
    """Genera un reporte de texto tabular de todo el inventario.

    Incluye las columnas 'Lote' y 'Fecha caducidad' (CR-004).
    """
    encabezado = (
        f"{'Código':<10} {'Nombre':<22} {'Cant.':>6} {'Precio':>10} "
        f"{'Perecible':<10} {'Lote':<12} {'Fecha caducidad':<16}"
    )
    lineas: List[str] = [encabezado, "-" * len(encabezado)]
    for p in inventario.listar():
        lineas.append(
            f"{p.codigo:<10} {p.nombre:<22} {p.cantidad:>6} {p.precio:>10.2f} "
            f"{('Sí' if p.perecible else 'No'):<10} {(p.lote or '-'):<12} "
            f"{(p.fecha_caducidad.isoformat() if p.fecha_caducidad else '-'):<16}"
        )
    return "\n".join(lineas)


def reporte_perecibles(inventario: Inventario) -> str:
    """Reporte enfocado en productos perecibles con lote y caducidad."""
    encabezado = (
        f"{'Código':<10} {'Nombre':<22} {'Lote':<12} {'Fecha caducidad':<16}"
    )
    lineas: List[str] = ["REPORTE DE PRODUCTOS PERECIBLES", encabezado,
                         "-" * len(encabezado)]
    for p in inventario.perecibles():
        lineas.append(
            f"{p.codigo:<10} {p.nombre:<22} {(p.lote or '-'):<12} "
            f"{(p.fecha_caducidad.isoformat() if p.fecha_caducidad else '-'):<16}"
        )
    return "\n".join(lineas)


def reporte_caducados(
    inventario: Inventario, referencia: Optional[date] = None
) -> str:
    """Reporte de productos caducados a una fecha de referencia."""
    referencia = referencia or date.today()
    encabezado = (
        f"{'Código':<10} {'Nombre':<22} {'Lote':<12} {'Fecha caducidad':<16}"
    )
    lineas: List[str] = [
        f"REPORTE DE PRODUCTOS CADUCADOS (al {referencia.isoformat()})",
        encabezado,
        "-" * len(encabezado),
    ]
    caducados: List[Producto] = inventario.caducados(referencia)
    if not caducados:
        lineas.append("Sin productos caducados.")
    for p in caducados:
        lineas.append(
            f"{p.codigo:<10} {p.nombre:<22} {(p.lote or '-'):<12} "
            f"{(p.fecha_caducidad.isoformat() if p.fecha_caducidad else '-'):<16}"
        )
    return "\n".join(lineas)
