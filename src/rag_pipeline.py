from retriever import retrieve
from transformers import pipeline

generator = pipeline(
    "text-generation",
 model="distilgpt2"
)

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

    prompt = build_prompt(
        question,
        chunks
    )

    response = generator(
        prompt,
        max_new_tokens=100,
        do_sample=False
    )

    return response[0]["generated_text"]

if __name__ == "__main__":

    question = "Why are customers unhappy with credit cards?"

    answer = ask(question)

    print("\nFINAL ANSWER:\n")
    print(answer)