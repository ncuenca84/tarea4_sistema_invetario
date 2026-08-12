# Evidencia de pruebas — CR-004-SEM4-CUENCA-NIXON

Fecha: 12/08/2026

```
============================= test session starts ==============================
platform linux -- Python 3.11.15, pytest-9.1.1, pluggy-1.6.0 -- /usr/local/bin/python3
cachedir: .pytest_cache
rootdir: /home/user/tarea4_sistema_invetario
collecting ... collected 8 items

tests/test_inventario.py::test_agregar_no_perecible_sin_lote_ok PASSED   [ 12%]
tests/test_inventario.py::test_perecible_sin_lote_falla PASSED           [ 25%]
tests/test_inventario.py::test_perecible_sin_fecha_caducidad_falla PASSED [ 37%]
tests/test_inventario.py::test_perecible_completo_ok PASSED              [ 50%]
tests/test_inventario.py::test_codigo_duplicado_falla PASSED             [ 62%]
tests/test_inventario.py::test_cantidad_negativa_falla PASSED            [ 75%]
tests/test_inventario.py::test_caducado_true PASSED                      [ 87%]
tests/test_inventario.py::test_no_perecible_nunca_caduca PASSED          [100%]

============================== 8 passed in 0.01s ===============================
```
