# PDF Q&A System

## Objective
A command-line application that answers user questions based on the content of research papers stored as PDFs.
The system uses RAG (Retrieval-Augmented Generation) powered by Ollama + Qwen3, ChromaDB, and PyMuPDF4LLM, running in Docker containers.


## Core Functionality

   - Provide a command-line interface for users to ask questions relevant to the research papers
   
   - Retrieval-Augmented Generation (RAG) using local embedding, to generate answers based on the content of these papers
   
   - Text chunking strategies for better retrieval
   
   - Dockerized architecture for reproducibility and isolation

   - Local execution fro DB — external APIs required for LLM

   - Display sources/references for the answers

### Technical stack

- **Language:** Python 3.11
- **DB:** chomadb
- **LLM Model:** Use Qwen3 with ollama api
- **Delivery:** Docker

## System Architecture

The Python container runs the CLI and communicates with:

   - ChromaDB container via HTTP (for vector storage and retrieval)

   - Ollama API (for Qwen3 embeddings and answer generation)

Add image

### Assumptions and design decisions
| Component            | Choice                           | Rationale                                                                                   |
| -------------------- | -------------------------------- | ------------------------------------------------------------------------------------------- |
| **PDF Reader**       | PyMuPDF4LLM                      | Optimized for LLM-based applications, provides high-quality structured extraction from PDFs, good decision in case of scalability is needed   |
| **Vector Store**     | ChromaDB                         | Native Python client, easy to persist and query, supports cosine similarity out of the box, good in case that monitoring and scalability is needed |
| **LLM Backend**      | Ollama (Qwen3) API connetion     | It offer flexibility at the moment to try differents models, ideal for develpment process, easy to use and don't use local storage                   |
| **CLI Framework**    | Typer                            | Simple, readable, and provides automatic help messages                                                                          |
| **Containerization** | Docker + Docker Compose          | Isolated and reproducible environment for both app and ChromaDB. Easy to build and deliver. Good for the calability                                     |
| **Search Engine**    | Default Chroma similarity search | Reliable and performant for semantic retrieval. Good starting point for development process                                                            |

### Workflow Overview

Ingestion:
PDFs are parsed into text using PyMuPDF4LLM and split into overlapping chunks.

Embedding:
Each chunk is embedded via the Chroma's default embedding function `all-MiniLM-L6-v2`.

Storage:
The vectors and metadata are stored in the ChromaDB on the volume of the container.

Retrieval:
When a question is asked, its embedding is computed and compared to stored chunks using Chroma’s similarity search.

Generation:
Top-3 chunks are formatted into a context prompt and sent to Qwen3 for answer generation.

Response:
The system returns the answer along with references to the most relevant PDFs.

NOTE: Every time when a new file is added to the folder is needed to update the DB.

### Setup instructions
**Prerequisites**
* git 
* Docker & Docker Compose installed
* Python with venv installed(if you prefer run the python app without docker)
1. Clone the repository and go inside of the the folder pdf-helper
```bash
git clone https://github.com/ilCat/pdf-helper.git
cd pdf-helper
```
2. Build containers
```bash
docker-compose build 
```
This will:

* Start ChromaDB on its own container

* Start the Python app container with all dependencies installed

### How to run the application
0. Create a '.env' file using the '.env.example' content plus your OLLAMA_API_KEY
1. Build and run containers
```bash
docker-compose up --build -d
```
2. Open a new terminal  and run the next command to connect with the python container 
```bash
docker exec -it pdf-helper-app sh
```
3. To inspect the options run:
```bash
python main.py --help 
```
4. As it is the fisrt time running the app, it's needed to load the data to the DB. To update the DB  run:
```bash
python main.py update-db
```
5. To start  with the Q&A about the PDFs, run:
```bash
python main.py make-question
```

### Example usage
1. Build and run containers(inside of pdf-helper folder)
```bash
docker-compose up --build -d
```
2. Open a new terminal  and run the next command to connect with the python container 
```bash
docker exec -it pdf-helper-app sh
```
3. Update the DB  run:
```bash
python main.py update-db
```
4. Start  with the Q&A about the PDFs, run:
```bash
python main.py make-question
```

5. The program start with a little text and await for your question:
```bash
Hi, you can ask any question about the provided documents. What is your question about the papers?:
```
5. You have to write your question:
```bash
Is there any informations about UI
```
The system will answer the question and ask for another one.
```bash
 Do you have another question? Otherwise type 'exit' to close the chat
```
6. Type 'exit' to close the program.
```bash
exit
```
7. Type 'exit' again to close the connection with the container.
```bash
exit
```
8. Go to the terminal that was used to run the containers in step 1  and type the next commant to down the containers.
```bash
docker compose down 
```

### Improvements to do 
As it is a first approach it could work better:
* Improve performance responce
* Improve chunking strategi
* Add keyword search
* Add historical chat data an user identification 
* Improve error handling

