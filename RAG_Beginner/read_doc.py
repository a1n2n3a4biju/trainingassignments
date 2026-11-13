"""
SIMPLE PYTHON RAG PROJECT

TASK 1 - Read and tokenize documents.
TASK 2 - Create chunks and embeddings.
TASK 3 - Store and retrieve chunks using ChromaDB.
TASK 4 - Generate answers using an AI model.
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

from rag_core import (
    COLLECTION_NAME,
    read_documents,
    count_tokens,
    make_chunks,
    embed_texts,
    get_database,
    search_chunks
)


# --------------------------------------------------
# STEP 1: READ DOCUMENTS
# --------------------------------------------------

print("\n========== STEP 1: READ DOCUMENTS ==========")

documents = read_documents()

for document in documents:

    filename = document["filename"]
    text = document["text"]

    print("\nDocument:", filename)
    print("Characters:", len(text))
    print("Token count:", count_tokens(text))


# --------------------------------------------------
# STEP 2: CREATE CHUNKS
# --------------------------------------------------

print("\n========== STEP 2: CREATE CHUNKS ==========")

all_chunks = []
all_sources = []

for document in documents:

    filename = document["filename"]
    text = document["text"]

    chunks = make_chunks(
        text,
        chunk_size=120,
        overlap=20
    )

    all_chunks.extend(chunks)

    all_sources.extend(
        [filename] * len(chunks)
    )


print("Total chunks:", len(all_chunks))

if not all_chunks:
    raise ValueError("No chunks were generated.")

print("\nSample chunk:")
print(all_chunks[0])


# --------------------------------------------------
# STEP 3: GENERATE EMBEDDINGS
# --------------------------------------------------

print("\n========== STEP 3: GENERATE EMBEDDINGS ==========")

embeddings = embed_texts(all_chunks)

print("Total embeddings:", len(embeddings))
print("Vector size:", len(embeddings[0]))


# --------------------------------------------------
# STEP 4: STORE IN CHROMADB
# --------------------------------------------------

print("\n========== STEP 4: STORE IN CHROMADB ==========")

db = get_database()

# Remove the previous collection to avoid
# duplicate IDs when running the script again.

try:
    db.delete_collection(COLLECTION_NAME)
except Exception:
    pass


collection = db.create_collection(
    name=COLLECTION_NAME,
    embedding_function=None
)


collection.add(

    documents=all_chunks,

    embeddings=embeddings,

    metadatas=[
        {"source": filename}
        for filename in all_sources
    ],

    ids=[
        f"id_{i}"
        for i in range(len(all_chunks))
    ]
)


print("Collection:", COLLECTION_NAME)
print("Stored chunks:", collection.count())

# --------------------------------------------------
# STEP 5: CONNECT TO OPENROUTER
# --------------------------------------------------

print("\n========== STEP 5: CONNECT TO OPENROUTER ==========")

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError(
        "OPENROUTER_API_KEY is missing from your .env file."
    )

ai_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "openai/gpt-oss-120b"
)

print("OpenRouter connected successfully!")
print("Selected model:", MODEL)


# --------------------------------------------------
# STEP 6: ASK A QUESTION
# --------------------------------------------------

print("\n========== STEP 6: ASK A QUESTION ==========")

while True:

    question = input(
        "\nEnter your question (or type 'exit'): "
    ).strip()

    if question.lower() == "exit":
        print("RAG application stopped.")
        break

    if not question:
        print("Please enter a question.")
        continue


    # --------------------------------------------------
    # STEP 7: RETRIEVE TOP 2 RELEVANT CHUNKS
    # --------------------------------------------------

    print("\n========== STEP 7: RETRIEVAL ==========")

    results = search_chunks(
        question,
        top_k=2
    )

    for i, result in enumerate(results, start=1):

        print(f"\nResult {i}")

        print("Chunk ID:", result["id"])

        print("Source:", result["source"])

        print("Cosine Distance:", result["distance"])

        print("Retrieved Text:")
        print(result["text"])


    # --------------------------------------------------
    # STEP 8: PREPARE CONTEXT
    # --------------------------------------------------

    context = "\n\n".join(
        result["text"]
        for result in results
    )


    # --------------------------------------------------
    # STEP 9: CREATE AI PROMPT
    # --------------------------------------------------

    prompt = f"""
    You are an employee workplace policy assistant.

    Answer the question using ONLY the provided context.

    Do not use outside knowledge.
    Do not invent information.

    If the answer is not available in the context,
    say:
    "I cannot find the answer in the provided documents."

    CONTEXT:
    {context}

    QUESTION:
    {question}

    ANSWER:
    """


    # --------------------------------------------------
    # STEP 10: GENERATE AI ANSWER
    # --------------------------------------------------

    print("\n========== STEP 10: AI ANSWER ==========")

    response = ai_client.chat.completions.create(

        model=MODEL,

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0
    )

    answer = response.choices[0].message.content

    print("\nFinal Answer:")
    print(answer)

    print("\n" + "=" * 60)
