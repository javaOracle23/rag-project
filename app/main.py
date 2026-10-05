from rag_pipeline import ejecutar_rag


def main():

    pregunta = input(
        "Escribe una pregunta sobre el PDF: "
    )

    contexto = ejecutar_rag(pregunta)

    print("\n")
    print("=" * 60)
    print("CONTEXTO FINAL PARA EL LLM")
    print("=" * 60)

    print(contexto)


if __name__ == "__main__":
    main()