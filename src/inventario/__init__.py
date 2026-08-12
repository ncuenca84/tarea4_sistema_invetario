"""Sistema de Inventario.

Paquete principal del sistema de gestión de inventario.
"""

from .modelos import Producto
from .inventario import Inventario, ErrorValidacion

__all__ = ["Producto", "Inventario", "ErrorValidacion"]
__version__ = "1.1.0"
