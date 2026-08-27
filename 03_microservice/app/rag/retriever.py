from app.rag.chunker import DocumentChunker
from app.rag.vector_store import InMemoryVectorStore
from app.config.settings import settings
import logging


logger = logging.getLogger(__name__)

class KnowledgeRetriever:
    """
    Orquesta la carga de documentos, la indexación y la recuperación de contexto relevante.
    """
    def __init__(self):
        self.chunker = DocumentChunker(knowledge_dir=settings.KNOWLEDGE_DIR)
        self.store = InMemoryVectorStore()
        self._initialize()

    def _initialize(self):
        """Carga e indexa automáticamente los archivos Markdown al iniciar el servicio."""
        chunks = self.chunker.load_and_chunk()
        logger.info("Inicializando retriever | chunks_cargados=%s", len(chunks))
        self.store.build_index(chunks)

    def get_relevant_context(self, query: str) -> str:
        """Retorna los fragmentos recuperados en un bloque de texto unificado."""
        logger.info("Buscando contexto relevante | query_len=%s", len(query or ""))
        retrieved_chunks = self.store.search(query=query, top_k=3)
        if not retrieved_chunks:
            logger.warning("Retriever sin resultados relevantes")
            return "No se encontró información específica en el perfil para esta consulta."
        logger.info("Retriever devolvio chunks | total=%s", len(retrieved_chunks))
        return "\n\n---\n\n".join(retrieved_chunks)

# Instancia singleton para reutilizar el índice en memoria
retriever_service = KnowledgeRetriever()