
from pathlib import Path

import chromadb
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    Settings,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore





# STEP 1: READ DOCUMENT
documents = SimpleDirectoryReader(
    input_dir="Documents"
).load_data()

print("Documents loaded:", len(documents))


# STEP 2: CREATE NODES (CHUNKS)
splitter = SentenceSplitter(
    chunk_size=150,
    chunk_overlap=20
)

nodes = splitter.get_nodes_from_documents(documents)

print("Total nodes:", len(nodes))
print("First node:", nodes[0].get_content()[:200])


Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = chromadb.PersistentClient(
    path="./chroma_db/llamaindex"
)

collection = db.get_or_create_collection(
    "museum_llamaindex"
)

vector_store = ChromaVectorStore(
    chroma_collection=collection
)

index = VectorStoreIndex(
    nodes,
    vector_store=vector_store
)

retriever = index.as_retriever(
    similarity_top_k=2
)


while True:
    question = input("\nAsk a question (exit to stop): ")

    if question.lower() == "exit":
        break

    results = retriever.retrieve(question)

    for result in results:
        print("\nRetrieved Text:")
        print(result.node.get_content())

        print("\nSource:")
        print(result.node.metadata.get("file_name"))

        print("Score:", result.score)
