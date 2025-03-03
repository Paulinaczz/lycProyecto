import tkinter as tk
from tkinter import messagebox
from direct_reader import DirectReader
from parsing import Parser
from nfa import AFND
from dfa import AFD

def validar_cadena(dfa):
    """Muestra una ventana para ingresar una cadena y validarla contra el AFD."""
    def procesar_validacion():
        cadena = entry_cadena.get()
        if not cadena:
            messagebox.showerror("Error", "Por favor, ingresa una cadena para validar.")
            return
        resultado = dfa.EvaluarCadena(cadena)
        messagebox.showinfo("Resultado", f"La cadena {'es válida' if resultado else 'NO es válida'} en el lenguaje.")

    def volver():
        ventana_validacion.destroy()

    ventana_validacion = tk.Toplevel(root)
    ventana_validacion.title("Validar Cadena")
    ventana_validacion.geometry("350x150")

    tk.Label(ventana_validacion, text="Ingresa una cadena para validar:").pack(pady=10)
    entry_cadena = tk.Entry(ventana_validacion, width=30)
    entry_cadena.pack(pady=5)

    frame_botones = tk.Frame(ventana_validacion)
    frame_botones.pack(pady=10)

    btn_validar = tk.Button(frame_botones, text="Validar", command=procesar_validacion)
    btn_validar.pack(side=tk.LEFT, padx=10)

    btn_volver = tk.Button(frame_botones, text="Volver", command=volver)
    btn_volver.pack(side=tk.RIGHT, padx=10)

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
        
        # Minimizar el AFD
        dfa.minimizar()
        dfa.GraficarAFD()

        messagebox.showinfo("Éxito", "Diagramas del AFND, AFD y AFD minimizado generados con éxito.")
        validar_cadena(dfa)  # Llamar a la interfaz de validación
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
