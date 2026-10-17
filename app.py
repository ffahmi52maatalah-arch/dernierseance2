
import re
from ollama import chat

MODEL = "qwen3.5:9b"

REFUSAL = (
    "I cannot help generate abusive or discriminatory content. "
    "I can help you explore the topic respectfully."
)

# Simple demonstration filter. Expand and test for your language.
BLOCKED_PATTERNS = [
    r"\bkill all members of\b",
    r"\bwrite hate speech against\b",
    r"\binsult (?:all )?people with\b",
]

def is_unsafe(text):
    return any(
        re.search(pattern, text, re.IGNORECASE)
        for pattern in BLOCKED_PATTERNS
    )

def safe_tutor(question):
    # Safeguard 1: check user input
    if is_unsafe(question):
        return REFUSAL

    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful educational tutor. "
                    "Explain concepts respectfully. Do not produce "
                    "hate speech, discriminatory insults, or "
                    "instructions intended to harm people."
                )
            },
            {"role": "user", "content": question}
        ]
    )

    answer = response.message.content

    # Safeguard 2: check generated output before displaying it
    if is_unsafe(answer):
        return REFUSAL

    return answer


if __name__ == "__main__":
    question = input("Ask your tutor: ")
    print("Tutor:", safe_tutor(question))
