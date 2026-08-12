"""Pruebas de validación y lógica de negocio (CR-004)."""

import os
import sys
from datetime import date

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from inventario import Inventario, Producto, ErrorValidacion  # noqa: E402


def test_agregar_no_perecible_sin_lote_ok():
    """Un producto NO perecible no requiere lote ni fecha de caducidad."""
    inv = Inventario()
    inv.agregar(Producto(codigo="P001", nombre="Cuaderno", cantidad=10,
                         precio=1.5, perecible=False))
    assert len(inv) == 1


def test_perecible_sin_lote_falla():
    """CR-004: un perecible sin lote debe rechazarse."""
    inv = Inventario()
    with pytest.raises(ErrorValidacion, match="lote"):
        inv.agregar(Producto(codigo="P002", nombre="Leche", cantidad=5,
                             precio=1.0, perecible=True,
                             fecha_caducidad=date(2026, 12, 1)))


def test_perecible_sin_fecha_caducidad_falla():
    """CR-004: un perecible sin fecha de caducidad debe rechazarse."""
    inv = Inventario()
    with pytest.raises(ErrorValidacion, match="fecha_caducidad"):
        inv.agregar(Producto(codigo="P003", nombre="Yogur", cantidad=5,
                             precio=1.0, perecible=True, lote="L-1"))


def test_perecible_completo_ok():
    """CR-004: un perecible con lote y fecha de caducidad es válido."""
    inv = Inventario()
    inv.agregar(Producto(codigo="P004", nombre="Queso", cantidad=8,
                         precio=3.0, perecible=True, lote="L-2026-01",
                         fecha_caducidad=date(2026, 10, 1)))
    p = inv.obtener("P004")
    assert p is not None
    assert p.lote == "L-2026-01"
    assert p.fecha_caducidad == date(2026, 10, 1)


def test_codigo_duplicado_falla():
    inv = Inventario()
    inv.agregar(Producto(codigo="P005", nombre="Pan", cantidad=5, precio=1.0,
                         perecible=True, lote="L-9",
                         fecha_caducidad=date(2026, 8, 20)))
    with pytest.raises(ErrorValidacion, match="Ya existe"):
        inv.agregar(Producto(codigo="P005", nombre="Pan 2", cantidad=3,
                             precio=1.2, perecible=True, lote="L-10",
                             fecha_caducidad=date(2026, 8, 21)))


def test_cantidad_negativa_falla():
    inv = Inventario()
    with pytest.raises(ErrorValidacion, match="cantidad"):
        inv.agregar(Producto(codigo="P006", nombre="Agua", cantidad=-1,
                             precio=1.0, perecible=False))


def test_caducado_true():
    p = Producto(codigo="P007", nombre="Jugo", cantidad=1, precio=1.0,
                 perecible=True, lote="L-11", fecha_caducidad=date(2026, 1, 1))
    assert p.esta_caducado(referencia=date(2026, 8, 12)) is True


def test_no_perecible_nunca_caduca():
    p = Producto(codigo="P008", nombre="Lápiz", cantidad=1, precio=0.5,
                 perecible=False)
    assert p.esta_caducado(referencia=date(2030, 1, 1)) is False
