import tkinter as tk
import re

class Colorear:
    def __init__(self, texto_widget):
        
        self.entrada_texto = texto_widget
        self.definir_expresiones_regulares()
        self.configurar_tags()
        self.entrada_texto.bind("<<Modified>>", self.texto_modificado)
        self.actualizar_resaltado(None)

    def definir_expresiones_regulares(self):
        self.expresiones = {
            "palabrasReservadas": (r"\b(if|else|do|while|switch|case|integer|double|main)\b", "verde"),
            "operadoresReservados": (r"(\+|\-|\*|(?<!/)/(?!/)|\%|\^)", "azulClaro"), 
            "operadoresRelacionales": (r"(\<=|\<|\>=|\>|\!=|\==)", "rojo"), 
            "operadoresLogicos": (r"\b(or|and)\b", "morado"), 
            "simbolos": (r"(\(|\)|\{|\}|,|;)", "amarillo"), 
            "asignacion": (r"((?<![><=!])=(?!=))", "azulFuerte"), 
            "numeros": (r"(?<!\.)\b[-+]?(\d+\.\d+|\d+)\b(?!\.)", "rosaProfundo"),
            "comentarios": (r"\/\/[^\n]*", "gris"),
            "comentariosMultilinea": (r"/\*.*?\*/", "gris"),
        }

    def configurar_tags(self):
        colores = {
            "azulClaro": "deep sky blue",
            "verde": "spring green",
            "amarillo": "yellow",
            "rojo": "red",  
            "azulFuerte": "dodger blue", 
            "rosaProfundo": "deep pink",
            "gris": "gray",
        }
        for tag, color in colores.items():
            self.entrada_texto.tag_config(tag, foreground=color)

    def texto_modificado(self, event):
        if self.entrada_texto.edit_modified():
            self.actualizar_resaltado(None)
            self.entrada_texto.edit_modified(False)

    def actualizar_resaltado(self, event):
        texto = self.entrada_texto.get("1.0", tk.END)
        for tag in self.entrada_texto.tag_names():
            self.entrada_texto.tag_remove(tag, "1.0", tk.END)
        
        for key, (expr, tag) in self.expresiones.items():
            for match in re.finditer(expr, texto, re.DOTALL):
                inicio = f"1.0+{match.start()}c"
                fin = f"1.0+{match.end()}c"
                self.entrada_texto.tag_add(tag, inicio, fin)
