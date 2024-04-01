import re

class AnalizadorLexico:
    def __init__(self):
        self.expresiones = [
            ("comentariosMultilinea", r"/\*[\s\S]*?\*/", "gris"),
            ("comentarios", r"\/\/[^\n]*", "gris"),
            ("espaciosEnBlanco", r"\s+", None),
            ("palabrasReservadas", r"\b(if|else|do|while|switch|case|integer|double|main)\b", "verde"),
            ("operadoresReservados", r"(\+|\-|\*|(?<!/)/(?!/)|\%|\^)", "azulClaro"),
            ("operadoresRelacionales", r"(\<=|\<|\>=|\>|\!=|\==)", "rojo"),
            ("operadoresLogicos", r"\b(or|and)\b", "morado"),
            ("simbolos", r"(\(|\)|\{|\}|,|;)", "amarillo"),
            ("asignacion", r"((?<![><=!])=(?!=))", "azulFuerte"),
            ("numeros", r"(?<!\.)\b[-+]?(\d+\.\d+|\d+)\b(?!\.)", "rosaProfundo"),
            ("identificadores", r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", "blanco"),
        ]

    def analizar(self, codigo):
        tokens = []
        posiciones_usadas = []
        errores = []

        for tipo, expr, color in self.expresiones:
            for match in re.finditer(expr, codigo, flags=re.DOTALL):
                if not any(start <= match.start() < end for start, end in posiciones_usadas):
                    tokens.append((match.start(), match.end(), tipo, match.group(), color))
                    posiciones_usadas.append((match.start(), match.end()))

        tokens.sort(key=lambda x: x[0])

        ultimo_final = 0
        for start, end, tipo, valor, color in tokens:
            if start > ultimo_final:
                errores.append(f"Error: texto no reconocido '{codigo[ultimo_final:start]}'")
            ultimo_final = max(ultimo_final, end)

        if ultimo_final < len(codigo):
            errores.append(f"Error: texto no reconocido '{codigo[ultimo_final:]}' ")

        resultado_tokens = [token for token in tokens if token[2] != "espaciosEnBlanco"]
        return resultado_tokens, errores
