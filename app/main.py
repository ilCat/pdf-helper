import typer
from llm import llm_call
from embed import EmbedEngine
from datetime import datetime
from service import check_services

check_services()

ee = EmbedEngine(name="research_papers")


app = typer.Typer(pretty_exceptions_show_locals=False)


@app.command()
def update_db():
    ee.load_docs("research_papers")
    print("Succesfull update")


@app.command()
def make_question():
    keep_chating = True
    user_question = typer.prompt(
        "Hi, you can ask any question about the provided documents. What is your question about the papers?"
    )
    while keep_chating:
        context = ee.get_context(user_question, 3)
        llm_call(user_question, context)
        user_question = typer.prompt(
            "\n Do you have another question? Otherwise type 'exit' to close the chat\n"
        )
        if user_question.upper() == "EXIT":
            print("\nWas a pleasure.\nBye")
            break


@app.callback()
def callback():
    """
    Welcome! I'm a Q&A system to help undestand PDfs content"

    """


if __name__ == "__main__":
    app()
