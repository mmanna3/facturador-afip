import driver
from csv import DictReader
import os

CREDENCIALES_PATH = "credenciales.dat"
if not os.path.isfile(CREDENCIALES_PATH):
    raise Exception("No hay archivo de credenciales")

with open(CREDENCIALES_PATH, "r") as f:
    CUIL, CLAVE, NOMBRE_COMPLETO = f.read().splitlines()

with open("facturas.csv", "r") as f:
    dict_reader = DictReader(f)
    facturas = list(dict_reader)

h = driver.conectar_AFIP(
    CUIL,
    CLAVE,
    nombre=NOMBRE_COMPLETO,
)

for f in facturas:
    driver.generar_factura(h, f)

h.close()
