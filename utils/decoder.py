def decode_tag(tag):
    lowercase_tag = tag.lower()
    decode_tree = {
        "a": {
            "label": "Adjetivo",
            "values": [
                {
                    "label": "Tipo",
                    "q": "Calificativo",
                    "o": "Ordinal"
                }, {
                    "label": "Grado",
                    "a": "Aumentativo",
                    "d": "Diminutivo",
                    "c": "Comparativo",
                    "s": "Superlativo"
                }, {
                    "label": "Género",
                    "m": "Masculino",
                    "f": "Femenino",
                    "c": "Común"
                }, {
                    "label": "Número",
                    "s": "Singular",
                    "p": "Plural",
                    "n": "Invariable"
                }, {
                    "label": "Función",
                    "0": "-",
                    "p": "Participi"
                }
            ]},
        "r": {
            "label": "Adverbio",
            "values": [
                {
                    "label": "Tipo",
                    "g": "General",
                    "n": "Negativo"
                }
            ]},
        "d": {
            "label": "Determinante",
            "values": [
                {
                    "label": "Tipo",
                    "d": "Demostrativo",
                    "p": "Posesivo",
                    "t": "Interrogativo",
                    "e": "Exclamativo",
                    "i": "Indefinido",
                    "a": "Artículo"
                }, {
                    "label": "Persona",
                    "1": "Primera",
                    "2": "Segunda",
                    "3": "Tercera"
                }, {
                    "label": "Género",
                    "m": "Masculino",
                    "f": "Femenino",
                    "c": "Común",
                    "n": "Neutro"
                }, {
                    "label": "Número",
                    "s": "Singular",
                    "p": "Plural",
                    "n": "Invariable"
                }, {
                    "label": "Poseedor",
                    "s": "Singular",
                    "p": "Plural"
                }
            ]},
        "n": {
            "label": "Nombre",
            "values": [
                {
                    "label": "Tipo",
                    "c": "Común",
                    "p": "Propio"
                }, {
                    "label": "Género",
                    "m": "Masculino",
                    "f": "Femenino",
                    "c": "Común"
                }, {
                    "label": "Número",
                    "s": "Singular",
                    "p": "Plural",
                    "n": "Invariable"
                }, {
                    "label": "Clasificación semántica",
                    "s": "Persona",
                    "g": "Lugar",
                    "o": "Organización",
                    "v": "Otros"
                }, {
                    # Included before
                    "label": "",
                    "p": "",
                    "0": ""
                }, {
                    "label": "Grado",
                    "a": "Aumentativo",
                    "d": "Diminutivo"
                }
            ]},
        "v": {
            "label": "Verbo",
            "values": [
                {
                    "label": "Tipo",
                    "m": "Principal",
                    "a": "Auxiliar",
                    "s": "Semiauxiliar"
                }, {
                    "label": "Modo",
                    "i": "Indicativo",
                    "s": "Subjuntivo",
                    "m": "Imperativo",
                    "n": "Infinitivo",
                    "g": "Gerundio",
                    "p": "Participio"
                }, {
                    "label": "Tiempo",
                    "p": "Presente",
                    "i": "Imperfecto",
                    "f": "Futuro",
                    "s": "Pasado",
                    "c": "Condicional",
                    "0": "-"
                }, {
                    "label": "Persona",
                    "1": "P1",
                    "2": "P2",
                    "3": "P3"
                }, {
                    "label": "Número",
                    "s": "SG",
                    "p": "PL"
                }, {
                    "label": "Género",
                    "M": "Masculino",
                    "F": "Femenino"
                },
            ]},
        "p": {
            "label": "Pronombre",
            "values": [
                {
                    "label": "Tipo",
                    "p": "Personal",
                    "d": "Demostrativo",
                    "x": "Posesivo",
                    "i": "Indefinido",
                    "t": "Interrogativo",
                    "r": "Relativo",
                    "e": "Exclamativo"
                }, {
                    "label": "Persona",
                    "1": "Primera",
                    "2": "Segunda",
                    "3": "Tercera"
                }, {
                    "label": "Género",
                    "m": "Masculino",
                    "f": "Femenino",
                    "c": "Común",
                    "n": "Neutro"
                }, {
                    "label": "Número",
                    "s": "Singular",
                    "p": "Plural",
                    "n": "ImpersonalMInvariable"
                }, {
                    "label": "Caso",
                    "n": "Nominativo",
                    "a": "Acusativo",
                    "d": "Dativo",
                    "o": "Oblicuo",
                }, {
                    "label": "Poseedor",
                    "s": "Singular",
                    "p": "Plural"
                }, {
                    "label": "Politeness",
                    "p": "Polite"
                },
            ]},
        "c": {
            "label": "Conjunción",
            "values": [
                {
                    "label": "Tipo",
                    "c": "Coordinada",
                    "s": "Subordinada"
                }
            ]},
        "i": {
            "label": "Interjección",
            "values": [
            ]},
        "s": {
            "label": "Adposición",
            "values": [
                {
                    "label": "Tipo",
                    "p": "Preposición"
                }, {
                    "label": "Forma",
                    "s": "Simple",
                    "c": "Contraída"
                }, {
                    "label": "Género",
                    "m": "Masculino"
                }, {
                    "label": "Número",
                    "s": "Singular"
                }
            ]},
        "f": {
            "label": "Puntuación",
            "values": [
                {}, {}
            ]},
        "Z": {
            "label": "Cifra",
            "values": [
                {
                    "label": "Tipo",
                    "d": "partitivo",
                    "m": "Moneda",
                    "p": "porcentaje",
                    "u": "unidad"
                }
            ]},
        "w": {
            "label": "Fecha/Hora",
            "values": [
            ]}
    }

    decoded = [decode_tree[lowercase_tag[0]]["label"]]
    for idx, code in enumerate(lowercase_tag[1:]):
        try:
            decoded.append(decode_tree[lowercase_tag[0]]["values"][idx][code])
        except KeyError:
            decoded.append("None")
    return decoded
