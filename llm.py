import os
from dotenv import load_dotenv
from ollama import Client
from embed import EmbedEngine

load_dotenv()

client = Client(
    host="https://ollama.com",
    headers={"Authorization": "Bearer " + os.environ.get("OLLAMA_API_KEY")},
)


def llm_call(user_question, context):
    SYSTEM_MESSAGE = """
    You are a helpful assistant that answers questions about research papers.
    You must use the data set to answer the questions,
    you should not provide any info that is not in the provided sources.
    Cite the sources you used to answer the question inside square brackets.
    The sources are in the format: <id>: <text>.
    """

    messages = [
        {"role": "system", "content": SYSTEM_MESSAGE},
        {"role": "user", "content": f"{user_question}\nSources: {context}"},
    ]

    for part in client.chat("qwen3-coder:480b-cloud", messages=messages, stream=True):
        print(part["message"]["content"], end="", flush=True)
