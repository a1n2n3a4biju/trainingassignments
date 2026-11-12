
from pathlib import Path

from haystack import Document, Pipeline
from haystack.components.converters import TextFileToDocument
from haystack.components.preprocessors import DocumentSplitter
from haystack_integrations.components.embedders.sentence_transformers import (
    SentenceTransformersDocumentEmbedder,
    SentenceTransformersTextEmbedder
)
from haystack.components.writers import DocumentWriter
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.document_stores.in_memory import InMemoryDocumentStore


documents_path = Path("Documents")

documents = []

for file_path in documents_path.glob("*.txt"):
    documents.append(
        Document(
            content=file_path.read_text(encoding="utf-8"),
            meta={"source": file_path.name}
        )
    )

print("Total documents:", len(documents))


document_store = InMemoryDocumentStore()


indexing_pipeline = Pipeline()

indexing_pipeline.add_component(
    "splitter",
    DocumentSplitter(
        split_by="word",
        split_length=100,
        split_overlap=15
    )
)

indexing_pipeline.add_component(
    "embedder",
    SentenceTransformersDocumentEmbedder(
        model="sentence-transformers/all-MiniLM-L6-v2"
    )
)

indexing_pipeline.add_component(
    "writer",
    DocumentWriter(document_store=document_store)
)

indexing_pipeline.connect("splitter", "embedder")
indexing_pipeline.connect("embedder", "writer")


indexing_pipeline.run({
    "splitter": {
        "documents": documents
    }
})

print("Documents indexed successfully")


text_embedder = SentenceTransformersTextEmbedder(
    model="sentence-transformers/all-MiniLM-L6-v2"
)

text_embedder.warm_up()


retriever = InMemoryEmbeddingRetriever(
    document_store=document_store,
    top_k=2
)


while True:
    question = input("\nAsk a question (exit to stop): ")

    if question.lower() == "exit":
        break

    query_embedding = text_embedder.run(
        text=question
    )["embedding"]

    results = retriever.run(
        query_embedding=query_embedding
    )["documents"]

    for document in results:
        print("\nRetrieved Text:")
        print(document.content)

        print("\nSource:")
        print(document.meta.get("source"))

        print("Score:", document.score)
