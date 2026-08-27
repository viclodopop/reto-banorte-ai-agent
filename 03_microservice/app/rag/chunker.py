import os
import re
from typing import List, Dict

class DocumentChunker:
    """
    Segmenta la base de conocimiento en bloques lógicos conservando
    encabezados y contexto semántico para optimizar la recuperación.
    """
    def __init__(self, knowledge_dir: str):
        self.knowledge_dir = knowledge_dir

    def load_and_chunk(self) -> List[Dict[str, str]]:
        chunks = []
        if not os.path.exists(self.knowledge_dir):
            return chunks

        # Itera sobre cada archivo Markdown del directorio knowledge
        for filename in sorted(os.listdir(self.knowledge_dir)):
            if filename.endswith(".md"):
                filepath = os.path.join(self.knowledge_dir, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                # Segmenta por secciones principales (## Encabezados)
                sections = re.split(r'\n(?=##\s+)', content)
                for section in sections:
                    clean_text = section.strip()
                    if clean_text:
                        chunks.append({
                            "source": filename,
                            "content": clean_text
                        })
        return chunks