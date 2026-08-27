from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class InMemoryVectorStore:
    """
    Almacén vectorial en memoria para recuperación semántica ultrarrápida.
    Ideal para bases de conocimiento acotadas a nivel microservicio.
    """
    def __init__(self):
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words=None)
        self.documents: List[Dict[str, str]] = []
        self.tfidf_matrix = None

    def build_index(self, docs: List[Dict[str, str]]):
        """Indexa los chunks de texto en una matriz de vectores dispersos."""
        if not docs:
            return
        self.documents = docs
        texts = [doc["content"] for doc in docs]
        self.tfidf_matrix = self.vectorizer.fit_transform(texts)

    def search(self, query: str, top_k: int = 3) -> List[str]:
        """Calcula similitud de coseno contra el query y retorna los mejores fragmentos."""
        if not self.documents or self.tfidf_matrix is None:
            return []

        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # Obtiene los índices con mayor afinidad semántica
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        # Filtra únicamente aquellos con relevancia mínima
        results = [
            self.documents[i]["content"] 
            for i in top_indices 
            if similarities[i] > 0.05
        ]
        return results