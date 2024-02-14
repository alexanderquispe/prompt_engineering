from langchain.chains import RetrievalQA as RQa
from langchain.chat_models import ChatOpenAI


class Response:

    def __init__(
        self, vectordb, llm_model="gpt-3.5-turbo", temperature=0, api_key=None
    ):

        llm = ChatOpenAI(
            openai_api_key=api_key, model_name=llm_model, temperature=temperature
        )

        stuff = RQa.from_chain_type(
            llm, retriever=vectordb.as_retriever(), chain_type="stuff"
        )
        self.stuff = stuff

    def gen_response(self, query):
        stuff_result = self.stuff({"query": query})
        result = stuff_result.get("result")

        return result
