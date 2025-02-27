from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

class Embedder:
    def __init__(self):
        self.data_dir = "./data/chroma_db"

    def generate(self, document, corpus_name):
        # split it into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
        docs = text_splitter.create_documents([document])

        if (docs.__len__() > 0):
            print(f"Embedding resultant {docs.__len__()} documents into corpus {corpus_name}")

            # create the open-source embedding function
            embedding_function = OpenAIEmbeddings()
            # load it into Chroma
            Chroma.from_documents(docs, embedding_function, persist_directory=f"{self.data_dir}/{corpus_name}")

    def search(self, corpus_name, query):
        # create the open-source embedding function
        embedding_function = OpenAIEmbeddings()

        db_search = Chroma(persist_directory=f"{self.data_dir}/{corpus_name}", embedding_function=embedding_function)
        docs = db_search.similarity_search(query)

        return docs

