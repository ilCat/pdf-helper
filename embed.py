import pymupdf
import chromadb
import os
import pymupdf4llm
from langchain_text_splitters import RecursiveCharacterTextSplitter


class EmbedEngine:
    def __init__(self, name):
        self.name = name
        self.client = chromadb.Client()
        self.db = self.client.get_or_create_collection(
            name=self.name,
            configuration={"hnsw": {"space": "cosine", "ef_construction": 100}},
        )

    def load_docs(self, dir):
        content = []
        meta_data = []
        idx = []

        for name in os.listdir(dir):
            print(f"Content of '{name}'")
            pdf = pymupdf4llm.to_markdown(os.path.join(dir, name))

            text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                chunk_size=500, chunk_overlap=125
            )
            texts = text_splitter.create_documents([pdf])
            for i, text in enumerate(texts):
                idx.append(str(hash(name + str(i + 1))))
                content.append(text.page_content)
                meta_data.append({"book": name, "section": str(i + 1)})

        self.db.upsert(ids=idx, documents=content, metadatas=meta_data)

    def __response_map(self, data):
        response = {}
        for i in range(len(data["ids"][0])):
            md = data["metadatas"][0][i]
            response.update(
                {md["book"] + "- section:" + md["section"]: data["documents"][0][i]}
            )
        return response

    def get_context(self, context, num_results):
        resp = self.db.query(query_texts=[context], n_results=num_results)

        return self.__response_map(resp)
