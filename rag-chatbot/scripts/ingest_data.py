import os
import logging
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
import uuid

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_secret_or_env(key):
    secret_path = f"/run/secrets/{key.lower()}"
    if os.path.exists(secret_path):
        with open(secret_path, "r") as f:
            return f.read().strip()
    return os.environ.get(key)

def ingest_data():
    try:
        logger.info("--- Starting data ingestion process ---")
        api_key = get_secret_or_env("PINECONE_API_KEY")
        pinecone_cloud = get_secret_or_env("PINECONE_CLOUD")
        pinecone_region = get_secret_or_env("PINECONE_REGION")

        if not all([api_key, pinecone_cloud, pinecone_region]):
            logger.error("Missing one or more Pinecone credentials. Aborting ingestion.")
            return

        logger.info("Connecting to Pinecone...")
        pc = Pinecone(api_key=api_key)
        
        index_name = "developer-quickstart-py"
        required_dimension = 384
        logger.info(f"Checking for index '{index_name}'...")

        index_exists = index_name in pc.list_indexes().names()

        if index_exists:
            logger.info(f"Index '{index_name}' already exists.")
            description = pc.describe_index(index_name)
            if description.dimension != required_dimension:
                logger.warning(f"Index dimension mismatch. Expected {required_dimension}, but got {description.dimension}. Deleting and recreating index.")
                pc.delete_index(index_name)
                index_exists = False

        if not index_exists:
            logger.info(f"Creating serverless index '{index_name}' with dimension {required_dimension}...")
            pc.create_index(
                name=index_name,
                dimension=required_dimension,
                metric="cosine",
                spec=ServerlessSpec(cloud=pinecone_cloud, region=pinecone_region)
            )
            logger.info("Index created.")

        index = pc.Index(index_name)
        logger.info("Index connected.")

        # Load data from file
        data_path = "data/default/sample.txt"
        logger.info(f"Loading data from {data_path}...")
        with open(data_path, "r") as f:
            text_data = f.read()

        # Split text into chunks
        logger.info("Splitting text into chunks...")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=450, chunk_overlap=100)
        chunks = text_splitter.split_text(text_data)
        logger.info(f"Split data into {len(chunks)} chunks.")

        # Prepare records for upsert
        logger.info("Embedding records...")
        embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        embeddings = embedding_model.encode(chunks)
        
        vectors_to_upsert = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            vector = (str(uuid.uuid4()), embedding.tolist(), {"text": chunk})
            vectors_to_upsert.append(vector)

        logger.info(f"Upserting {len(vectors_to_upsert)} vectors to Pinecone...")
        index.upsert(vectors=vectors_to_upsert)
        logger.info("Upsert completed.")

        # Verify the number of vectors in the index
        logger.info("Verifying data in index...")
        stats = index.describe_index_stats()
        logger.info(f"Index stats: {stats}")
        
        vector_count = stats.get('total_vector_count', 0)
        if vector_count > 0:
            logger.info(f"--- Successfully verified {vector_count} vectors in the index. Ingestion successful. ---")
        else:
            logger.error("--- Verification failed: No vectors found in the index after upsert. ---")

    except Exception as e:
        logger.error(f"An error occurred during data ingestion: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    ingest_data()
