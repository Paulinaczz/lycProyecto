import tkinter as tk
from tkinter import messagebox
from direct_reader import DirectReader
from parsing import Parser
from nfa import AFND
from dfa import AFD

def convertir_regex():
    regex = entry_regex.get()
    if not regex:
        messagebox.showerror("Error", "Por favor, ingresa una expresión regular.")
        return
    
    try:
        # Tokenizar la expresión regular
        reader = DirectReader(regex)
        tokens = list(reader.CrearTokens())
        
        # Construir el árbol sintáctico
        parser = Parser(tokens)
        arbol_sintactico = parser.Parse()
        
        # Generar el AFND
        afnd = AFND(arbol_sintactico, reader.GetSimbolos(), regex)
        afnd.WriteAFNDiagram()
        
        # Convertir AFND a AFD
        dfa = AFD(afnd.func_trans, reader.GetSimbolos(), list(afnd.func_trans.keys()), afnd.estados_aceptacion, regex)
        dfa.TransformarAFNaAFD()
        dfa.GraficarAFD()

        messagebox.showinfo("Éxito", "Diagramas del AFND y AFD generados con éxito.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

# Crear la ventana principal
root = tk.Tk()
root.title("Conversión de Expresión Regular a AFND y AFD")
root.geometry("400x200")

tk.Label(root, text="Ingresa una expresión regular:").pack(pady=10)
entry_regex = tk.Entry(root, width=40)
entry_regex.pack(pady=5)

btn_convertir = tk.Button(root, text="Convertir", command=convertir_regex)
btn_convertir.pack(pady=20)

root.mainloop()
#a