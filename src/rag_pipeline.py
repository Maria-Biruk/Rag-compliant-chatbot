from src.retriever import retrieve


def build_prompt(question, chunks):

    context = "\n\n".join(
        chunk[:300] for chunk in chunks
    )

    return f"""
You are a financial analyst assistant for CrediTrust.

Use ONLY the complaint excerpts below to answer the question.

If the information is not available in the context, reply:
"I don't have enough information."

Context:
{context}

Question:
{question}

Answer:
"""


def ask(question):

    results = retrieve(question)

    chunks = results["documents"][0]

    answer = "Based on the retrieved customer complaints:\n\n"

    for i, chunk in enumerate(chunks[:3], start=1):
        answer += f"{i}. {chunk[:250]}...\n\n"

    sources = chunks[:3]

    return answer, sources


if __name__ == "__main__":

    question = "Why are customers unhappy with credit cards?"

    answer, sources = ask(question)

    print("\nFINAL ANSWER:\n")
    print(answer)

    print("\nSOURCES:\n")
    for s in sources:
        print(s)