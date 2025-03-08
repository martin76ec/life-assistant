from langchain.vectorstores import PGVector
from langchain.embeddings.vertexai import VertexAIEmbeddings
from sqlalchemy import create_engine
from constants.env import Envs

COLLECTION_NAME = "langchain_vectors"

engine = create_engine(Envs.DB_URL)

vectorstore = PGVector(
    collection_name=COLLECTION_NAME,
    connection_string=Envs.DB_URL,
    embedding_function=VertexAIEmbeddings()
)
