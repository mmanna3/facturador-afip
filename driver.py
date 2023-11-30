from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep


def conectar_AFIP(usuario, clave, nombre, driverapp="./chromedriver"):
    # h = webdriver.Chrome(driverapp)

    chrome_driver_path = "./chromedriver"
    service = Service(chrome_driver_path)
    h = webdriver.Chrome(service=service)

    h.implicitly_wait(2)

    h.get(
        "https://auth.afip.gov.ar/contribuyente_/login.xhtml?action=SYSTEM&system=rcel"
    )

    if not h.current_url.startswith("https://auth.afip.gov.ar/contribuyente_/"):
        raise Exception("Error!")

    type_text(h, "F1:username", usuario)
    click_id(h, "F1:btnSiguiente")
    type_text(h, "F1:password", clave)
    click_id(h, "F1:btnIngresar")
    sleep(1)

    click_if_value(h, "input", nombre)
    sleep(3)
    return h


def click_id(h, id_):
    it = h.find_element(By.ID, id_)
    it.click()


def type_text(h, id_, val, by_=By.ID, tab=False):
    it = h.find_element(by_, id_)
    it.clear()
    it.send_keys(val)

    if tab:
        it.send_keys(webdriver.Keys.TAB)


def click_if_value(h, els, val):
    for el in as_list(els):
        for it in h.find_elements(By.TAG_NAME, el):
            if it.get_attribute("value") == val:
                it.click()
                break


def as_list(x):
    if type(x) is list:
        return x
    return [x]


def select(h, id_, by_=By.ID, index=None, value=None):
    it = Select(h.find_element(by_, id_))

    if index is not None:
        it.select_by_index(index)
    else:
        it.select_by_value(value)


def generar_factura(h, ft):
    return fill_pagina(h, ft)


def fill_pagina(h, ft):
    FACT_C = "2"
    CONCEPTO_SERVICIOS = "2"
    CONSUMIDOR_FINAL = "5"
    OTRAS_UNIDADES = "98"
    TIEMPO_A_ESPERAR_ENTRE_PANTALLAS = 2

    fcdate = ft["fc_date"]
    sdate = ft["fc_date"]
    edate = ft["fc_date"]

    # Pantalla 1
    click_id(h, "btn_gen_cmp")
    select(h, "puntodeventa", index=1)
    select(h, "universocomprobante", value=FACT_C)
    sleep(TIEMPO_A_ESPERAR_ENTRE_PANTALLAS)
    click_if_value(h, "input", "Continuar >")

    # Pantalla 2: Datos de emisión
    type_text(h, "fc", fcdate)
    select(h, "idconcepto", value=CONCEPTO_SERVICIOS)
    type_text(h, "fsd", sdate)
    type_text(h, "fsh", edate)
    sleep(TIEMPO_A_ESPERAR_ENTRE_PANTALLAS)
    click_if_value(h, "input", "Continuar >")

    # Pantalla 3: Datos del receptor
    select(h, "idivareceptor", value=CONSUMIDOR_FINAL)
    click_id(h, "formadepago1")
    sleep(TIEMPO_A_ESPERAR_ENTRE_PANTALLAS)
    click_if_value(h, "input", "Continuar >")

    # Pantalla 4: Datos de la operación
    type_text(h, "detalle_descripcion1", ft["descripcion"])
    select(h, "detalle_medida1", value=OTRAS_UNIDADES)
    type_text(h, "detalle_precio1", ft["precio"])
    click_if_value(h, "input", "Continuar >")
    sleep(TIEMPO_A_ESPERAR_ENTRE_PANTALLAS)

    click_id(h, "btngenerar")
    h.switch_to.alert.accept()
    sleep(3)

    click_if_value(h, ["button", "input"], "Menú Principal")
    sleep(1)
