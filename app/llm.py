import os
from dotenv import load_dotenv
from ollama import Client
from embed import EmbedEngine
from datetime import datetime

load_dotenv()

client = Client(
    host="https://ollama.com",
    headers={"Authorization": "Bearer " + os.environ.get("OLLAMA_API_KEY")},
)


def llm_call(user_question, context):

    SYSTEM_MESSAGE = """
    You are an AI research assistant designed to answer user questions based on a provided dataset of research papers.

    ### Instructions:
    - Use **only** the information from the provided sources to answer questions. 
    - **Do not** include any outside knowledge, assumptions, or speculation.
    - When citing, use the format: [source_id]. 
    - If the answer cannot be found in the sources, reply: "The provided sources do not contain information to answer this question."
    - Summarize and synthesize the relevant parts of the sources to create a clear, concise, and accurate answer.

    ### Source Format:
    Each source is provided as:
    <id>: <text>

    ### Example:
    **User Question:** What are the main findings about quantum entanglement?

    **Answer:** The studies indicate that quantum entanglement allows instantaneous correlations between particles regardless of distance [3][7].

    Now begin answering user questions based on the provided sources.
    """

    messages = [
        {"role": "system", "content": SYSTEM_MESSAGE},
        {"role": "user", "content": f"{user_question}\nSources: {context}"},
    ]

    response = ""
    for part in client.chat("qwen3-coder:480b-cloud", messages=messages, stream=True):
        print(part["message"]["content"], end="", flush=True)
        response = response + part["message"]["content"]
