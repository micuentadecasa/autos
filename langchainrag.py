import dotenv
import os

dotenv.load_dotenv() 

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

from glob import glob

files = glob("*")

from langchain_community.document_loaders import DirectoryLoader
loader = DirectoryLoader('/users/luis/Documents/obsvault/', glob="**/*.md")
docs = loader.load()
print (len(docs))

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(docs)
embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(texts, embeddings)

question = " what is the latest 1on1 with david?"
searchDocs = db.similarity_search(question)
print(searchDocs[0].page_content)

retriever = db.as_retriever(search_kwargs={"k": 3})

from langchain.prompts import PromptTemplate

template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Keep the answer as concise as possible. 
{context}
Question: {question}
Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

from langchain import OpenAI
from langchain.chains import RetrievalQA
from langchain.agents import Tool

openai_llm = OpenAI(
    openai_api_key=OPENAI_API_KEY,
    temperature=0
)
qa_chain = RetrievalQA.from_chain_type(   
  llm=openai_llm,   
  chain_type="stuff",   
  retriever=db.as_retriever(),   
  chain_type_kwargs={"prompt": QA_CHAIN_PROMPT} 
) 
result = qa_chain ({ "query" : question }) 
print(result["result"])