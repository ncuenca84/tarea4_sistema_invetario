"""Exportación de datos del Sistema de Inventario.

La CR-004 (SEM4) exige que los campos 'lote' y 'fecha_caducidad' se incluyan
en las exportaciones (CSV y JSON).
"""

from __future__ import annotations

import csv
import io
import json
from typing import List

from .inventario import Inventario

# Orden de columnas de exportación. Incluye 'lote' y 'fecha_caducidad' (CR-004).
CAMPOS: List[str] = [
    "codigo",
    "nombre",
    "cantidad",
    "precio",
    "perecible",
    "lote",
    "fecha_caducidad",
]


def exportar_csv(inventario: Inventario) -> str:
    """Exporta el inventario a una cadena en formato CSV."""
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=CAMPOS)
    writer.writeheader()
    for producto in inventario.listar():
        writer.writerow(producto.to_dict())
    return buffer.getvalue()


def exportar_json(inventario: Inventario, indent: int = 2) -> str:
    """Exporta el inventario a una cadena en formato JSON."""
    datos = [producto.to_dict() for producto in inventario.listar()]
    return json.dumps(datos, ensure_ascii=False, indent=indent)
