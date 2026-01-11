import logging
import os

from huggingface_hub import InferenceClient


def simplify_question(statement):
    template = "I have the following competitive programming problem that I want to show someone else:\n\n=======\n[[ORIGINAL]]\n=======\n\nStrip off all the stories, legends, characters, backgrounds etc. from the statement while still enabling everyone to understand the problem. Also remove the name of the character if possible. This is to say, do not remove anything necessary to understand the full problem and one should feel safe to replace the original statement with your version of the statement. If it is not in English make it English. Provide the simplified statement directly without jargon. Use mathjax ($...$) for math. Start your response with \"Simplified statement:\"."

    # Initialize Hugging Face client with API key from environment
    client = InferenceClient(token=os.getenv("HUGGINGFACE_API_KEY"))
    if client.token is None:
        raise RuntimeError(
            "HUGGINGFACE_API_KEY is not set in the environment.")

    prompt = template.replace("[[ORIGINAL]]", statement).strip()

    # Using a free model like Meta's Llama or Mistral
    response = client.chat_completion(
        model="meta-llama/Llama-3.2-3B-Instruct",  # Free model
        messages=[
            {
                "role": "user",
                "content": prompt
            },
            {"role": "assistant", "content": "Simplified statement:"}
        ],
        max_tokens=2048
    )
    return response.choices[0].message.content.strip()
