import streamlit as st, os

from dotenv import load_dotenv, find_dotenv


def environment():

    _ = load_dotenv(find_dotenv())

    openai_api_key = os.environ["OPENAI_API_KEY"]
    openai_api_key = st.text_input(
        "Insert your OPENAI API key: ",
        type="password",
        value=openai_api_key,
    )
    database = st.text_input("Insert name of the `vectorstorage`", value="default")
    model_gpt = st.selectbox(
        "Select model: ", ["gpt-3.5-turbo", "gpt-3.5-turbo-instruct"]
    )
    temperature = st.number_input("Temperature GPT: ", 0, 1)

    return openai_api_key, database, model_gpt, temperature
