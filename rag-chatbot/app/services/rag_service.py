from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from app.core.config import get_domain_config
from app.services.vector_db import VectorDBService
import logging

class RAGService:
    def __init__(self, vector_db_service: VectorDBService):
        self.vector_db_service = vector_db_service
        self.tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
        self.logger = logging.getLogger(__name__)

    def get_answer(self, query: str, domain: str) -> dict:
        self.logger.info(f"Received query: '{query}' for domain: '{domain}'")
        
        domain_config = get_domain_config(domain)
        index_name = domain_config["index_name"]
        prompt_template = domain_config["system_prompt_template"]

        # 1. Query vector database for relevant context
        self.logger.info(f"Querying index '{index_name}' for relevant context...")
        context_chunks = self.vector_db_service.query(index_name, query)
        self.logger.info(f"Retrieved {len(context_chunks)} context chunks.")

        if not context_chunks:
            self.logger.warning("No context was retrieved from the vector database.")
            return {
                "answer": "I am sorry, I could not find any relevant information to answer your question.",
                "sources": []
            }

        self.logger.info(f"First retrieved chunk: {context_chunks[0][:250]}...")
        context = "\n---\n".join(context_chunks)

        # 2. Construct augmented prompt
        prompt = prompt_template.format(context=context, question=query)
        self.logger.info(f"Constructed prompt for LLM: {prompt}")

        # 3. Call LLM
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_length=1024, num_beams=5)
        answer = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
        self.logger.info(f"Generated answer: {answer}")

        return {
            "answer": answer,
            "sources": [{"source": "vector_db", "content": chunk} for chunk in context_chunks]
        }