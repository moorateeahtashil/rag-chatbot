# Production-Ready RAG Chatbot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project is a complete, production-ready RAG (Retrieval-Augmented Generation) chatbot application. It is built with a modern Python stack and is fully containerized with Docker for easy deployment and scalability. It includes a web-based admin panel for easy interaction and configuration.

## Features

-   **Retrieval-Augmented Generation (RAG):** Provides answers grounded in a specific knowledge base, reducing hallucinations.
-   **Web UI:** A user-friendly admin panel built with AdminKit for interacting with the chatbot and managing settings.
-   **REST API:** A FastAPI-based backend provides a robust API for programmatic interaction.
-   **Configurable:** Easily change the knowledge base, language model, and other settings through configuration files.
-   **Containerized:** Fully containerized with Docker and Docker Compose for consistent environments and easy deployment.
-   **Scalable Architecture:** Modular and designed for scalability and maintainability.

## Architecture Overview

The application follows a standard RAG architecture:

1.  **Data Ingestion:** Text documents from the `/data` directory are chunked, embedded using a Sentence Transformer model, and stored in a Pinecone vector index. This happens automatically during the Docker build.
2.  **Runtime Query:** When a user sends a query, it is embedded into a vector. This vector is used to search the Pinecone index for the most relevant text chunks.
3.  **Answer Generation:** The retrieved text chunks are combined with the user's query into a prompt and sent to a generator LLM (Flan-T5-base), which synthesizes a final answer.

## Tech Stack

-   **Backend:** Python, FastAPI
-   **Vector Database:** Pinecone
-   **Embedding Model:** `all-MiniLM-L6-v2` (from Sentence Transformers)
-   **Generator Model:** `google/flan-t5-base` (from Hugging Face Transformers)
-   **Frontend:** AdminKit (Bootstrap 5)
-   **Deployment:** Docker, Docker Compose

## Getting Started

### Prerequisites

-   Docker
-   Docker Compose

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd rag-chatbot
    ```

2.  **Configure Environment Variables:**
    Create a `.env` file by copying the example template:
    ```bash
    cp .env.example .env
    ```
    Now, edit the `.env` file and add your credentials:
    -   `PINECONE_API_KEY`: Your API key from Pinecone.
    -   `PINECONE_CLOUD`: The cloud provider for your Pinecone index (e.g., `aws`).
    -   `PINECONE_REGION`: The region for your Pinecone index (e.g., `us-east-1`).

3.  **Build and Run the Application:**
    ```bash
    docker-compose up --build
    ```
    The first build will take some time as it needs to download the language models and run the data ingestion script.

## Usage

### Admin Panel

-   **URL:** [http://localhost:8000](http://localhost:8000)
-   **Documentation:** The main page provides a detailed overview of the project.
-   **Chatbot:** A real-time interface to test the chatbot.
-   **Settings:** A page to view and update the Pinecone credentials in the `.env` file.

### API Usage

The API is available for programmatic access. The interactive Swagger UI documentation can be found at [http://localhost:8000/docs](http://localhost:8000/docs).

**Example cURL request:**
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
-H "Content-Type: application/json" \
-d '{
  "query": "What is RAG?"
}'
```

## Customization

### Adding New Data

1.  Add your text files (`.txt`) to the `/data/default` directory.
2.  Rebuild the application to re-run the ingestion script:
    ```bash
    docker-compose up --build
    ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
