from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# ✅ Define globally (IMPORTANT)
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

vectorstore = Chroma(
    persist_directory="db",
    embedding_function=embeddings
)


def retrieve_docs(query):
    try:
        query = query.strip().lower()

        docs = vectorstore.similarity_search_with_score(query, k=3)

        if not docs:
            return None

        best_doc, best_score = docs[0]

        if best_score > 1.5:
            return None

        lines = best_doc.page_content.split("\n")
        query_words = query.split()

        best_line = None

        for line in lines:
            line = line.strip().lower()

            if not line:
                continue

            # skip headings like "4. Payment Issues"
            if line[0].isdigit():
                continue

            # check if line matches query words
            if any(word in line for word in query_words):
                best_line = line

        # ✅ If matched line found → return it
        if best_line:
            return best_line.capitalize()

        # fallback → return first meaningful line
        for line in lines:
            line = line.strip()
            if line and not line[0].isdigit():
                return line

        return None

    except Exception as e:
        return None