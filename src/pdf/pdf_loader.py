from PyPDF2 import PdfReader
from langchain.docstore.document import Document
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings

import os


def document_pdf(pdf):

    reader = PdfReader(pdf)

    docs = []

    for i, page in enumerate(reader.pages):

        doc = Document(page_content=page.extract_text(), metadata={"page": i + 1})
        docs.append(doc)

    return docs


def embed(pages_doc, api_key):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)
    splits = text_splitter.split_documents(pages_doc)
    embedding = OpenAIEmbeddings(api_key=api_key)

    return splits, embedding


MASTER_DIR = "./VectorDB"


def create_db(name, splits, embedding):
    vectordb_dir = f"{MASTER_DIR}/{name}"
    if not os.path.exists(vectordb_dir):
        if not os.path.exists(MASTER_DIR):
            os.makedirs(MASTER_DIR)
        vectordb = Chroma.from_documents(
            documents=splits, embedding=embedding, persist_directory=vectordb_dir
        )
    else:
        print("Using existing DB")
        vectordb = Chroma(persist_directory=vectordb_dir, embedding_function=embedding)
        vectordb.add_documents(documents=splits)

    return vectordb
