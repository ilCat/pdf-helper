import os
from ollama import Client
from embed import EmbedEngine


client = Client(
    host="https://ollama.com",
    headers={"Authorization": "Bearer " + os.environ.get("OLLAMA_API_KEY")},
)


ee = EmbedEngine(name="myCollection")

SYSTEM_MESSAGE = """
You are a helpful assistant that answers questions about research papers.
You must use the data set to answer the questions,
you should not provide any info that is not in the provided sources.
Cite the sources you used to answer the question inside square brackets.
The sources are in the format: <id>: <text>.
"""
user_question = "Are ther advances in UI automation"


ee.load_docs("research_papers")
context = ee.get_context("Are ther advances in UI automation", 3)


messages = [
    {"role": "system", "content": SYSTEM_MESSAGE},
    {"role": "user", "content": f"{user_question}\nSources: {context}"},
]


for part in client.chat("qwen3-coder:480b-cloud", messages=messages, stream=True):
    print(part["message"]["content"], end="", flush=True)
