from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS


class TextService:
    def __init__(self):
        self.text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        self.embeddings = OpenAIEmbeddings()
        self.docsearch: FAISS = None

    def process(self, text: str):
        text = self.text_splitter.split_text(text)
        self.docsearch = FAISS.from_texts(text, self.embeddings)

    def search(self, query: str) -> list[Document]:
        return self.docsearch.similarity_search(query)
