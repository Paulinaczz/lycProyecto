import tkinter as tk
from tkinter import messagebox
from direct_reader import DirectReader
from parsing import Parser
from nfa import NFA

def convertir_regex():
    regex = entry_regex.get()
    if not regex:
        messagebox.showerror("Error", "Por favor, ingresa una expresión regular.")
        return
    
    try:
        # Tokenizar la expresión regular
        reader = DirectReader(regex)
        tokens = list(reader.CreateTokens())
        
        # Construir el árbol sintáctico
        parser = Parser(tokens)
        arbol_sintactico = parser.Parse()
        
        # Generar el AFND
        afnd = NFA(arbol_sintactico, reader.GetSymbols(), regex)
        afnd.WriteNFADiagram()
        
        messagebox.showinfo("Éxito", "Diagrama del AFND generado con éxito.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

# Crear la ventana principal
root = tk.Tk()
root.title("Conversión de Expresión Regular a AFND")
root.geometry("400x200")

tk.Label(root, text="Ingresa una expresión regular:").pack(pady=10)
entry_regex = tk.Entry(root, width=40)
entry_regex.pack(pady=5)

btn_convertir = tk.Button(root, text="Convertir", command=convertir_regex)
btn_convertir.pack(pady=20)

root.mainloop()
#a