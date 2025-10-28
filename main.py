import typer
from llm import llm_call
from embed import EmbedEngine


ee = EmbedEngine(name="research_papers")

app = typer.Typer()


@app.command()
def update_db():
    ee.load_docs("research_papers")
    print("Succesfull update")


@app.command()
def exit():
    print("\nBye")


@app.command()
def make_question():
    user_question = typer.prompt("What's your question about the papers?")
    context = ee.get_context(user_question, 2)
    llm_call(user_question, context)


@app.callback()
def callback():
    """
    Welcome! I'm a Q&A system to help undestand PDfs content"

    """


if __name__ == "__main__":
    app()
