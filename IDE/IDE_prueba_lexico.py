import tkinter as tk
from tkinter import ttk, filedialog, messagebox 
from colorearFinalizado import Colorear
from lexicoProceso import AnalizadorLexico

class IDE:
    def __init__(self, raiz):
        bandera=True;
        self.raiz = raiz
        self.raiz.geometry('1400x600')  # Establece el tamaño de la ventana
        self.ruta_archivo_actual = None  # Variable para almacenar la ruta del archivo actual
        
        # Configuración de la interfaz de usuario
        self.configurar_interfaz_usuario()

          # Aplica Colorear al editor de texto
        self.resaltador = Colorear(self.editor_de_texto)


        # Inicializar los números de línea y configurar la actualización automática
        self.actualizar_numeros_de_linea()
        self.raiz.after(100, self.actualizar_numeros_de_linea_automaticamente)

    def configurar_interfaz_usuario(self):
        # Crear y empaquetar el marco de botones
        self.crear_marco_botones()

        # Configurar el menú
        self.configurar_menu()

        # Crear paneles y ventanas con pestañas
        self.crear_paneles()
        self.crear_ventana_editor()
        self.crear_ventana_pestanas()
        self.crear_ventana_consola()

        # Crear etiqueta para mostrar la posición del cursor
        self.crear_etiqueta_posicion_cursor()

    def crear_marco_botones(self):
        self.marco_botones = tk.Frame(self.raiz)
        self.marco_botones.pack(side=tk.TOP, fill=tk.X)
        botones = [
            ("Abrir", self.abrir_archivo),
            ("Guardar", self.guardar_archivo),
            ("Guardar Como", self.guardar_archivo_como),
            ("Cerrar", self.cerrar_archivo),
            ("Compilar", self.compilar_lexico)
        ]
        for texto, comando in botones:
            tk.Button(self.marco_botones, text=texto, command=comando).pack(side=tk.LEFT)

    def configurar_menu(self):
        menu = tk.Menu(self.raiz)
        self.raiz.config(menu=menu)
        menu_archivo = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Abrir", command=self.abrir_archivo)
        menu_archivo.add_command(label="Guardar", command=self.guardar_archivo)
        menu_archivo.add_command(label="Guardar Como", command=self.guardar_archivo_como)
        menu_archivo.add_command(label="Cerrar", command=self.cerrar_archivo)

    def crear_paneles(self):
        self.ventana_con_paneles = tk.PanedWindow(self.raiz, orient=tk.VERTICAL)
        self.ventana_con_paneles.pack(fill=tk.BOTH, expand=1)

        self.marco_superior = tk.Frame(self.ventana_con_paneles)
        self.ventana_con_paneles.add(self.marco_superior, height=400)

        self.marco_inferior = tk.Frame(self.ventana_con_paneles)
        self.ventana_con_paneles.add(self.marco_inferior, height=200)

    def crear_ventana_editor(self):
        texto_inicial = """
// Ejemplo de uso de palabras reservadas, operadores y comentarios
int main() {
    integer contador = 0;  // Declaración de variable de tipo integer
    double total = 0.0;    // Declaración de variable de tipo double

    // Verifica una condición compuesta con operadores lógicos y relacionales
    if(contador < 10 and total <= 100.5) {
        do {
            // Acción condicional con operador de desigualdad
            if(contador != 5) {
                total = total + 10.5;  // Actualiza el total
            } else {
                total = total / 2;  // Divide el total por dos
            }
            contador = contador + 1;  // Incrementa el contador
        } while(contador <= 10);  // Condicional del bucle do-while
    } else if (total > 200.0 or contador == 0) {
        // Acción alternativa en caso de que la primera condición no se cumpla
        total = 0;  // Reinicia el total
    }

    // Ciclo while con una condición simple
    while(contador > 0) {
        contador = contador - 1;  // Decrementa el contador
    }

    return 0; // Fin del programa
}
"""
        self.numeros_de_linea = tk.Text(self.marco_superior, width=4, state='disabled',bg='gray22', fg='white', insertbackground='white', wrap='none')
        self.numeros_de_linea.pack(side=tk.LEFT, fill=tk.Y)
        self.editor_de_texto = tk.Text(self.marco_superior,bg='gray22', fg='white', insertbackground='white', wrap='none', undo=True, autoseparators=True, maxundo=-1)
        self.editor_de_texto.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.editor_de_texto.bind('<KeyRelease>', self.actualizar_numeros_de_linea)

        self.editor_de_texto.insert(tk.END,texto_inicial)

    def crear_ventana_pestanas(self):
        self.notebook = ttk.Notebook(self.marco_superior)
        self.tab_lexico = tk.Text(self.notebook,bg='gray22', fg='white', insertbackground='white', wrap='none')
        self.tab_sintactico = tk.Text(self.notebook,bg='gray22', fg='white', insertbackground='white', wrap='none')
        self.tab_semantico = tk.Text(self.notebook,bg='gray22', fg='white', insertbackground='white', wrap='none')
        self.tab_CodigoIntermedio= tk.Text(self.notebook,bg='gray22', fg='white', insertbackground='white', wrap='none')
        self.tab_HashTable= tk.Text(self.notebook,bg='gray22', fg='white', insertbackground='white', wrap='none')
        self.notebook.add(self.tab_lexico, text='Léxico')
        self.notebook.add(self.tab_sintactico, text='Sintáctico')
        self.notebook.add(self.tab_semantico, text='Semántico')
        self.notebook.add(self.tab_HashTable, text='HashTable')
        self.notebook.add(self.tab_CodigoIntermedio, text='Codigo intermedio')
        self.notebook.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

        colores = {
            "rojo": "deep sky blue", "verde": "spring green", "azul": "yellow",
            "rosa": "red", "amarillo": "purple", "morado": "firebrick1",
            "lima": "dodger blue", "rosaProfundo": "deep pink", "gris": "gray",
        }
        for tag, color in colores.items():
            self.tab_lexico.tag_config(tag, foreground=color)
        

    def crear_ventana_consola(self):
        self.notebook_consola = ttk.Notebook(self.marco_inferior)
        self.tab_errores_consola = tk.Text(self.notebook_consola,bg='gray22', fg='white', insertbackground='white', wrap='none')
        self.tab_resultados_consola = tk.Text(self.notebook_consola,bg='gray22', fg='white', insertbackground='white', wrap='none')
        self.notebook_consola.add(self.tab_errores_consola, text="Errores")
        self.notebook_consola.add(self.tab_resultados_consola, text="Resultados")
        self.notebook_consola.pack(fill=tk.BOTH, expand=1)

    def abrir_archivo(self):
        ruta_archivo = filedialog.askopenfilename()
        if ruta_archivo:
            with open(ruta_archivo, 'r') as archivo:
                contenido = archivo.read()
            self.editor_de_texto.delete('1.0', tk.END)
            self.editor_de_texto.insert('1.0', contenido)
            self.ruta_archivo_actual = ruta_archivo

    def guardar_archivo_como(self):
        ruta_archivo = filedialog.asksaveasfilename()
        if ruta_archivo:
            with open(ruta_archivo, 'w') as archivo:
                contenido = self.editor_de_texto.get('1.0', tk.END)
                archivo.write(contenido)
            self.ruta_archivo_actual = ruta_archivo
            messagebox.showinfo("Guardado", "Archivo guardado con éxito.")

    def guardar_archivo(self):

        if self.ruta_archivo_actual and self.ruta_archivo_actual!="" :
            with open(self.ruta_archivo_actual, 'w') as archivo:
                contenido = self.editor_de_texto.get('1.0', tk.END)
                archivo.write(contenido)
            messagebox.showinfo("Guardado", "Archivo guardado con éxito.")
        else:
            self.guardar_archivo_como()

    def cerrar_archivo(self):
        self.editor_de_texto.delete('1.0', tk.END)
        self.ruta_archivo_actual="";
        self.bandera=False;
    
    def compilar_lexico(self):
        codigo = self.editor_de_texto.get("1.0", tk.END)
        analizador = AnalizadorLexico()
        tokens, errores = analizador.analizar(codigo)
        
        self.tab_lexico.delete("1.0", tk.END)
        self.tab_errores_consola.delete("1.0", tk.END)
        
        #Mostramos tanto los errroes como los tokens
        for error in errores:
            self.tab_errores_consola.insert(tk.END, error + "\n")
        for token in tokens:
            tipo, color, valor = token[2], token[4], token[3]
            self.tab_lexico.insert(tk.END, f"{tipo} ({color}): {valor}\n")

        ''' MOstrar errores en su apartado si hay y no los tokes o si no hay errores mostrar los tokens en su apartado
        if errores:
            for error in errores:
                self.tab_errores_consola.insert(tk.END, error + "\n")
        else:
            for token in tokens:
                tipo, color, valor = token[2], token[4], token[3]
                self.tab_lexico.insert(tk.END, f"{tipo} ({color}): {valor}\n")'''



    def actualizar_numeros_de_linea(self, event=None):
        num_lines = self.editor_de_texto.get("1.0", "end-1c").count("\n") + 1
        line_numbers_text = "\n".join(str(i) for i in range(1, num_lines + 1))
        self.numeros_de_linea.config(state=tk.NORMAL)
        self.numeros_de_linea.delete("1.0", tk.END)
        self.numeros_de_linea.insert(tk.END, line_numbers_text)
        self.numeros_de_linea.config(state=tk.DISABLED)
        self.sincronizar_desplazamiento()

    def sincronizar_desplazamiento(self):
        text_area_scroll_pos = self.editor_de_texto.yview()[0]
        self.numeros_de_linea.yview_moveto(text_area_scroll_pos)

    def actualizar_numeros_de_linea_automaticamente(self):
        self.actualizar_numeros_de_linea()
        # Configurar la próxima actualización
        self.raiz.after(100, self.actualizar_numeros_de_linea_automaticamente)
        
    def crear_etiqueta_posicion_cursor(self):
        self.etiqueta_posicion = tk.Label(self.marco_botones, text="Línea: 1, Columna: 1")
        self.etiqueta_posicion.pack(side=tk.RIGHT)
        self.editor_de_texto.bind('<KeyRelease>', self.actualizar_posicion_cursor)
        self.editor_de_texto.bind('<Button-1>', self.actualizar_posicion_cursor)

    def actualizar_posicion_cursor(self, event=None):
        posicion = self.editor_de_texto.index(tk.INSERT)
        fila, columna = posicion.split('.')
        self.etiqueta_posicion.config(text=f"Línea: {fila}, Columna: {columna}")

if __name__ == "__main__":
    raiz = tk.Tk()
    raiz.title("IDE Completo con Números de Línea Automáticos")
    ide = IDE(raiz)
    raiz.mainloop()
