from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing_extensions import List, TypedDict
from langgraph.graph import START, StateGraph
from langchain import hub

from langchain_postgres import PGVector
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from sqlalchemy import create_engine

# from constants.env import Envs
from dotenv import load_dotenv
import os

load_dotenv()


class Envs:
    DB_URL = os.getenv("DB_URL") or ""


COLLECTION_NAME = "langchain_vectors"

engine = create_engine(Envs.DB_URL)


vectorstore = PGVector(
    collection_name=COLLECTION_NAME, connection=Envs.DB_URL, use_jsonb=True, embeddings=GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
)

# DOCUMENTS
loader = CSVLoader(file_path="docs/data.csv", csv_args={"delimiter": ",", "quotechar": '"', "fieldnames": ["description", "stablishment", "total"]})

docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
all_splits = text_splitter.split_documents(docs)

vectorstore.add_documents(documents=all_splits)

prompt = hub.pull("rlm/rag-prompt")
example_messages = prompt.invoke({"context": "(context goes here)", "question": "(question goes here)"}).to_messages()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")


class State(TypedDict):
    question: str
    context: List[Document]
    answer: str


def retrieve(state: State):
    retrieved_docs = vectorstore.similarity_search(state["question"], k=100)
    return {"context": retrieved_docs}


def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response.content}


graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()

response = graph.invoke({"question": "how much i spent"})
print(response["answer"])
