from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from sentence_transformers import CrossEncoder


def ejecutar_rag(pregunta):

    # 1. Cargar PDF
    pdf_path = "documentos/manual.pdf"

    loader = PyPDFLoader(pdf_path)
    documentos = loader.load()

    print(f"PDF cargado: {len(documentos)} páginas")

    # 2. Dividir en chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documentos)

    print(f"Chunks creados: {len(chunks)}")

    # 3. Embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Modelo de embeddings cargado")

    # 4. FAISS
    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    print("FAISS creado")

    # 5. Reranker
    reranker = CrossEncoder(
        "cross-encoder/ms-marco-MiniLM-L-6-v2"
    )

    print("Reranker cargado")

    # 6. Búsqueda FAISS
    resultados_faiss = vectorstore.similarity_search_with_score(
        pregunta,
        k=5
    )

    # 7. Preparar pares
    pares = []

    for documento, distancia in resultados_faiss:

        pares.append(
            [
                pregunta,
                documento.page_content
            ]
        )

    # 8. Reranking
    scores = reranker.predict(pares)

    # 9. Combinar resultados
    resultados_reranking = []

    for (documento, distancia), score in zip(
        resultados_faiss,
        scores
    ):

        resultados_reranking.append(
            (
                documento,
                distancia,
                score
            )
        )

    # 10. Ordenar
    resultados_reranking.sort(
        key=lambda x: x[2],
        reverse=True
    )

    # 11. Crear contexto
    contexto = ""

    for i, (documento, distancia, score) in enumerate(
        resultados_reranking[:2]
    ):

        pagina = documento.metadata.get(
            "page_label",
            documento.metadata.get("page", "desconocida")
        )

        contexto += f"""
FUENTE {i + 1}
Página: {pagina}

{documento.page_content}

"""

    return contexto