import streamlit as st
from src import sidebar

from src import chat

from src.pdf import pdf_loader
from src.responser import responser

with st.sidebar:
    st.title("Environment variables")
    openai_api_key, vectordb_name, model_gpt, temp = sidebar.environment()


st.title("Chat with your Data")


def gen_vector_db(pdf):
    documents = pdf_loader.document_pdf(pdf)
    docs, embed = pdf_loader.embed(documents, api_key=openai_api_key)
    vector_db = pdf_loader.create_db(vectordb_name, docs, embed)
    return vector_db


vector_db_name_memory = f"vectordb_{vectordb_name}"

if vector_db_name_memory not in st.session_state:
    st.session_state[vector_db_name_memory] = None
else:
    Retriever = st.session_state[vector_db_name_memory]


with st.expander("ADD PDFS"):
    pdfs = st.file_uploader(
        "Ingrese el documento PDF", accept_multiple_files=True, type="pdf"
    )

    if not pdfs:
        st.stop()
    else:
        if st.button("Chat", type="primary", use_container_width=True):
            # with st.spinner()
            for pdf in pdfs:
                vector_db = gen_vector_db(pdf)

            # st.session_state["vectordb"] = None
            # if "vectordb" not in st.session_state:

            Retriever = responser.Response(
                vectordb=vector_db,
                llm_model=model_gpt,
                temperature=temp,
                api_key=openai_api_key,
            )
            st.session_state[vector_db_name_memory] = Retriever


print(Retriever)
if Retriever is not None:
    st.header("Ask")
    chat.chat_message(Retriever.gen_response)


# st.write(reader.pages)
