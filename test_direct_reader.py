from direct_reader import DirectReader
from parsing import Parser
from nfa import NFA

def main():
    print("\n🔹 Conversión de Expresión Regular a AFND")
    
    # 1️⃣ Pedir expresión regular al usuario
    regex = input("➡️  Ingresa una expresión regular: ")

    try:
        # 2️⃣ Tokenizar la expresión regular
        reader = DirectReader(regex)
        tokens = list(reader.CreateTokens())

        print("\n✅ Tokens generados:")
        for token in tokens:
            print(token)

        # 3️⃣ Construir el árbol sintáctico
        parser = Parser(tokens)
        arbol_sintactico = parser.Parse()

        print("\n🌳 Árbol Sintáctico generado con éxito.")

        # 4️⃣ Generar el AFND
        afnd = NFA(arbol_sintactico, reader.GetSymbols(), regex)

        # 5️⃣ Dibujar el AFND
        afnd.WriteNFADiagram()
        print("\n✅ Diagrama del AFND generado con éxito. Abriendo archivo...")

    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
