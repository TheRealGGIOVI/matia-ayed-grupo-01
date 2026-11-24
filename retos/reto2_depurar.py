"""Reto 2 · Depurar antes de contar.

    py -3 retos/reto2_depurar.py
Normaliza códigos y categorías (herramienta/normalizar.py), vuelve a contar y muestra qué cambia.
"""
import os
import sys
from difflib import SequenceMatcher

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "herramienta"))
import configuracion
from lector_excel import leer_hoja
from normalizar import es_codigo_fabricante, normalizar_codigo, normalizar_texto, pruebas_reto2
from utiles import escribir_csv, guardar_texto, tabla_texto


def agrupar_variantes(valores, normalizar):
    """Diccionario forma_normalizada -> conjunto de formas originales distintas."""
    grupos = {}
    for v in valores:
        clave = normalizar(v)               # la etiqueta de la "caja": el texto limpio
        if clave not in grupos:
            grupos[clave] = set()           # caja nueva y vacía
        grupos[clave].add(v)                # metemos la forma original (el set no guarda repetidos)
    return grupos


def parecidas(textos, umbral=0.85):
    """Parejas de textos distintos que se parecen mucho (posibles erratas).
    Compara todas las parejas: k(k-1)/2 comparaciones. Devuelve (parejas, comparaciones)."""
    distintos = sorted(set(textos))         # sin repetidos y en orden
    parejas = []
    comparaciones = 0
    for i in range(len(distintos)):
        for j in range(i + 1, len(distintos)):   # j empieza en i+1: cada pareja se compara una sola vez
            comparaciones += 1
            parecido = SequenceMatcher(None, distintos[i], distintos[j]).ratio()   # 0 = nada, 1 = iguales
            if parecido >= umbral:
                parejas.append((distintos[i], distintos[j], round(parecido, 2)))
    return parejas, comparaciones


def pruebas():
    pruebas_reto2()                              # pruebas de herramienta/normalizar.py
    g = agrupar_variantes(["PINZA ", "PINZA", "Tijera"], normalizar_texto)
    assert g["PINZA"] == {"PINZA ", "PINZA"}                 # presente, con dos variantes
    assert "BISTURI" not in g                                  # ausente
    assert agrupar_variantes([], normalizar_texto) == {}      # vacío
    assert parecidas(["BABCOCK", "BABCOK", "PEAN"])[0] == [("BABCOCK", "BABCOK", 0.92)]
    assert parecidas([]) == ([], 0)


if __name__ == "__main__":
    pruebas()
    configuracion.comprobar()
    materiales = leer_hoja(configuracion.RUTA_EXCEL, "Materiales")

    # 1. Códigos
    codigos = [m["codigo_material"] for m in materiales]
    grupos_cod = agrupar_variantes(codigos, normalizar_codigo)
    cambian = [(m["id_material"], repr(m["codigo_material"]), normalizar_codigo(m["codigo_material"]))
               for m in materiales if m["codigo_material"] != normalizar_codigo(m["codigo_material"])]
    repetidos = []
    vistos = {}
    for m in materiales:
        c = normalizar_codigo(m["codigo_material"])
        if c == "":
            continue
        if c in vistos:
            repetidos.append((c, vistos[c], m["id_material"]))
        else:
            vistos[c] = m["id_material"]
    formato_raro = sorted(set(normalizar_codigo(c) for c in codigos if c.strip() != "" and not es_codigo_fabricante(normalizar_codigo(c))))

    # 2. Categorías
    categorias = [m["Descripcion_material_hqsmlg"] for m in materiales if m["Descripcion_material_hqsmlg"].strip() != ""]
    grupos_cat = agrupar_variantes(categorias, normalizar_texto)
    variantes = [(k, " · ".join(sorted("«%s»" % v for v in vs))) for k, vs in sorted(grupos_cat.items()) if len(vs) > 1]

    pares, comp_pares = parecidas(list(grupos_cat))

    # 3. Descripciones repetidas tras normalizar
    desc = {}
    for m in materiales:
        d = normalizar_texto(m["Descripcion_material"])
        if d != "":
            desc.setdefault(d, []).append(m["id_material"])
    desc_rep = [(d, ", ".join(ids)) for d, ids in desc.items() if len(ids) > 1]

    lineas = ["# Reto 2 · Qué cambia al depurar", ""]
    lineas += tabla_texto(["Indicador", "Antes", "Después de normalizar"], [
        ["Códigos distintos (sin vacíos)", len(set(c for c in codigos if c != "")), len([k for k in grupos_cod if k != ""])],
        ["Códigos vacíos", sum(1 for c in codigos if c.strip() == ""), sum(1 for c in codigos if normalizar_codigo(c) == "")],
        ["Códigos repetidos", len([c for c in codigos if c != ""]) - len(set(c for c in codigos if c != "")), len(repetidos)],
        ["Categorías distintas", len(set(categorias)), len(grupos_cat)],
        ["Materiales sin categoría", len(materiales) - len(categorias), len(materiales) - len(categorias)],
    ])
    lineas += ["", "## Códigos que cambian al normalizar", ""] + tabla_texto(["id_material", "Original", "Normalizado"], cambian or [["—", "—", "—"]])
    lineas += ["", "## Códigos repetidos tras normalizar", ""] + tabla_texto(["Código", "Primer id", "Otro id"], repetidos or [["—", "—", "—"]])
    lineas += ["", "## Códigos con formato distinto del habitual (%d)" % len(formato_raro), "", ", ".join(formato_raro) or "—"]
    lineas += ["", "## Categorías que solo se diferenciaban por espacios, mayúsculas o tildes", ""] + tabla_texto(["Normalizada", "Variantes"], variantes or [["—", "—"]])
    lineas += ["", "## Categorías parecidas: posibles erratas (%d comparaciones)" % comp_pares, "",
               "Ojo: la herramienta PROPONE; que sean el mismo instrumento lo decide una persona.", ""]
    lineas += tabla_texto(["Categoría", "Categoría parecida", "Parecido (0–1)"], pares or [["—", "—", "—"]])
    lineas += ["", "## Descripciones repetidas", ""] + tabla_texto(["Descripción", "ids"], desc_rep or [["—", "—"]])
    print("\n".join(lineas))
    guardar_texto(os.path.join(configuracion.RESULTADOS, "reto2_depuracion.md"), lineas)
    escribir_csv(os.path.join(configuracion.RESULTADOS, "reto2_categorias_normalizadas.csv"), ["categoria_normalizada", "variantes"],
                 [(k, " | ".join(sorted(v))) for k, v in sorted(grupos_cat.items())])
