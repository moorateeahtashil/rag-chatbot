from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from app.core.config import get_settings

class VectorDBService:
    def __init__(self):
        settings = get_settings()
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

    def query(self, index_name: str, query: str, top_k: int = 3):
        index = self.pc.Index(index_name)
        query_embedding = self.embedding_model.encode([query]).tolist()[0]
        results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
        return [match['metadata']['text'] for match in results['matches']]