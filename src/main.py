"""Demostración de uso del Sistema de Inventario.

Ejecutar con:  python -m src.main   (desde la raíz del proyecto)
"""

from datetime import date

from inventario import Inventario, Producto
from inventario.exportacion import exportar_csv, exportar_json
from inventario.reportes import (
    reporte_caducados,
    reporte_inventario,
    reporte_perecibles,
)


def construir_inventario_demo() -> Inventario:
    inv = Inventario()
    # Producto no perecible: lote y fecha_caducidad opcionales.
    inv.agregar(Producto(codigo="P001", nombre="Cuaderno A4", cantidad=120,
                         precio=1.50, perecible=False))
    # Productos perecibles: lote y fecha_caducidad obligatorios (CR-004).
    inv.agregar(Producto(codigo="P002", nombre="Leche entera 1L", cantidad=40,
                         precio=0.95, perecible=True, lote="L-2026-0012",
                         fecha_caducidad=date(2026, 9, 30)))
    inv.agregar(Producto(codigo="P003", nombre="Yogur natural", cantidad=60,
                         precio=0.70, perecible=True, lote="L-2026-0007",
                         fecha_caducidad=date(2026, 8, 1)))
    return inv


def main() -> None:
    inv = construir_inventario_demo()

    print("=== REPORTE DE INVENTARIO ===")
    print(reporte_inventario(inv))
    print()
    print(reporte_perecibles(inv))
    print()
    print(reporte_caducados(inv, referencia=date(2026, 8, 12)))
    print()
    print("=== EXPORTACIÓN CSV ===")
    print(exportar_csv(inv))
    print("=== EXPORTACIÓN JSON ===")
    print(exportar_json(inv))


if __name__ == "__main__":
    main()
