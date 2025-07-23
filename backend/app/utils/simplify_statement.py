from together import Together


def simplify_question(statement):
    template = "I have the following competitive programming problem that I want to show someone else:\n\n=======\n[[ORIGINAL]]\n=======\n\nStrip off all the stories, legends, characters, backgrounds etc. from the statement while still enabling everyone to understand the problem. Also remove the name of the character if possible. This is to say, do not remove anything necessary to understand the full problem and one should feel safe to replace the original statement with your version of the statement. If it is not in English make it English. Provide the simplified statement directly without jargon. Use mathjax ($...$) for math. Start your response with \"Simplified statement:\"."
    client = Together()
    prompt = template.replace("[[ORIGINAL]]", statement).strip()
    print(f"Prompt: {prompt}\n")
    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
        messages=[
            {
                "role": "user",
                "content": prompt
            },
            {"role": "assistant", "content": "Simplified statement:"}
        ],
    )
    return response.choices[0].message.content.strip()
