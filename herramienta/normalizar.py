"""MatIA · Funciones para depurar texto y códigos. Retos 2 y 4."""

TILDES = {"Á": "A", "É": "E", "Í": "I", "Ó": "O", "Ú": "U", "Ü": "U"}


def normalizar_codigo(texto):
    """' bn022r ' -> 'BN022R' ; '8393184.0' -> '8393184' ; '' -> ''."""
    t = str(texto).strip().upper()          # sin espacios a los lados y en mayúsculas
    if t.endswith(".0") and t[:-2].isdigit():
        t = t[:-2]                          # Excel convierte 8393184 en 8393184.0: quitamos el .0
    return t


def normalizar_texto(texto):
    """' Mosquito  curvo ' -> 'MOSQUITO CURVO': mayúsculas, sin tildes, sin espacios sobrantes."""
    t = ""
    for letra in str(texto).strip().upper():
        t += TILDES.get(letra, letra)       # si la letra tiene tilde, su versión sin tilde; si no, ella misma
    while "  " in t:                        # mientras queden dos espacios seguidos, los dejamos en uno
        t = t.replace("  ", " ")
    return t


def es_codigo_fabricante(codigo):
    """True si el código (ya normalizado) tiene la forma habitual: 2 letras, 3 cifras, 1 letra y
    quizá 1 cifra al final. 'BN022R' -> True ; '8393184' -> False ; 'CONMED' -> False."""
    if len(codigo) not in (6, 7):           # primero la longitud: así codigo[5] nunca da error
        return False
    final_bien = len(codigo) == 6 or codigo[6].isdigit()    # la 7.ª posición, si existe, es una cifra
    return codigo[0:2].isalpha() and codigo[2:5].isdigit() and codigo[5].isalpha() and final_bien


def codigo_de_nombre(nombre):
    """'0b181205-NB114R_18_JPG.rf.XYZ' -> 'NB114R'. Formato: hash-CODIGO_indice_...  ('' si no encaja)."""
    # TODO: Reto 4. Mismo código que el martes: split('-', 1) y split('_', 1).
    # Devolved el código ya normalizado con normalizar_codigo.
    return ""


def pruebas_reto2():
    assert normalizar_codigo(" bn022r ") == "BN022R"
    assert normalizar_codigo("8393184.0") == "8393184"
    assert normalizar_codigo("") == ""
    assert normalizar_texto(" Mosquito  curvo ") == "MOSQUITO CURVO"
    assert normalizar_texto("Disección") == "DISECCION"
    assert normalizar_texto("") == ""
    assert es_codigo_fabricante("BN022R") and es_codigo_fabricante("EA831R5")
    assert not es_codigo_fabricante("8393184") and not es_codigo_fabricante("CONMED") and not es_codigo_fabricante("")


def pruebas_reto4():
    assert codigo_de_nombre("0b181205-NB114R_18_JPG.rf.XYZ") == "NB114R"
    assert codigo_de_nombre("CAJA_cirugiaGeneralA_s3_01") == ""
    assert codigo_de_nombre("abc-SINGUIONBAJO") == ""
