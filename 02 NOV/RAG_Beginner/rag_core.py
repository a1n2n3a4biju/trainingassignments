
"""Shared functions for the Simple Python RAG project."""

from pathlib import Path

import chromadb
import tiktoken
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction


# --------------------------------------------------
# 1. PROJECT CONFIGURATION
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent

DOCUMENTS_DIR = PROJECT_DIR / "Documents"

DB_PATH = PROJECT_DIR / "chroma_db"

COLLECTION_NAME = "EmployeeWorkplacePolicy_guide"

TOKENIZER = tiktoken.get_encoding("cl100k_base")


# --------------------------------------------------
# 2. READ DOCUMENTS
# --------------------------------------------------

def read_documents():
    """Read all text files from Documents folder."""

    documents = []

    for file_path in sorted(DOCUMENTS_DIR.glob("*.txt")):

        text = file_path.read_text(encoding="utf-8")

        documents.append({
            "filename": file_path.name,
            "text": text
        })

    if not documents:
        raise FileNotFoundError(
            "No .txt files found in Documents folder."
        )

    return documents


# --------------------------------------------------
# 3. COUNT TOKENS
# --------------------------------------------------

def count_tokens(text):
    """Count tokens in a document."""

    token_ids = TOKENIZER.encode(text)

    return len(token_ids)


# --------------------------------------------------
# 4. SPLIT TEXT INTO CHUNKS
# --------------------------------------------------

def make_chunks(text, chunk_size=120, overlap=20):
    """Split text into overlapping token chunks."""

    if not (0 <= overlap < chunk_size):
        raise ValueError(
            "Overlap must be >= 0 and smaller than chunk_size"
        )

    token_ids = TOKENIZER.encode(text)

    chunks = []

    start = 0

    while start < len(token_ids):

        end = min(start + chunk_size, len(token_ids))

        chunk = TOKENIZER.decode(
            token_ids[start:end]
        ).strip()

        if chunk:
            chunks.append(chunk)

        if end == len(token_ids):
            break

        start = end - overlap

    return chunks


# --------------------------------------------------
# 5. GENERATE EMBEDDINGS
# --------------------------------------------------

def embed_texts(texts):
    """Convert text into numerical vectors."""

    model = DefaultEmbeddingFunction()

    vectors = model(texts)

    return [
        v.tolist() if hasattr(v, "tolist") else list(v)
        for v in vectors
    ]


# --------------------------------------------------
# 6. CONNECT TO CHROMADB
# --------------------------------------------------

def get_database():
    """Create or connect to persistent ChromaDB."""

    return chromadb.PersistentClient(
        path=str(DB_PATH)
    )


# --------------------------------------------------
# 7. SEARCH RELEVANT CHUNKS
# --------------------------------------------------

def search_chunks(question, top_k=2):
    """Retrieve the most relevant chunks."""

    db = get_database()

    try:
        collection = db.get_collection(
            COLLECTION_NAME,
            embedding_function=None
        )

    except Exception as exc:
        raise RuntimeError(
            "No indexed collection. Run main.py first."
        ) from exc

    count = collection.count()

    if count == 0:
        raise RuntimeError(
            "The collection is empty. Run main.py first."
        )

    # Generate embedding for the question
    question_vector = embed_texts([question])[0]

    # Retrieve closest matching chunks
    results = collection.query(
        query_embeddings=[question_vector],
        n_results=min(top_k, count),
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    matches = []

    for chunk_id, text, metadata, distance in zip(
        results["ids"][0],
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):

        matches.append({
            "id": chunk_id,
            "text": text,
            "source": metadata.get("source", "unknown"),
            "distance": distance
        })

    return matches
