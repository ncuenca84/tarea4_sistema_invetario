"""Modelos de datos del Sistema de Inventario."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class Producto:
    """Representa un producto del inventario.

    A partir de la CR-004 (SEM4), los productos perecibles requieren de forma
    obligatoria los campos ``lote`` y ``fecha_caducidad``. Los productos no
    perecibles pueden dejar estos campos vacíos.

    Atributos:
        codigo: Identificador único del producto (SKU).
        nombre: Nombre descriptivo del producto.
        cantidad: Unidades disponibles en stock.
        precio: Precio unitario.
        perecible: Indica si el producto es perecible.
        lote: Número/identificador de lote (obligatorio si es perecible).
        fecha_caducidad: Fecha de caducidad (obligatoria si es perecible).
    """

    codigo: str
    nombre: str
    cantidad: int = 0
    precio: float = 0.0
    perecible: bool = False
    lote: Optional[str] = None
    fecha_caducidad: Optional[date] = None

    def esta_caducado(self, referencia: Optional[date] = None) -> bool:
        """Indica si el producto está caducado respecto a una fecha.

        Devuelve ``False`` cuando el producto no es perecible o no tiene
        fecha de caducidad registrada.
        """
        if not self.perecible or self.fecha_caducidad is None:
            return False
        referencia = referencia or date.today()
        return self.fecha_caducidad < referencia

    def to_dict(self) -> dict:
        """Serializa el producto a un diccionario plano (para export/reportes)."""
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio": self.precio,
            "perecible": self.perecible,
            "lote": self.lote or "",
            "fecha_caducidad": (
                self.fecha_caducidad.isoformat() if self.fecha_caducidad else ""
            ),
        }
