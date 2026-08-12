"""Lógica de negocio del Sistema de Inventario."""

from __future__ import annotations

from datetime import date
from typing import Dict, Iterable, List, Optional

from .modelos import Producto


class ErrorValidacion(Exception):
    """Se lanza cuando un producto no cumple las reglas de validación."""


class Inventario:
    """Contenedor y gestor de productos del inventario."""

    def __init__(self) -> None:
        self._productos: Dict[str, Producto] = {}

    # ------------------------------------------------------------------ #
    # Validación
    # ------------------------------------------------------------------ #
    @staticmethod
    def validar(producto: Producto) -> None:
        """Valida un producto según las reglas de negocio.

        Regla CR-004 (SEM4): si el producto es perecible, los campos
        ``lote`` y ``fecha_caducidad`` son obligatorios.

        Lanza:
            ErrorValidacion: si alguna regla no se cumple.
        """
        if not producto.codigo or not producto.codigo.strip():
            raise ErrorValidacion("El código del producto es obligatorio.")
        if not producto.nombre or not producto.nombre.strip():
            raise ErrorValidacion("El nombre del producto es obligatorio.")
        if producto.cantidad < 0:
            raise ErrorValidacion("La cantidad no puede ser negativa.")
        if producto.precio < 0:
            raise ErrorValidacion("El precio no puede ser negativo.")

        if producto.perecible:
            if not producto.lote or not producto.lote.strip():
                raise ErrorValidacion(
                    "El campo 'lote' es obligatorio para productos perecibles."
                )
            if producto.fecha_caducidad is None:
                raise ErrorValidacion(
                    "El campo 'fecha_caducidad' es obligatorio para productos "
                    "perecibles."
                )
            if not isinstance(producto.fecha_caducidad, date):
                raise ErrorValidacion(
                    "El campo 'fecha_caducidad' debe ser una fecha válida."
                )

    # ------------------------------------------------------------------ #
    # Operaciones CRUD
    # ------------------------------------------------------------------ #
    def agregar(self, producto: Producto) -> None:
        """Agrega un producto al inventario tras validarlo."""
        self.validar(producto)
        if producto.codigo in self._productos:
            raise ErrorValidacion(
                f"Ya existe un producto con código '{producto.codigo}'."
            )
        self._productos[producto.codigo] = producto

    def actualizar(self, producto: Producto) -> None:
        """Actualiza un producto existente tras validarlo."""
        self.validar(producto)
        if producto.codigo not in self._productos:
            raise ErrorValidacion(
                f"No existe un producto con código '{producto.codigo}'."
            )
        self._productos[producto.codigo] = producto

    def eliminar(self, codigo: str) -> None:
        """Elimina un producto por su código."""
        if codigo not in self._productos:
            raise ErrorValidacion(f"No existe un producto con código '{codigo}'.")
        del self._productos[codigo]

    def obtener(self, codigo: str) -> Optional[Producto]:
        """Devuelve un producto por su código, o ``None`` si no existe."""
        return self._productos.get(codigo)

    def listar(self) -> List[Producto]:
        """Devuelve todos los productos ordenados por código."""
        return [self._productos[c] for c in sorted(self._productos)]

    # ------------------------------------------------------------------ #
    # Consultas de apoyo
    # ------------------------------------------------------------------ #
    def perecibles(self) -> List[Producto]:
        """Devuelve solo los productos perecibles."""
        return [p for p in self.listar() if p.perecible]

    def caducados(self, referencia: Optional[date] = None) -> List[Producto]:
        """Devuelve los productos caducados respecto a una fecha."""
        return [p for p in self.listar() if p.esta_caducado(referencia)]

    def __len__(self) -> int:
        return len(self._productos)

    def __iter__(self) -> Iterable[Producto]:
        return iter(self.listar())
