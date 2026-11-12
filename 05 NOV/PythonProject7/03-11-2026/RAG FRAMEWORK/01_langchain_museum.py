from pathlib import Path
import sys
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

docs=[]
DOCUMENTS_PATH=Path('Documents')
for file_path in DOCUMENTS_PATH.glob("*.txt"):
    text=file_path.read_text(encoding='utf-8')
    document=Document(
        page_content=text,
        metadata={"source":file_path.name}
    )
    docs.append(document)
# print("Document loaded:", len(docs))

splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    encoding_name="cl100k_base",
    chunk_size=180,
    chunk_overlap=35
)

chunks = splitter.split_documents(docs)

for i, chunk in enumerate(chunks, start=1):
    chunk.metadata["chunk_id"] = f"lc_chunk_{i:03d}"

# print("Total chunks:", len(chunks))
# print("First chunk:", chunks[0].page_content[:130])

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="museum_langchain",
    persist_directory="./chroma_db/langchain"
)


while True:
    question = input("\nEnter your question (exit to stop): ").strip()

    if question.lower() == "exit":
        break

    if not question:
        continue

    results = vectorstore.similarity_search_with_score(question, k=3)

    for document, distance in results:
        print("\n" + "-" * 60)
        print("Chunk:", document.metadata["chunk_id"])
        print("Source:", document.metadata["source"])
        print("Cosine distance:", round(distance, 4))
        print("Text:", document.page_content)





