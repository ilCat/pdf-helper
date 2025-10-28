import pymupdf
import chromadb
import os
from dotenv import load_dotenv
import pymupdf4llm
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rich.progress import track

load_dotenv()


class EmbedEngine:
    def __init__(self, name):
        self.name = name
        self.client = chromadb.HttpClient(
            host=os.environ.get("DB_HOST"), port=os.environ.get("DB_PORT")
        )
        self.db = self.client.get_or_create_collection(
            name=self.name,
            configuration={"hnsw": {"space": "cosine", "ef_construction": 100}},
        )

    def load_docs(self, dir):
        content = []
        meta_data = []
        idx = []

        try:
            for name in track(os.listdir(dir), description="Loading..."):
                print(f"Processing content of '{name}'")
                pdf = pymupdf4llm.to_markdown(os.path.join(dir, name))

                text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                    chunk_size=500, chunk_overlap=125
                )
                texts = text_splitter.create_documents([pdf])
                loaded_ids = self.db.get()["ids"]
                for i, text in enumerate(texts):
                    id = name + str(i + 1)
                    if id not in loaded_ids:
                        idx.append(id)
                        content.append(text.page_content)
                        meta_data.append({"book": name, "section": str(i + 1)})
        except:
            raise TypeError(
                f"There is a problem with the folder {dir}, check if not exist or is empty"
            )
        if len(idx) > 0:
            self.db.upsert(ids=idx, documents=content, metadatas=meta_data)
        else:
            print("All data is already in the db. Nothing to update")

    def __response_map(self, data):
        response = {}
        for i in range(len(data["ids"][0])):
            md = data["metadatas"][0][i]
            response.update(
                {md["book"] + "- section:" + md["section"]: data["documents"][0][i]}
            )
        return response

    def get_context(self, context, num_results):
        try:
            resp = self.db.query(query_texts=[context], n_results=num_results)

            return self.__response_map(resp)
        except:
            raise TypeError(f"Error to connect to DB, check HOST and PORT values")
