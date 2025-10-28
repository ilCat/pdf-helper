import requests
import typer
import os
from dotenv import load_dotenv
import chromadb

load_dotenv()


def check_services():
    try:
        client = chromadb.HttpClient(
            host=os.environ.get("DB_HOST"), port=os.environ.get("DB_PORT")
        )
        client.heartbeat()
    except Exception:
        typer.echo(
            "Cannot connect to ChromaDB. Check the container Port ,host, and status "
        )
        raise typer.Exit(code=1)

    try:
        OLLAMA_HOST = os.environ.get("OLLAMA_HOST")
        requests.get(f"{OLLAMA_HOST}/api/version", timeout=3)
    except Exception:
        typer.echo("Ollama is not running or not reachable.")
        raise typer.Exit(code=1)
